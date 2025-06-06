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
import type { UserRead } from './UserRead';
import {
    UserReadFromJSON,
    UserReadFromJSONTyped,
    UserReadToJSON,
    UserReadToJSONTyped,
} from './UserRead';

/**
 * 
 * @export
 * @interface PaginatedUserReadList
 */
export interface PaginatedUserReadList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedUserReadList
     */
    count: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedUserReadList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedUserReadList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<UserRead>}
     * @memberof PaginatedUserReadList
     */
    results: Array<UserRead>;
}

/**
 * Check if a given object implements the PaginatedUserReadList interface.
 */
export function instanceOfPaginatedUserReadList(value: object): value is PaginatedUserReadList {
    if (!('count' in value) || value['count'] === undefined) return false;
    if (!('results' in value) || value['results'] === undefined) return false;
    return true;
}

export function PaginatedUserReadListFromJSON(json: any): PaginatedUserReadList {
    return PaginatedUserReadListFromJSONTyped(json, false);
}

export function PaginatedUserReadListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedUserReadList {
    if (json == null) {
        return json;
    }
    return {
        
        'count': json['count'],
        'next': json['next'] == null ? undefined : json['next'],
        'previous': json['previous'] == null ? undefined : json['previous'],
        'results': ((json['results'] as Array<any>).map(UserReadFromJSON)),
    };
}

export function PaginatedUserReadListToJSON(json: any): PaginatedUserReadList {
    return PaginatedUserReadListToJSONTyped(json, false);
}

export function PaginatedUserReadListToJSONTyped(value?: PaginatedUserReadList | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'count': value['count'],
        'next': value['next'],
        'previous': value['previous'],
        'results': ((value['results'] as Array<any>).map(UserReadToJSON)),
    };
}

