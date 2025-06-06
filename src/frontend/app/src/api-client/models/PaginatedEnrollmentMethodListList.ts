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
import type { EnrollmentMethodList } from './EnrollmentMethodList';
import {
    EnrollmentMethodListFromJSON,
    EnrollmentMethodListFromJSONTyped,
    EnrollmentMethodListToJSON,
    EnrollmentMethodListToJSONTyped,
} from './EnrollmentMethodList';

/**
 * 
 * @export
 * @interface PaginatedEnrollmentMethodListList
 */
export interface PaginatedEnrollmentMethodListList {
    /**
     * 
     * @type {number}
     * @memberof PaginatedEnrollmentMethodListList
     */
    count: number;
    /**
     * 
     * @type {string}
     * @memberof PaginatedEnrollmentMethodListList
     */
    next?: string | null;
    /**
     * 
     * @type {string}
     * @memberof PaginatedEnrollmentMethodListList
     */
    previous?: string | null;
    /**
     * 
     * @type {Array<EnrollmentMethodList>}
     * @memberof PaginatedEnrollmentMethodListList
     */
    results: Array<EnrollmentMethodList>;
}

/**
 * Check if a given object implements the PaginatedEnrollmentMethodListList interface.
 */
export function instanceOfPaginatedEnrollmentMethodListList(value: object): value is PaginatedEnrollmentMethodListList {
    if (!('count' in value) || value['count'] === undefined) return false;
    if (!('results' in value) || value['results'] === undefined) return false;
    return true;
}

export function PaginatedEnrollmentMethodListListFromJSON(json: any): PaginatedEnrollmentMethodListList {
    return PaginatedEnrollmentMethodListListFromJSONTyped(json, false);
}

export function PaginatedEnrollmentMethodListListFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedEnrollmentMethodListList {
    if (json == null) {
        return json;
    }
    return {
        
        'count': json['count'],
        'next': json['next'] == null ? undefined : json['next'],
        'previous': json['previous'] == null ? undefined : json['previous'],
        'results': ((json['results'] as Array<any>).map(EnrollmentMethodListFromJSON)),
    };
}

export function PaginatedEnrollmentMethodListListToJSON(json: any): PaginatedEnrollmentMethodListList {
    return PaginatedEnrollmentMethodListListToJSONTyped(json, false);
}

export function PaginatedEnrollmentMethodListListToJSONTyped(value?: PaginatedEnrollmentMethodListList | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'count': value['count'],
        'next': value['next'],
        'previous': value['previous'],
        'results': ((value['results'] as Array<any>).map(EnrollmentMethodListToJSON)),
    };
}

