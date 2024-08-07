/*
 * OpenBook Studio: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import * as esbuild from "esbuild";
import {lessLoader} from "esbuild-plugin-less";
import path         from "node:path";
import shelljs      from "shelljs";

/**
 * Centralized esbuild configuration to build JavaScript assets. This is used
 * by the higher-level build scripts which find the source files and determine
 * what destination files need to be created.
 *
 * There must be exactly one source file that imports all other files to be
 * included in the build. Normally a single bundle will be created from that.
 * For the libraries we however support creating multiple identical bundles
 * at different locations. Bundles always consist of a *.js and *.css file
 * plus copied over static files.
 *
 * @param infile {string} Full path of the main source file
 * @param outfiles {string[]} Full path of all bundle files to be created
 * @param staticdir {string} Path with static files to be copied (optional)
 * @param watch {bool} Keep running and rebuild on file changes (optional)
 * @param plug-in {object[]} Additional esbuild plug-ins (optional)
 */
export async function runEsbuild({infile, outfiles, staticdir, watch, plugins} = {}) {
    plugins = plugins || [];

    let ctx = await esbuild.context({
        entryPoints: [infile],
        bundle:      true,
        minify:      true,
        outfile:     outfiles[0],
        sourcemap:   true,

        plugins: [
            lessLoader(),
            additionalOutfilesPlugin(outfiles),
            staticFilesPlugin(outfiles, staticdir),
            ...plugins
        ],

        loader: {
            ".svg":   "text",
            ".ttf":   "dataurl",
            ".woff":  "dataurl",
            ".woff2": "dataurl",
            ".eot":   "dataurl",
            ".jpg":   "dataurl",
            ".png":   "dataurl",
            ".gif":   "dataurl",
        },
    });

    if (watch) {
        console.log("esbuild - starting watch mode");
        await ctx.watch();
    } else {
        console.log("esbuild - building bundles");
        await ctx.rebuild();
        await ctx.dispose();
    }
}

/**
 * Internal plug-in that creates duplicate output files, if the same bundle
 * shall be built multiple times at different locations. The first entry of
 * the given array will be ignored as this is the file that esbuild creates
 * anyway. The plug-in just copies this file to the other locations after
 * the build.
 *
 * @param outfiles {string[]} Full path of bundle files to be created
 * @param staticdir {string} Path with static files to be copied (optional)
 * @returns esbuild plug-in instance
 */
function additionalOutfilesPlugin(outfiles) {
    return {
        name: "additionalOutfilesPlugin",
        setup(build) {
            if (outfiles.length < 2) return;

            let bundle = path.parse(outfiles[0]);
            let src = path.join(bundle.dir, `${bundle.name}.*`);

            build.onEnd(result => {
                for (let outfile of outfiles.slice(1)) {
                    let dst = path.dirname(outfile);
                    shelljs.mkdir("-p", dst);
                    shelljs.cp("-R", src, dst);
                }
            });
        },
    };
}

/**
 * Internal plug-in that copies additional static files
 *
 * @param outfiles {string[]} Full path of all bundle files to be created
 * @param staticdir {string} Path with static files to be copied (optional)
 * @returns esbuild plug-in instance
 */
function staticFilesPlugin(outfiles, staticdir) {
    return {
        name: "staticFilesPlugin",
        setup(build) {
            if (!outfiles || outfiles.length < 1) return;
            if (!staticdir) return;

            let src = path.join(staticdir, "*");

            build.onEnd(result => {
                for (let outfile of outfiles) {
                    let dst = path.dirname(outfile);
                    shelljs.mkdir("-p", dst);
                    shelljs.cp("-R", src, dst);
                }
            });
        },
    };
}
