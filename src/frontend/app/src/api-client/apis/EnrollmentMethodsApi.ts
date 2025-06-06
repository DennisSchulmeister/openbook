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
  EnrollActionRequest,
  EnrollmentMethod,
  PaginatedEnrollmentMethodList,
  PatchedEnrollmentMethod,
  RoleAssignment,
} from '../models/index';
import {
    EnrollActionRequestFromJSON,
    EnrollActionRequestToJSON,
    EnrollmentMethodFromJSON,
    EnrollmentMethodToJSON,
    PaginatedEnrollmentMethodListFromJSON,
    PaginatedEnrollmentMethodListToJSON,
    PatchedEnrollmentMethodFromJSON,
    PatchedEnrollmentMethodToJSON,
    RoleAssignmentFromJSON,
    RoleAssignmentToJSON,
} from '../models/index';

export interface AuthEnrollmentMethodEnrollRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
    enrollActionRequest?: EnrollActionRequest;
}

export interface AuthEnrollmentMethodsCreateRequest {
    enrollmentMethod: Omit<EnrollmentMethod, 'id'|'created_by'|'created_at'|'modified_by'|'modified_at'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthEnrollmentMethodsDestroyRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthEnrollmentMethodsListRequest {
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
    isActive?: boolean;
    modifiedAt?: Date;
    modifiedAtGte?: Date;
    modifiedAtLte?: Date;
    modifiedBy?: string;
    name?: string;
    role?: string;
    scopeType?: number;
    scopeUuid?: string;
}

export interface AuthEnrollmentMethodsPartialUpdateRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
    patchedEnrollmentMethod?: Omit<PatchedEnrollmentMethod, 'id'|'created_by'|'created_at'|'modified_by'|'modified_at'>;
}

export interface AuthEnrollmentMethodsRetrieveRequest {
    id: string;
    expand?: string;
    fields?: string;
    omit?: string;
}

export interface AuthEnrollmentMethodsUpdateRequest {
    id: string;
    enrollmentMethod: Omit<EnrollmentMethod, 'id'|'created_by'|'created_at'|'modified_by'|'modified_at'>;
    expand?: string;
    fields?: string;
    omit?: string;
}

/**
 * 
 */
export class EnrollmentMethodsApi extends runtime.BaseAPI {

    /**
     * Self-enrollment of the current user via given enrollment method.
     * Enroll User
     */
    async authEnrollmentMethodEnrollRaw(requestParameters: AuthEnrollmentMethodEnrollRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<RoleAssignment>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authEnrollmentMethodEnroll().'
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
            path: `/api/auth/enrollment_methods/{id}/enroll/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: EnrollActionRequestToJSON(requestParameters['enrollActionRequest']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => RoleAssignmentFromJSON(jsonValue));
    }

    /**
     * Self-enrollment of the current user via given enrollment method.
     * Enroll User
     */
    async authEnrollmentMethodEnroll(requestParameters: AuthEnrollmentMethodEnrollRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<RoleAssignment> {
        const response = await this.authEnrollmentMethodEnrollRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Enrollment methods for self-registration
     * Create
     */
    async authEnrollmentMethodsCreateRaw(requestParameters: AuthEnrollmentMethodsCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<EnrollmentMethod>> {
        if (requestParameters['enrollmentMethod'] == null) {
            throw new runtime.RequiredError(
                'enrollmentMethod',
                'Required parameter "enrollmentMethod" was null or undefined when calling authEnrollmentMethodsCreate().'
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
            path: `/api/auth/enrollment_methods/`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: EnrollmentMethodToJSON(requestParameters['enrollmentMethod']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => EnrollmentMethodFromJSON(jsonValue));
    }

    /**
     * Enrollment methods for self-registration
     * Create
     */
    async authEnrollmentMethodsCreate(requestParameters: AuthEnrollmentMethodsCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<EnrollmentMethod> {
        const response = await this.authEnrollmentMethodsCreateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Enrollment methods for self-registration
     * Delete
     */
    async authEnrollmentMethodsDestroyRaw(requestParameters: AuthEnrollmentMethodsDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authEnrollmentMethodsDestroy().'
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
            path: `/api/auth/enrollment_methods/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Enrollment methods for self-registration
     * Delete
     */
    async authEnrollmentMethodsDestroy(requestParameters: AuthEnrollmentMethodsDestroyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.authEnrollmentMethodsDestroyRaw(requestParameters, initOverrides);
    }

    /**
     * Enrollment methods for self-registration
     * List
     */
    async authEnrollmentMethodsListRaw(requestParameters: AuthEnrollmentMethodsListRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PaginatedEnrollmentMethodList>> {
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

        if (requestParameters['name'] != null) {
            queryParameters['name'] = requestParameters['name'];
        }

        if (requestParameters['role'] != null) {
            queryParameters['role'] = requestParameters['role'];
        }

        if (requestParameters['scopeType'] != null) {
            queryParameters['scope_type'] = requestParameters['scopeType'];
        }

        if (requestParameters['scopeUuid'] != null) {
            queryParameters['scope_uuid'] = requestParameters['scopeUuid'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/auth/enrollment_methods/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PaginatedEnrollmentMethodListFromJSON(jsonValue));
    }

    /**
     * Enrollment methods for self-registration
     * List
     */
    async authEnrollmentMethodsList(requestParameters: AuthEnrollmentMethodsListRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PaginatedEnrollmentMethodList> {
        const response = await this.authEnrollmentMethodsListRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Enrollment methods for self-registration
     * Partial Update
     */
    async authEnrollmentMethodsPartialUpdateRaw(requestParameters: AuthEnrollmentMethodsPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<EnrollmentMethod>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authEnrollmentMethodsPartialUpdate().'
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
            path: `/api/auth/enrollment_methods/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PATCH',
            headers: headerParameters,
            query: queryParameters,
            body: PatchedEnrollmentMethodToJSON(requestParameters['patchedEnrollmentMethod']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => EnrollmentMethodFromJSON(jsonValue));
    }

    /**
     * Enrollment methods for self-registration
     * Partial Update
     */
    async authEnrollmentMethodsPartialUpdate(requestParameters: AuthEnrollmentMethodsPartialUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<EnrollmentMethod> {
        const response = await this.authEnrollmentMethodsPartialUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Enrollment methods for self-registration
     * Retrieve
     */
    async authEnrollmentMethodsRetrieveRaw(requestParameters: AuthEnrollmentMethodsRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<EnrollmentMethod>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authEnrollmentMethodsRetrieve().'
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
            path: `/api/auth/enrollment_methods/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => EnrollmentMethodFromJSON(jsonValue));
    }

    /**
     * Enrollment methods for self-registration
     * Retrieve
     */
    async authEnrollmentMethodsRetrieve(requestParameters: AuthEnrollmentMethodsRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<EnrollmentMethod> {
        const response = await this.authEnrollmentMethodsRetrieveRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Enrollment methods for self-registration
     * Update
     */
    async authEnrollmentMethodsUpdateRaw(requestParameters: AuthEnrollmentMethodsUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<EnrollmentMethod>> {
        if (requestParameters['id'] == null) {
            throw new runtime.RequiredError(
                'id',
                'Required parameter "id" was null or undefined when calling authEnrollmentMethodsUpdate().'
            );
        }

        if (requestParameters['enrollmentMethod'] == null) {
            throw new runtime.RequiredError(
                'enrollmentMethod',
                'Required parameter "enrollmentMethod" was null or undefined when calling authEnrollmentMethodsUpdate().'
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
            path: `/api/auth/enrollment_methods/{id}/`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters['id']))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: EnrollmentMethodToJSON(requestParameters['enrollmentMethod']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => EnrollmentMethodFromJSON(jsonValue));
    }

    /**
     * Enrollment methods for self-registration
     * Update
     */
    async authEnrollmentMethodsUpdate(requestParameters: AuthEnrollmentMethodsUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<EnrollmentMethod> {
        const response = await this.authEnrollmentMethodsUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
