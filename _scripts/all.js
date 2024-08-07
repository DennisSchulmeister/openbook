/*
 * OpenBook Studio: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import concurrently from "concurrently";
//import fs           from "node:fs/promises";
import {glob}       from "glob";
import path         from "node:path";
import url          from "node:url";

const __dirname = url.fileURLToPath(new url.URL(".", import.meta.url));

let script = process.argv[2].replaceAll("/", path.sep).replaceAll("\\", path.sep);
script = path.join(__dirname, script);

let commands = [];
let packageJsons = await glob(path.join("*", "package.json"));

for (let packageJson of packageJsons || []) {
    let subdir = path.dirname(packageJson);
    commands.push({ name: subdir, command: `node ${script}`, cwd: subdir });
}

concurrently(commands, {
    raw: true,
    prefixColors: ["auto"],
});
