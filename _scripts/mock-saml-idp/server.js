/*
 * OpenBook: Interactive Online Textbooks
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import {startServer} from 'mock-saml-idp';

/**
 * Configure and start mock SAML IDP server to local testing and unit tests.
 */
const {url} = await startServer({
    port: 8886,          // default: 7000
    host: "localhost",   // default: localhost

    // Default user shown in the login form. Actually the server accepts all
    // credentials and simply passes them on to the service provider. For testing
    // we use different e-mail domains to assign initial permission groups:
    // @student.com, @teacher.com
    defaultUser: {
        nameId:    "alice@student.com",
        firstName: "Alice",
        lastName:  "Student",
    },
});

console.log(`Mock SAML IdP running at ${url}`);