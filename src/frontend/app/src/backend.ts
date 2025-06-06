/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import * as apiClient  from "./api-client/index.js";
import {Configuration} from "./api-client/index.js";

// Fetch backend URL
let response  = await fetch("server.url");
let serverUrl = await response.text();

while (serverUrl.endsWith("/")) {
    serverUrl = serverUrl.slice(0, serverUrl.length - 1);
}

let configuration = new Configuration({
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
    // Core App
    availableLanguages:     new apiClient.AvailableLanguagesApi(configuration),
    mediaFiles:             new apiClient.MediaFilesApi(configuration),
    websites:               new apiClient.WebsitesApi(configuration),

    // Auth App
    accessRequests:         new apiClient.AccessRequestsApi(configuration),
    allowedRolePermissions: new apiClient.AllowedRolePermissionsApi(configuration),
    currentUser:            new apiClient.CurrentUserApi(configuration),
    enrollmentMethods:      new apiClient.EnrollmentMethodsApi(configuration),
    roleAssignments:        new apiClient.RoleAssignmentsApi(configuration),
    roles:                  new apiClient.RolesApi(configuration),
    scopeTypes:             new apiClient.ScopeTypesApi(configuration),
    translatedPermissions:  new apiClient.TranslatedPermissionsApi(configuration),
    userProfiles:           new apiClient.UserProfilesApi(configuration),

    // Course App
    courses:                new apiClient.CoursesApi(configuration),
}
