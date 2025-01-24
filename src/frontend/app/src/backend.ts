/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

/**
 * HTTP method for backend call
 */
export type HTTPMethod = "GET" | "PUT" | "POST" | "PATCH" | "DELETE" | "HEAD" | "OPTIONS"
                       | "get" | "put" | "post" | "patch" | "delete" | "head" | "options";

/**
 * URL path string for backend call (everything after protocol, server and port).
 */
export type PathString = string;

/**
 * Additional options for backend calls
 */
export type BackendFetchOptions = {
    /**
     * Query parameters
     */
    query?: Record<string, any>,

    /**
     * HTTP request headers
     */
    headers?: Record<string, string>;

    /**
     * HTTP request body data (will be serialized to JSON)
     */
    body?: any,
};

/**
 * Unified class to encapsulate all backend access. This class provides an
 * internal interface that makes it easier to call the backend functions by
 * hiding the HTTP communication from its users and ensuring uniform requests.
 */
export class Backend {
    /**
     * Root URL of the backend Django application.
     */
    private $url: string = "";

    /**
     * Fetch backend URL from file `server.url`. In the Docker template this can be
     * given in the `OB_SERVER_URL` environment variable. For custom deployments the
     * admin must make sure that the root URL of the Django app is written into this
     * file during deployment.
     */
    async init() {
        // Fetch backend URL
        let response = await fetch("server.url");
        this.$url = await response.text();

        // Remove trailing slashes
        while (this.$url.endsWith("/")) {
            this.$url = this.$url.slice(0, this.$url.length - 1);
        }
    }

    /**
     * Low level wrapper around the native fetch API to make sure that all backend
     * requests follow an uniform structure. Usage example:
     *
     *   * backend.fetch("GET", "/api/sites/health");
     *   * backend.fetch("GET", "/api/example", {query: {first_name: "Test"}});
     *   * backend.fetch("PUT", "/api/example", {body: { ... }});
     *
     * The optional options object can be used to pass query parameters, which will be
     * appended as URL parameters. Additionally, body data, which will automatically
     * serialized as JSON, can be passed.
     * 
     * @param method HTTP method (e.g. "GET" or "get")
     * @param path Requested path (without the URL prefix of the server)
     * @param options Optional request configuration values
     * @returns Result of the actual `fetch()` call
     * @throws an exception when a backend error is received
     */
    async fetch(method: HTTPMethod, path: PathString, options?: BackendFetchOptions) {
        options = options || {};
        method  = method.toUpperCase() as HTTPMethod;

        // Append query parameter to URL
        if (options?.query) {
            let parameters = new URLSearchParams();

            for (let name in options.query) {
                parameters.append(name, options.query[name]);
            }

            path = `${path}?${parameters}`;
        }

        // Use given HTTP method, header fields and body        
        let fetchOptions = {
            method:      method,
            headers:     new Headers(options?.headers || {}),
            credentials: "include",
            body:        undefined as undefined|string,
        };

        if (method !== "GET") {
            fetchOptions.headers.set("Content-Type", "application/json");

            if (options?.body) {
                fetchOptions.body = JSON.stringify(options.body);
            }
        }

        fetchOptions.headers.set("Accept", "application/json");

        // Call REST webservice
        let response = await fetch(`${this.$url}${path}`, fetchOptions as RequestInit);

        if (response.ok) {
            return await response.json();
        } else {
            // Throw exception when an error was received
            let contentType = response.headers.get("Content-Type") || "";

            if (contentType.includes("json")) {
                throw await response.json();
            } else {
                throw {
                    code: "SERVER_ERROR",
                    message: `HTTP ${response.status} ${response.statusText}: ${await response.text()}`,
                };
            }
        }
    }
}

// Initialize and export semi-singleton object
const backend = new Backend();
await backend.init();

export default backend;