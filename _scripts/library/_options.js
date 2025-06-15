/*
 * OpenBook: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import fs      from "node:fs/promises";
import path    from "node:path";
import process from "node:process";

import {Ajv}   from "ajv";
import {glob}  from "glob";
import JSZip   from "jszip";
import shelljs from "shelljs";
import yaml    from "yaml";

/**
 * Shared logic for all scripts to determine the build options.
 */
export function getOptions() {
    const cwd  = process.cwd();
    const name = path.basename(cwd);

    return {
        infile: path.join(cwd, "src", "index.ts"),
        watch:  process.argv[2] === "--watch",

        outfiles:  [
            path.join(cwd, "dist", "library.js"),
        ],

        plugins: [
            logHeader(cwd),
            validateAndCopyElementYml(cwd, path.join(cwd, "dist")),
            createLibraryYml(cwd, path.join(cwd, "dist", "library.yml")),
            createLibraryZip(path.join(cwd, "dist"), path.join(cwd, "zip", "library.zip")),
            copyToInstallLocation(
                cwd,
                path.join(cwd, "zip", "library.zip"),
                path.join(cwd, "..", "..", "_media", "lib")),
        ],
    };
}

/**
 * Internal plugin that logs a header with the name of the currently built library.
 * @param {string} cwd Root directory of the library
 * @returns esbuild plug-in instance
 */
function logHeader(cwd) {
    return {
        name: "logHeader",
        setup(build) {
            build.onStart(async () => {
                let packageJsonFile = await fs.readFile(path.join(cwd, "package.json"), "utf-8");
                let packageJson     = JSON.parse(packageJsonFile);
                let logLine         = `Building library ${packageJson.name} ${packageJson.version}`;
                let separator       = "=".repeat(logLine.length);

                console.log();
                console.log(separator);
                console.log(logLine);
                console.log(separator);
                console.log();
            });
        },
    };
}

/**
 * Copy YML files describing the custom elements to the WYSIWYG editor to a
 * new directory called `elements`. Also validates the YML files and raises
 * an error when validation fails.
 * 
 * @param {string} cwd Root directory of the library
 * @param {string} outdir Build output directory
 * @returns esbuild plug-in instance
 */
function validateAndCopyElementYml(cwd, outdir) {
    return {
        name: "copyElementYml",
        setup(build) {
            build.onEnd(async () => {
                console.log("COPY ELEMENT YAML FILES");

                let srcDir            = path.join(cwd, "src");
                let elementSchemaFile = await fs.readFile(path.join(import.meta.dirname, "element-schema.yml"), "utf-8");
                let elementSchemaYml  = yaml.parse(elementSchemaFile);
                let ajv = new Ajv();

                for (let srcFile of await glob([path.join(srcDir, "**", "*.yml")])) {
                    // Validate file
                    let elementFile = await fs.readFile(path.join(srcFile), "utf-8");
                    let elementYml  = yaml.parse(elementFile);

                    await ajv.validate(elementSchemaYml, elementYml);
                    if (ajv.errors) throw ajv.errors;

                    // Copy file
                    srcFile = path.relative(srcDir, srcFile);
                    shelljs.mkdir("-p", path.join(outdir, "elements", path.dirname(srcFile)));
                    shelljs.cp("-R", path.join("src", srcFile), path.join(outdir, "elements", srcFile));
                }
            });
        },
    };
}

/**
 * Internal plugin that reads the meta-data from `package.json` and `README.md`
 * to creates the `library.yml` file. This file is used by the OpenBook server
 * when installing a library to check that it is a valid library and show some
 * information to the admin.
 * 
 * @param {string} cwd Root directory of the library
 * @param {string} outfile Path of the created file
 * @returns esbuild plug-in instance
 */
function createLibraryYml(cwd, outfile) {
    return {
        name: "createLibraryYmlPlugin",
        setup(build) {
            build.onEnd(async () => {
                console.log("CREATE LIBRARY YAML");

                let packageJsonFile = await fs.readFile(path.join(cwd, "package.json"), "utf-8");
                let packageJson     = JSON.parse(packageJsonFile);
                let readmeFile      = await fs.readFile(path.join(cwd, "README.md"), "utf-8");

                let data = {
                    name:        packageJson.name,
                    version:     packageJson.version,
                    description: packageJson.description,
                    author:      packageJson.author,
                    readme:      readmeFile,
                };

                await fs.writeFile(outfile, yaml.stringify(data));
            });
        },
    };
}

/**
 * Internal plugin that creates a ZIP file with the bundled library source code,
 * ready to be installed on the OpenBook server.
 * 
 * @param {string} distdir Directory with the pre-built distribution files
 * @param {string} outfile Path of the created file
 * @returns esbuild plug-in instance
 */
function createLibraryZip(distdir, outfile) {
    return {
        name: "createLibraryZipPlugin",
        setup(build) {
            build.onEnd(async () => {
                console.log("CREATE LIBRARY ZIP");

                try {
                    await fs.unlink(outfile);
                } catch {
                    // File didn't exist                
                }

                fs.mkdir(path.dirname(outfile), {recursive: true});
                
                let zip = new JSZip();
                let folder = zip.folder("openbook-library");

                async function _addDirectoryContent(zip, srcdir) {
                    for (let entry of await fs.readdir(srcdir, {withFileTypes: true})) {
                        let entryPath = path.join(srcdir, entry.name);

                        if (entry.isDirectory()) {
                            let subfolder = zip.folder(entry.name);
                            await _addDirectoryContent(subfolder, entryPath);
                        } else {
                            let data = await fs.readFile(entryPath);
                            zip.file(entry.name, data);   
                        }
                    }
                }

                await _addDirectoryContent(folder, distdir);
                let zipContent = await zip.generateAsync({type: "nodebuffer"});
                await fs.writeFile(outfile, zipContent);
            });
        },
    };
}

/**
 * Internal plugin that copies and renames the built ZIP file so that can be
 * automatically installed by the OpenBook server.
 * 
 * @param {string} cwd Root directory of the library
 * @param {string} zipfile Path to the built ZIP file
 * @param {string} outdir Install directory
 * @returns esbuild plug-in instance
 */
function copyToInstallLocation(cwd, zipfile, outdir) {
    return {
        name: "copyToInstallLocation",
        setup(build) {
            build.onEnd(async () => {
                console.log("COPY LIBRARY ZIP TO INSTALL LOCATION");
                
                let packageJsonFile = await fs.readFile(path.join(cwd, "package.json"), "utf-8");
                let packageJson     = JSON.parse(packageJsonFile);
                let dstFile         = `${packageJson.name}_${packageJson.version}.zip`.replaceAll("/", "_");

                shelljs.cp("-R", zipfile, path.join(outdir, dstFile));
            });
        },
    };
}