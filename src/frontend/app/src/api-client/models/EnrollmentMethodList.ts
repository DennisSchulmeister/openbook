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
import type { RoleRead } from './RoleRead';
import {
    RoleReadFromJSON,
    RoleReadFromJSONTyped,
    RoleReadToJSON,
    RoleReadToJSONTyped,
} from './RoleRead';

/**
 * Reduced list of fields for getting a list of enrollment methods.
 * @export
 * @interface EnrollmentMethodList
 */
export interface EnrollmentMethodList {
    /**
     * 
     * @type {string}
     * @memberof EnrollmentMethodList
     */
    readonly id: string;
    /**
     * 
     * @type {string}
     * @memberof EnrollmentMethodList
     */
    scopeType: string;
    /**
     * 
     * @type {string}
     * @memberof EnrollmentMethodList
     */
    readonly scopeUuid: string;
    /**
     * 
     * @type {RoleRead}
     * @memberof EnrollmentMethodList
     */
    readonly role: RoleRead;
    /**
     * 
     * @type {string}
     * @memberof EnrollmentMethodList
     */
    readonly name: string;
    /**
     * 
     * @type {boolean}
     * @memberof EnrollmentMethodList
     */
    readonly isActive: boolean;
    /**
     * 
     * @type {UserRead}
     * @memberof EnrollmentMethodList
     */
    readonly createdBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof EnrollmentMethodList
     */
    readonly createdAt: Date | null;
    /**
     * 
     * @type {UserRead}
     * @memberof EnrollmentMethodList
     */
    readonly modifiedBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof EnrollmentMethodList
     */
    readonly modifiedAt: Date | null;
}

/**
 * Check if a given object implements the EnrollmentMethodList interface.
 */
export function instanceOfEnrollmentMethodList(value: object): value is EnrollmentMethodList {
    if (!('id' in value) || value['id'] === undefined) return false;
    if (!('scopeType' in value) || value['scopeType'] === undefined) return false;
    if (!('scopeUuid' in value) || value['scopeUuid'] === undefined) return false;
    if (!('role' in value) || value['role'] === undefined) return false;
    if (!('name' in value) || value['name'] === undefined) return false;
    if (!('isActive' in value) || value['isActive'] === undefined) return false;
    if (!('createdBy' in value) || value['createdBy'] === undefined) return false;
    if (!('createdAt' in value) || value['createdAt'] === undefined) return false;
    if (!('modifiedBy' in value) || value['modifiedBy'] === undefined) return false;
    if (!('modifiedAt' in value) || value['modifiedAt'] === undefined) return false;
    return true;
}

export function EnrollmentMethodListFromJSON(json: any): EnrollmentMethodList {
    return EnrollmentMethodListFromJSONTyped(json, false);
}

export function EnrollmentMethodListFromJSONTyped(json: any, ignoreDiscriminator: boolean): EnrollmentMethodList {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'],
        'scopeType': json['scope_type'],
        'scopeUuid': json['scope_uuid'],
        'role': RoleReadFromJSON(json['role']),
        'name': json['name'],
        'isActive': json['is_active'],
        'createdBy': UserReadFromJSON(json['created_by']),
        'createdAt': (json['created_at'] == null ? null : new Date(json['created_at'])),
        'modifiedBy': UserReadFromJSON(json['modified_by']),
        'modifiedAt': (json['modified_at'] == null ? null : new Date(json['modified_at'])),
    };
}

export function EnrollmentMethodListToJSON(json: any): EnrollmentMethodList {
    return EnrollmentMethodListToJSONTyped(json, false);
}

export function EnrollmentMethodListToJSONTyped(value?: Omit<EnrollmentMethodList, 'id'|'scope_uuid'|'role'|'name'|'is_active'|'created_by'|'created_at'|'modified_by'|'modified_at'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'scope_type': value['scopeType'],
    };
}

