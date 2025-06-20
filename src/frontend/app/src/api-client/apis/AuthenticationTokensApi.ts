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
  AuthToken,
  AuthTokenUpdate,
  PaginatedAuthTokenList,
  PatchedAuthTokenUpdate,
} from '../models/index';
import {
    AuthTokenFromJSON,
    AuthTokenToJSON,
    AuthTokenUpdateFromJSON,
    AuthTokenUpdateToJSON,
    PaginatedAuthTokenListFromJSON,
    PaginatedAuthTokenListToJSON,
    PatchedAuthTokenUpdateFromJSON,
    PatchedAuthTokenUpdateToJSON,
} from '../models/index';

export interface AuthAuthTokensCreateRequest {
    authToken: Omit<AuthToken, 'id'|'token'|'created_by'|'created_at'|'modified_by'|'modified_at'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthAuthTokensDestroyRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthAuthTokensListRequest {
    expand?: string;
    fields?: string;
    omit?: string;
    page?: number;
    pageSize?: number;
    search?: string;
    sort?: string;
    createdAt?: Date;
    createdAtGte?: Date;
    createdAtLte?: Date;
    createdBy?: string;
    endDate?: Date;
    endDateGte?: Date;
    endDateLte?: Date;
    isActive?: boolean;
    modifiedAt?: Date;
    modifiedAtGte?: Date;
    modifiedAtLte?: Date;
    modifiedBy?: string;
    startDate?: Date;
    startDateGte?: Date;
    startDateLte?: Date;
    user?: string;
}

export interface AuthAuthTokensPartialUpdateRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
    patchedAuthTokenUpdate?: Omit<PatchedAuthTokenUpdate, 'id'|'user'>;
}

export interface AuthAuthTokensRetrieveRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthAuthTokensUpdateRequest {
    id: string;
    authTokenUpdate: Omit<AuthTokenUpdate, 'id'|'user'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

/**
 * 
 */
export class AuthenticationTokensApi extends runtime.BaseAPI {

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Create
     */
    async authAuthTokensCreateRaw(requestParameters: AuthAuthTokensCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<AuthToken>> {
        if (requestParameters['authToken'] == null) {
            throw new runtime.RequiredError(
                'authToken',
                'Required parameter "authToken" was null or undefined when calling authAuthTokensCreate().'
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
            path: `/api/auth/auth_tokens/`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: AuthTokenToJSON(requestParameters['authToken']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => AuthTokenFromJSON(jsonValue));
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Create
     */
    async authAuthTokensCreate(requestParameters: AuthAuthTokensCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<AuthToken> {
        const response = await this.authAuthTokensCreateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Delete
     */
    async authAuthTokensDestroyRaw(requestParameters: AuthAuthTokensDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authAuthTokensDestroy().'
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
            path: `/api/auth/auth_tokens/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Delete
     */
    async authAuthTokensDestroy(requestParameters: AuthAuthTokensDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.authAuthTokensDestroyRaw(requestParameters, initOverrides);
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * List
     */
    async authAuthTokensListRaw(requestParameters: AuthAuthTokensListRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PaginatedAuthTokenList>> {
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

        if (requestParameters['createdAt'] != null) {
            queryParameters['created_at'] = (requestParameters['createdAt'] as any).toISOString();
        }

        if (requestParameters['createdAtGte'] != null) {
            queryParameters['created_at__gte'] = (requestParameters['createdAtGte'] as any).toISOString();
        }

        if (requestParameters['createdAtLte'] != null) {
            queryParameters['created_at__lte'] = (requestParameters['createdAtLte'] as any).toISOString();
        }

        if (requestParameters['createdBy'] != null) {
            queryParameters['created_by'] = requestParameters['createdBy'];
        }

        if (requestParameters['endDate'] != null) {
            queryParameters['end_date'] = (requestParameters['endDate'] as any).toISOString();
        }

        if (requestParameters['endDateGte'] != null) {
            queryParameters['end_date__gte'] = (requestParameters['endDateGte'] as any).toISOString();
        }

        if (requestParameters['endDateLte'] != null) {
            queryParameters['end_date__lte'] = (requestParameters['endDateLte'] as any).toISOString();
        }

        if (requestParameters['isActive'] != null) {
            queryParameters['is_active'] = requestParameters['isActive'];
        }

        if (requestParameters['modifiedAt'] != null) {
            queryParameters['modified_at'] = (requestParameters['modifiedAt'] as any).toISOString();
        }

        if (requestParameters['modifiedAtGte'] != null) {
            queryParameters['modified_at__gte'] = (requestParameters['modifiedAtGte'] as any).toISOString();
        }

        if (requestParameters['modifiedAtLte'] != null) {
            queryParameters['modified_at__lte'] = (requestParameters['modifiedAtLte'] as any).toISOString();
        }

        if (requestParameters['modifiedBy'] != null) {
            queryParameters['modified_by'] = requestParameters['modifiedBy'];
        }

        if (requestParameters['startDate'] != null) {
            queryParameters['start_date'] = (requestParameters['startDate'] as any).toISOString();
        }

        if (requestParameters['startDateGte'] != null) {
            queryParameters['start_date__gte'] = (requestParameters['startDateGte'] as any).toISOString();
        }

        if (requestParameters['startDateLte'] != null) {
            queryParameters['start_date__lte'] = (requestParameters['startDateLte'] as any).toISOString();
        }

        if (requestParameters['user'] != null) {
            queryParameters['user'] = requestParameters['user'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/auth_tokens/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PaginatedAuthTokenListFromJSON(jsonValue));
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * List
     */
    async authAuthTokensList(requestParameters: AuthAuthTokensListRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PaginatedAuthTokenList> {
        const response = await this.authAuthTokensListRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Partial Update
     */
    async authAuthTokensPartialUpdateRaw(requestParameters: AuthAuthTokensPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<AuthTokenUpdate>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authAuthTokensPartialUpdate().'
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
            path: `/api/auth/auth_tokens/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PATCH',
            headers: headerParameters,
            query: queryParameters,
            body: PatchedAuthTokenUpdateToJSON(requestParameters['patchedAuthTokenUpdate']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => AuthTokenUpdateFromJSON(jsonValue));
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Partial Update
     */
    async authAuthTokensPartialUpdate(requestParameters: AuthAuthTokensPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<AuthTokenUpdate> {
        const response = await this.authAuthTokensPartialUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Retrieve
     */
    async authAuthTokensRetrieveRaw(requestParameters: AuthAuthTokensRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<AuthToken>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authAuthTokensRetrieve().'
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
            path: `/api/auth/auth_tokens/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => AuthTokenFromJSON(jsonValue));
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Retrieve
     */
    async authAuthTokensRetrieve(requestParameters: AuthAuthTokensRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<AuthToken> {
        const response = await this.authAuthTokensRetrieveRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Update
     */
    async authAuthTokensUpdateRaw(requestParameters: AuthAuthTokensUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<AuthTokenUpdate>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authAuthTokensUpdate().'
            );
        }

        if (requestParameters['authTokenUpdate'] == null) {
            throw new runtime.RequiredError(
                'authTokenUpdate',
                'Required parameter "authTokenUpdate" was null or undefined when calling authAuthTokensUpdate().'
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
            path: `/api/auth/auth_tokens/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: AuthTokenUpdateToJSON(requestParameters['authTokenUpdate']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => AuthTokenUpdateFromJSON(jsonValue));
    }

    /**
     * Authentication tokens provide an authentication mechanism for remote clients without giving them a username and password. This allows human users to grant access (in their name) to other apps, though the apps then impersonate these human users. Thus, more importantly this allows to create special technical app users for which the access token is the only allowed authentication mechanism.
     * Update
     */
    async authAuthTokensUpdate(requestParameters: AuthAuthTokensUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<AuthTokenUpdate> {
        const response = await this.authAuthTokensUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
