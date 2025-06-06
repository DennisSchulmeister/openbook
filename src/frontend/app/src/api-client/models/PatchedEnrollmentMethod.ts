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
import type { AccessRequestDurationPeriod } from './AccessRequestDurationPeriod';
import {
    AccessRequestDurationPeriodFromJSON,
    AccessRequestDurationPeriodFromJSONTyped,
    AccessRequestDurationPeriodToJSON,
    AccessRequestDurationPeriodToJSONTyped,
} from './AccessRequestDurationPeriod';

/**
 * Enrollment Method
 * @export
 * @interface PatchedEnrollmentMethod
 */
export interface PatchedEnrollmentMethod {
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    readonly id?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    scopeType?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    scopeUuid?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    name?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    description?: string;
    /**
     * 
     * @type {TextFormatEnum}
     * @memberof PatchedEnrollmentMethod
     */
    textFormat?: TextFormatEnum;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    role?: string;
    /**
     * 
     * @type {Date}
     * @memberof PatchedEnrollmentMethod
     */
    endDate?: Date | null;
    /**
     * 
     * @type {AccessRequestDurationPeriod}
     * @memberof PatchedEnrollmentMethod
     */
    durationPeriod?: AccessRequestDurationPeriod;
    /**
     * 
     * @type {number}
     * @memberof PatchedEnrollmentMethod
     */
    durationValue?: number;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    passphrase?: string;
    /**
     * 
     * @type {boolean}
     * @memberof PatchedEnrollmentMethod
     */
    isActive?: boolean;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    readonly createdBy?: string;
    /**
     * 
     * @type {Date}
     * @memberof PatchedEnrollmentMethod
     */
    readonly createdAt?: Date | null;
    /**
     * 
     * @type {string}
     * @memberof PatchedEnrollmentMethod
     */
    readonly modifiedBy?: string;
    /**
     * 
     * @type {Date}
     * @memberof PatchedEnrollmentMethod
     */
    readonly modifiedAt?: Date | null;
}



/**
 * Check if a given object implements the PatchedEnrollmentMethod interface.
 */
export function instanceOfPatchedEnrollmentMethod(value: object): value is PatchedEnrollmentMethod {
    return true;
}

export function PatchedEnrollmentMethodFromJSON(json: any): PatchedEnrollmentMethod {
    return PatchedEnrollmentMethodFromJSONTyped(json, false);
}

export function PatchedEnrollmentMethodFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedEnrollmentMethod {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'scopeType': json['scope_type'] == null ? undefined : json['scope_type'],
        'scopeUuid': json['scope_uuid'] == null ? undefined : json['scope_uuid'],
        'name': json['name'] == null ? undefined : json['name'],
        'description': json['description'] == null ? undefined : json['description'],
        'textFormat': json['text_format'] == null ? undefined : TextFormatEnumFromJSON(json['text_format']),
        'role': json['role'] == null ? undefined : json['role'],
        'endDate': json['end_date'] == null ? undefined : (new Date(json['end_date'])),
        'durationPeriod': json['duration_period'] == null ? undefined : AccessRequestDurationPeriodFromJSON(json['duration_period']),
        'durationValue': json['duration_value'] == null ? undefined : json['duration_value'],
        'passphrase': json['passphrase'] == null ? undefined : json['passphrase'],
        'isActive': json['is_active'] == null ? undefined : json['is_active'],
        'createdBy': json['created_by'] == null ? undefined : json['created_by'],
        'createdAt': json['created_at'] == null ? undefined : (new Date(json['created_at'])),
        'modifiedBy': json['modified_by'] == null ? undefined : json['modified_by'],
        'modifiedAt': json['modified_at'] == null ? undefined : (new Date(json['modified_at'])),
    };
}

export function PatchedEnrollmentMethodToJSON(json: any): PatchedEnrollmentMethod {
    return PatchedEnrollmentMethodToJSONTyped(json, false);
}

export function PatchedEnrollmentMethodToJSONTyped(value?: Omit<PatchedEnrollmentMethod, 'id'|'created_by'|'created_at'|'modified_by'|'modified_at'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'scope_type': value['scopeType'],
        'scope_uuid': value['scopeUuid'],
        'name': value['name'],
        'description': value['description'],
        'text_format': TextFormatEnumToJSON(value['textFormat']),
        'role': value['role'],
        'end_date': value['endDate'] == null ? undefined : ((value['endDate'] as any).toISOString()),
        'duration_period': AccessRequestDurationPeriodToJSON(value['durationPeriod']),
        'duration_value': value['durationValue'],
        'passphrase': value['passphrase'],
        'is_active': value['isActive'],
    };
}

