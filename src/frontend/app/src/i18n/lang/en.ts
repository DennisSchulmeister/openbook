/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// This is the master language. Therefor no type import here.
export default {
    Placeholder: {
        Title: "OpenBook",
        Text:  "Under Construction!",

        BackendStatus: {
            Checking: "Checking Now …",
            Online:   "Online",
            Offline:  "Offline",
        },
    },

    Error404: {
        Title:    "Page not found",
        Message1: "We are terribly sorry, but the requested page <b>$url$</b> cannot be found.",
        Message2: 'Maybe go back to the <a href="#/">home page</a> and grab some other cheese, instead?',
    },
};