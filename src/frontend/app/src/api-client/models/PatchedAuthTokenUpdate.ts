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
import type { TextFormatEnum } from './TextFormatEnum';
import {
    TextFormatEnumFromJSON,
    TextFormatEnumFromJSONTyped,
    TextFormatEnumToJSON,
    TextFormatEnumToJSONTyped,
} from './TextFormatEnum';

/**
 * Authentication Token
 * @export
 * @interface PatchedAuthTokenUpdate
 */
export interface PatchedAuthTokenUpdate {
    /**
     * 
     * @type {string}
     * @memberof PatchedAuthTokenUpdate
     */
    readonly id?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedAuthTokenUpdate
     */
    readonly user?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedAuthTokenUpdate
     */
    name?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedAuthTokenUpdate
     */
    description?: string;
    /**
     * 
     * @type {TextFormatEnum}
     * @memberof PatchedAuthTokenUpdate
     */
    textFormat?: TextFormatEnum;
    /**
     * 
     * @type {boolean}
     * @memberof PatchedAuthTokenUpdate
     */
    isActive?: boolean;
    /**
     * 
     * @type {Date}
     * @memberof PatchedAuthTokenUpdate
     */
    startDate?: Date | null;
    /**
     * 
     * @type {Date}
     * @memberof PatchedAuthTokenUpdate
     */
    endDate?: Date | null;
}



/**
 * Check if a given object implements the PatchedAuthTokenUpdate interface.
 */
export function instanceOfPatchedAuthTokenUpdate(value: object): value is PatchedAuthTokenUpdate {
    return true;
}

export function PatchedAuthTokenUpdateFromJSON(json: any): PatchedAuthTokenUpdate {
    return PatchedAuthTokenUpdateFromJSONTyped(json, false);
}

export function PatchedAuthTokenUpdateFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedAuthTokenUpdate {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'user': json['user'] == null ? undefined : json['user'],
        'name': json['name'] == null ? undefined : json['name'],
        'description': json['description'] == null ? undefined : json['description'],
        'textFormat': json['text_format'] == null ? undefined : TextFormatEnumFromJSON(json['text_format']),
        'isActive': json['is_active'] == null ? undefined : json['is_active'],
        'startDate': json['start_date'] == null ? undefined : (new Date(json['start_date'])),
        'endDate': json['end_date'] == null ? undefined : (new Date(json['end_date'])),
    };
}

export function PatchedAuthTokenUpdateToJSON(json: any): PatchedAuthTokenUpdate {
    return PatchedAuthTokenUpdateToJSONTyped(json, false);
}

export function PatchedAuthTokenUpdateToJSONTyped(value?: Omit<PatchedAuthTokenUpdate, 'id'|'user'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'name': value['name'],
        'description': value['description'],
        'text_format': TextFormatEnumToJSON(value['textFormat']),
        'is_active': value['isActive'],
        'start_date': value['startDate'] == null ? undefined : ((value['startDate'] as any).toISOString()),
        'end_date': value['endDate'] == null ? undefined : ((value['endDate'] as any).toISOString()),
    };
}

