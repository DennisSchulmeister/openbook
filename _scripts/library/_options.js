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
import yaml    from "yaml";
import JSZip   from "jszip";

/**
 * Shared logic for all scripts to determine the build options.
 */
export function getOptions() {
    const cwd  = process.cwd();
    const name = path.basename(cwd);

    return {
        infile: path.join(cwd, "src", "index.ts"),
        watch:  process.argv[2] === "--watch",

        staticdirs: [
            path.join(cwd, "components"),
            path.join(cwd, "static"),
        ],

        outfiles:  [
            path.join(cwd, "dist", "library.js"),
            path.join(cwd, "..", "..", "_media", "lib", name, "library.js"),
        ],

        plugins: [
            createLibraryYml(cwd, path.join(cwd, "dist", "library.yml")),
            createLibraryZip(path.join(cwd, "dist"), path.join(cwd, "zip", "library.zip")),
        ],
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
 * Internal plugin the creates a ZIP file with the bundled library source code,
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