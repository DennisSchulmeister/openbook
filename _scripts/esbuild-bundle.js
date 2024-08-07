/*
 * OpenBook Studio: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import * as esbuild from "esbuild";
import {lessLoader} from "esbuild-plugin-less";
import path         from "path";

if (process.argv.length < 4) {
    console.error(`Arguments missing. Usage: ${process.argv[1]} source_file out_file`);
    process.exit(-1);
}

let infile  = process.argv[2].replaceAll("\\", path.sep).replaceAll("/", path.sep);
let outfile = process.argv[3].replaceAll("\\", path.sep).replaceAll("/", path.sep);

let ctx = await esbuild.context({
    entryPoints: [infile],
    bundle:      true,
    minify:      true,
    outfile:     outfile,
    sourcemap:   true,
    plugins:     [lessLoader()],

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

if (process.env.NODE_ENV === "development") {
    console.log("esbuild - starting watch mode");
    await ctx.watch();
} else {
    console.log("esbuild - building assets");
    await ctx.rebuild();
    await ctx.dispose();
}
