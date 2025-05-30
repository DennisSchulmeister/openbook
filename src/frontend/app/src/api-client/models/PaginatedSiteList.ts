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

import { mapValues } from '../runtime';
import type { Site } from './Site';
import {
    SiteFromJSON,
    SiteFromJSONTyped,
    SiteToJSON,
    SiteToJSONTyped,
} from './Site';

/**
 * 
 * @export
 * @interface PaginatedSiteList
 */
export interface PaginatedSiteList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedSiteList
     */
    count: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedSiteList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedSiteList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<Site>}
     * @memberof PaginatedSiteList
     */
    results: Array<Site>;
}

/**
 * Check if a given object implements the PaginatedSiteList interface.
 */
export function instanceOfPaginatedSiteList(value: object): value is PaginatedSiteList {
    if (!('count' in value) || value['count'] === undefined) return false;
    if (!('results' in value) || value['results'] === undefined) return false;
    return true;
}

export function PaginatedSiteListFromJSON(json: any): PaginatedSiteList {
    return PaginatedSiteListFromJSONTyped(json, false);
}

export function PaginatedSiteListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedSiteList {
    if (json == null) {
        return json;
    }
    return {
        
        'count': json['count'],
        'next': json['next'] == null ? undefined : json['next'],
        'previous': json['previous'] == null ? undefined : json['previous'],
        'results': ((json['results'] as Array<any>).map(SiteFromJSON)),
    };
}

export function PaginatedSiteListToJSON(json: any): PaginatedSiteList {
    return PaginatedSiteListToJSONTyped(json, false);
}

export function PaginatedSiteListToJSONTyped(value?: PaginatedSiteList | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'count': value['count'],
        'next': value['next'],
        'previous': value['previous'],
        'results': ((value['results'] as Array<any>).map(SiteToJSON)),
    };
}

