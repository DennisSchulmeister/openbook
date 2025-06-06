/* tslint:disable */
/* eslint-disable */
/**
 * OpenBook API
 * Beautiful and Engaging Learning Materials
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  CurrentUser,
  PaginatedCurrentUserList,
  PatchedCurrentUser,
} from '../models/index';
import {
    CurrentUserFromJSON,
    CurrentUserToJSON,
    PaginatedCurrentUserListFromJSON,
    PaginatedCurrentUserListToJSON,
    PatchedCurrentUserFromJSON,
    PatchedCurrentUserToJSON,
} from '../models/index';

export interface AuthCurrentUserRequest {
    expand?: string;
    fields?: string;
    omit?: string;
    page?: number;
    pageSize?: number;
    search?: string;
    sort?: string;
}

export interface AuthCurrentUserCreateRequest {
    currentUser: Omit<CurrentUser, 'id'|'full_name'|'is_authenticated'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthCurrentUserDestroyRequest {
    id: number;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthCurrentUserPartialUpdateRequest {
    id: number;
    expand?: string;
    fields?: string;
    omit?: string;
    patchedCurrentUser?: Omit<PatchedCurrentUser, 'id'|'full_name'|'is_authenticated'>;
}

export interface AuthCurrentUserUpdateRequest {
    id: number;
    currentUser: Omit<CurrentUser, 'id'|'full_name'|'is_authenticated'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

/**
 * 
 */
export class CurrentUserApi extends runtime.BaseAPI {

    /**
     * Returns the currently authenticated user or a fallback response.
     * Retrieve
     */
    async authCurrentUserRaw(requestParameters: AuthCurrentUserRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PaginatedCurrentUserList>> {
        const queryParameters: any = {};

        if (requestParameters['expand'] != null) {
            queryParameters['_expand'] = requestParameters['expand'];
        }

        if (requestParameters['fields'] != null) {
            queryParameters['_fields'] = requestParameters['fields'];
        }

        if (requestParameters['omit'] != null) {
            queryParameters['_omit'] = requestParameters['omit'];
        }

        if (requestParameters['page'] != null) {
            queryParameters['_page'] = requestParameters['page'];
        }

        if (requestParameters['pageSize'] != null) {
            queryParameters['_page_size'] = requestParameters['pageSize'];
        }

        if (requestParameters['search'] != null) {
            queryParameters['_search'] = requestParameters['search'];
        }

        if (requestParameters['sort'] != null) {
            queryParameters['_sort'] = requestParameters['sort'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/current_user/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PaginatedCurrentUserListFromJSON(jsonValue));
    }

    /**
     * Returns the currently authenticated user or a fallback response.
     * Retrieve
     */
    async authCurrentUser(requestParameters: AuthCurrentUserRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PaginatedCurrentUserList> {
        const response = await this.authCurrentUserRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Current User
     * Create
     */
    async authCurrentUserCreateRaw(requestParameters: AuthCurrentUserCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<CurrentUser>> {
        if (requestParameters['currentUser'] == null) {
            throw new runtime.RequiredError(
                'currentUser',
                'Required parameter "currentUser" was null or undefined when calling authCurrentUserCreate().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['expand'] != null) {
            queryParameters['_expand'] = requestParameters['expand'];
        }

        if (requestParameters['fields'] != null) {
            queryParameters['_fields'] = requestParameters['fields'];
        }

        if (requestParameters['omit'] != null) {
            queryParameters['_omit'] = requestParameters['omit'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/current_user/`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: CurrentUserToJSON(requestParameters['currentUser']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => CurrentUserFromJSON(jsonValue));
    }

    /**
     * Current User
     * Create
     */
    async authCurrentUserCreate(requestParameters: AuthCurrentUserCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<CurrentUser> {
        const response = await this.authCurrentUserCreateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Current User
     * Delete
     */
    async authCurrentUserDestroyRaw(requestParameters: AuthCurrentUserDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authCurrentUserDestroy().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['expand'] != null) {
            queryParameters['_expand'] = requestParameters['expand'];
        }

        if (requestParameters['fields'] != null) {
            queryParameters['_fields'] = requestParameters['fields'];
        }

        if (requestParameters['omit'] != null) {
            queryParameters['_omit'] = requestParameters['omit'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/current_user/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Current User
     * Delete
     */
    async authCurrentUserDestroy(requestParameters: AuthCurrentUserDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.authCurrentUserDestroyRaw(requestParameters, initOverrides);
    }

    /**
     * Current User
     * Partial Update
     */
    async authCurrentUserPartialUpdateRaw(requestParameters: AuthCurrentUserPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<CurrentUser>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authCurrentUserPartialUpdate().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['expand'] != null) {
            queryParameters['_expand'] = requestParameters['expand'];
        }

        if (requestParameters['fields'] != null) {
            queryParameters['_fields'] = requestParameters['fields'];
        }

        if (requestParameters['omit'] != null) {
            queryParameters['_omit'] = requestParameters['omit'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/current_user/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PATCH',
            headers: headerParameters,
            query: queryParameters,
            body: PatchedCurrentUserToJSON(requestParameters['patchedCurrentUser']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => CurrentUserFromJSON(jsonValue));
    }

    /**
     * Current User
     * Partial Update
     */
    async authCurrentUserPartialUpdate(requestParameters: AuthCurrentUserPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<CurrentUser> {
        const response = await this.authCurrentUserPartialUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Current User
     * Update
     */
    async authCurrentUserUpdateRaw(requestParameters: AuthCurrentUserUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<CurrentUser>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authCurrentUserUpdate().'
            );
        }

        if (requestParameters['currentUser'] == null) {
            throw new runtime.RequiredError(
                'currentUser',
                'Required parameter "currentUser" was null or undefined when calling authCurrentUserUpdate().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['expand'] != null) {
            queryParameters['_expand'] = requestParameters['expand'];
        }

        if (requestParameters['fields'] != null) {
            queryParameters['_fields'] = requestParameters['fields'];
        }

        if (requestParameters['omit'] != null) {
            queryParameters['_omit'] = requestParameters['omit'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/current_user/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: CurrentUserToJSON(requestParameters['currentUser']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => CurrentUserFromJSON(jsonValue));
    }

    /**
     * Current User
     * Update
     */
    async authCurrentUserUpdate(requestParameters: AuthCurrentUserUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<CurrentUser> {
        const response = await this.authCurrentUserUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
