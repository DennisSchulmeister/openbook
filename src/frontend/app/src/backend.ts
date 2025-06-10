/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import * as authClient                      from "./auth-client/index.js";
import * as apiClient                       from "./api-client/index.js";
import {Configuration as AuthConfiguration} from "./auth-client/index.js";
import {Configuration as ApiConfiguration}  from "./api-client/index.js";

// Fetch backend URL
let response  = await fetch("server.url");
let serverUrl = await response.text();

while (serverUrl.endsWith("/")) {
    serverUrl = serverUrl.slice(0, serverUrl.length - 1);
}

let apiConfiguration = new ApiConfiguration({
    basePath: serverUrl,
    headers: {
        "X-CSRFToken": document.cookie.match(/csrftoken=([\w]+)/)?.[1] || "",
    },
});

let authConfiguration = new AuthConfiguration({
    basePath: serverUrl,
    headers: {
        "X-CSRFToken": document.cookie.match(/csrftoken=([\w]+)/)?.[1] || "",
    },
});

/**
 * Pre-instantiated client objects, generated from the OpenAPI specification.
 * The clients objects automatically use the correct base URL of the server.
 */
export default {
    // Auth API
    account: {
        email:                  new authClient.AccountEmailApi(authConfiguration),
        password:               new authClient.AccountPasswordApi(authConfiguration),
        phone:                  new authClient.AccountPhoneApi(authConfiguration),
        providers:              new authClient.AccountProvidersApi(authConfiguration),
    },

    authentication: {
        account:                new authClient.AuthenticationAccountApi(authConfiguration),
        currentSession:         new authClient.AuthenticationCurrentSessionApi(authConfiguration),
        loginByCode:            new authClient.AuthenticationLoginByCodeApi(authConfiguration),
        passwordReset:          new authClient.AuthenticationPasswordResetApi(authConfiguration),
        providers:              new authClient.AuthenticationProvidersApi(authConfiguration),
    },

    // Core App
    core: {
        availableLanguages:     new apiClient.AvailableLanguagesApi(apiConfiguration),
        mediaFiles:             new apiClient.MediaFilesApi(apiConfiguration),
        websites:               new apiClient.WebsitesApi(apiConfiguration),
    },

    // Auth App
    auth: {
        accessRequests:         new apiClient.AccessRequestsApi(apiConfiguration),
        allowedRolePermissions: new apiClient.AllowedRolePermissionsApi(apiConfiguration),
        currentUser:            new apiClient.CurrentUserApi(apiConfiguration),
        enrollmentMethods:      new apiClient.EnrollmentMethodsApi(apiConfiguration),
        roleAssignments:        new apiClient.RoleAssignmentsApi(apiConfiguration),
        roles:                  new apiClient.RolesApi(apiConfiguration),
        scopeTypes:             new apiClient.ScopeTypesApi(apiConfiguration),
        translatedPermissions:  new apiClient.TranslatedPermissionsApi(apiConfiguration),
        userProfiles:           new apiClient.UserProfilesApi(apiConfiguration),
    },

    // Course App
    course: {
        courses:                new apiClient.CoursesApi(apiConfiguration),
    },
}
