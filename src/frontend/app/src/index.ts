/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import "./index.css";
import "./global.js";

import ApplicationFrame from "./components/ApplicationFrame.svelte";
import {mount}          from 'svelte';

mount(ApplicationFrame, {target: document.body});
