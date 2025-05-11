/*
* OpenBook: Interactive Online Textbooks - Server
* © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*/

/**
 * Update scope uuid choices according to the selected scope type.
 * The choices are fetched via the API.
 */
document.addEventListener("DOMContentLoaded", async () => {
    let scopeTypeField;
    let scopeUuidField;
    let permissionsFromField;
    let count = 0;

    while (!permissionsFromField && count < 100) {
        await new Promise(resolve => window.setTimeout(resolve, 250));
        count++;

        scopeTypeField       = document.querySelector("#id_scope_type");
        scopeUuidField       = document.querySelector("#id_scope_uuid");
        permissionsFromField = document.querySelector("#id_permissions_from");
    }

    if (!permissionsFromField) {
        console.error("Field #id_permissions_from is still not available. Aborting!");
        return;
    }

    async function updateScopeUuidChoices(scopeType) {
        try {
            let result = {};

            if (scopeType) {
                let url = `/api/auth/scopes/${scopeType}`;
                let response = await fetch(url);
    
                if (!response.ok) {
                    throw new Error(await response.text());
                }
    
                result = (await response.json()) || {};
            }

            // Clear and repopulate scopeUuidField
            selectedValue = scopeUuidField.querySelector("[selected]")?.value || "";
            scopeUuidField.innerHTML = "";

            for (let scope_object of result.objects || []) {
                let option = new Option(scope_object.name, scope_object.uuid);
                if (scope_object.uuid === selectedValue) option.selected = true;
                scopeUuidField.appendChild(option);
            }

            if (!selectedValue) {
                let option = new Option("", "");
                option.setAttribute("selected", "");
                scopeUuidField.appendChild(option);
            }

            // Hide disallowed permissions from the permission filter
            if (!result.allowed_permissions) result.allowed_permissions = [];

            for (let option of permissionsFromField.querySelectorAll("option")) {
                option.style.display = "None";
                
                let allowed_permission = result.allowed_permissions?.find(entry => entry.id == option.value);
                if (!allowed_permission) continue;

                delete option.style.display;
                option.setAttribute("title", `${allowed_permission.app} | ${allowed_permission.name}`);
            }
        } catch (err) {
            console.error("Failed to load scope UUIDs:", err);
        }
    }

    scopeTypeField.addEventListener("change", () => {
        let selected = scopeTypeField.value || "";
        updateScopeUuidChoices(selected);
    });

    // Load initial data if editing an existing instances
    updateScopeUuidChoices(scopeTypeField.value || "");
});
