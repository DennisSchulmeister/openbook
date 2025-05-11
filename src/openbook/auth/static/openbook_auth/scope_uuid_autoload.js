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
document.addEventListener("DOMContentLoaded", () => {
    let scopeTypeField = document.querySelector("#id_scope_type");
    let scopeUuidField = document.querySelector("#id_scope_uuid");

    if (!scopeTypeField || !scopeUuidField) return;

    async function updateScopeUuidChoices(scopeType) {
        try {
            let results = [];

            if (scopeType) {
                let url = `/api/auth/scopes/?scope_type=${scopeType}`;
                let response = await fetch(url);
    
                if (!response.ok) {
                    throw new Error(await response.text());
                }
    
                results = (await response.json()) || [];
            }

            // Clear and repopulate scopeUuidField
            debugger;
            selectedValue = scopeUuidField.querySelector("[selected]")?.value || "";
            scopeUuidField.innerHTML = "";

            for (let result of results) {
                let option = new Option(result.scope_name, result.scope_uuid);
                if (result.scope_uuid === selectedValue) option.selected = true;
                scopeUuidField.appendChild(option);
            }

            if (!selectedValue) {
                let option = new Option("", "");
                option.setAttribute("selected", "");
                scopeUuidField.appendChild(option);
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
