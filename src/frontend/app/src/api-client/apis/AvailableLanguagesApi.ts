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
  Language,
  PaginatedLanguageList,
} from '../models/index';
import {
    LanguageFromJSON,
    LanguageToJSON,
    PaginatedLanguageListFromJSON,
    PaginatedLanguageListToJSON,
} from '../models/index';

export interface CoreLanguagesListRequest {
    expand?: string;
    fields?: string;
    omit?: string;
    page?: number;
    pageSize?: number;
    search?: string;
    sort?: string;
    name?: string;
}

export interface CoreLanguagesRetrieveRequest {
    language: string;
    expand?: string;
    fields?: string;
    omit?: string;
}

/**
 * 
 */
export class AvailableLanguagesApi extends runtime.BaseAPI {

    /**
     * Small view set mixin class that allows unrestricted access to the `list` and `retrieve` actions while deferring permission checks for all other actions to the permission classes of the view set (usually defined in `settings.py`).
     * List
     */
    async coreLanguagesListRaw(requestParameters: CoreLanguagesListRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PaginatedLanguageList>> {
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

        if (requestParameters['name'] != null) {
            queryParameters['name'] = requestParameters['name'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["sessionId"] = await this.configuration.apiKey("sessionId"); // SessionAuthentication authentication
        }

        const response = await this.request({
            path: `/api/core/languages/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PaginatedLanguageListFromJSON(jsonValue));
    }

    /**
     * Small view set mixin class that allows unrestricted access to the `list` and `retrieve` actions while deferring permission checks for all other actions to the permission classes of the view set (usually defined in `settings.py`).
     * List
     */
    async coreLanguagesList(requestParameters: CoreLanguagesListRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PaginatedLanguageList> {
        const response = await this.coreLanguagesListRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Small view set mixin class that allows unrestricted access to the `list` and `retrieve` actions while deferring permission checks for all other actions to the permission classes of the view set (usually defined in `settings.py`).
     * Retrieve
     */
    async coreLanguagesRetrieveRaw(requestParameters: CoreLanguagesRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Language>> {
        if (requestParameters['language'] == null) {
            throw new runtime.RequiredError(
                'language',
                'Required parameter "language" was null or undefined when calling coreLanguagesRetrieve().'
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
            path: `/api/core/languages/{language}/`.replace(`{${"language"}}`, encodeURIComponent(String(requestParameters['language']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => LanguageFromJSON(jsonValue));
    }

    /**
     * Small view set mixin class that allows unrestricted access to the `list` and `retrieve` actions while deferring permission checks for all other actions to the permission classes of the view set (usually defined in `settings.py`).
     * Retrieve
     */
    async coreLanguagesRetrieve(requestParameters: CoreLanguagesRetrieveRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Language> {
        const response = await this.coreLanguagesRetrieveRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
