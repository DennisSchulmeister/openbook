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
/**
 * 
 * @export
 * @interface ScopeTypeList
 */
export interface ScopeTypeList {
    /**
     * 
     * @type {number}
     * @memberof ScopeTypeList
     */
    pk: number;
    /**
     * 
     * @type {string}
     * @memberof ScopeTypeList
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof ScopeTypeList
     */
    label: string;
}

/**
 * Check if a given object implements the ScopeTypeList interface.
 */
export function instanceOfScopeTypeList(value: object): value is ScopeTypeList {
    if (!('pk' in value) || value['pk'] === undefined) return false;
    if (!('id' in value) || value['id'] === undefined) return false;
    if (!('label' in value) || value['label'] === undefined) return false;
    return true;
}

export function ScopeTypeListFromJSON(json: any): ScopeTypeList {
    return ScopeTypeListFromJSONTyped(json, false);
}

export function ScopeTypeListFromJSONTyped(json: any, ignoreDiscriminator: boolean): ScopeTypeList {
    if (json == null) {
        return json;
    }
    return {
        
        'pk': json['pk'],
        'id': json['id'],
        'label': json['label'],
    };
}

export function ScopeTypeListToJSON(json: any): ScopeTypeList {
    return ScopeTypeListToJSONTyped(json, false);
}

export function ScopeTypeListToJSONTyped(value?: ScopeTypeList | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'pk': value['pk'],
        'id': value['id'],
        'label': value['label'],
    };
}

