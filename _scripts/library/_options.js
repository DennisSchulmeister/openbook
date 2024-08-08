/*
 * OpenBook Studio: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import path    from "node:path";
import process from "node:process";

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
            path.join(cwd, "library.yml"),
        ],

        outfiles:  [
            path.join(cwd, "dist", "library.js"),
            path.join(cwd, "..", "..", "openbook_server", "_media", "lib", name, "library.js"),
        ],
    };
}
