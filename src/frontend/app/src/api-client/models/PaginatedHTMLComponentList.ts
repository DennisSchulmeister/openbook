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
import type { HTMLComponent } from './HTMLComponent';
import {
    HTMLComponentFromJSON,
    HTMLComponentFromJSONTyped,
    HTMLComponentToJSON,
    HTMLComponentToJSONTyped,
} from './HTMLComponent';

/**
 * 
 * @export
 * @interface PaginatedHTMLComponentList
 */
export interface PaginatedHTMLComponentList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedHTMLComponentList
     */
    count: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedHTMLComponentList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedHTMLComponentList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<HTMLComponent>}
     * @memberof PaginatedHTMLComponentList
     */
    results: Array<HTMLComponent>;
}

/**
 * Check if a given object implements the PaginatedHTMLComponentList interface.
 */
export function instanceOfPaginatedHTMLComponentList(value: object): value is PaginatedHTMLComponentList {
    if (!('count' in value) || value['count'] === undefined) return false;
    if (!('results' in value) || value['results'] === undefined) return false;
    return true;
}

export function PaginatedHTMLComponentListFromJSON(json: any): PaginatedHTMLComponentList {
    return PaginatedHTMLComponentListFromJSONTyped(json, false);
}

export function PaginatedHTMLComponentListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedHTMLComponentList {
    if (json == null) {
        return json;
    }
    return {
        
        'count': json['count'],
        'next': json['next'] == null ? undefined : json['next'],
        'previous': json['previous'] == null ? undefined : json['previous'],
        'results': ((json['results'] as Array<any>).map(HTMLComponentFromJSON)),
    };
}

export function PaginatedHTMLComponentListToJSON(json: any): PaginatedHTMLComponentList {
    return PaginatedHTMLComponentListToJSONTyped(json, false);
}

export function PaginatedHTMLComponentListToJSONTyped(value?: PaginatedHTMLComponentList | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'count': value['count'],
        'next': value['next'],
        'previous': value['previous'],
        'results': ((value['results'] as Array<any>).map(HTMLComponentToJSON)),
    };
}

