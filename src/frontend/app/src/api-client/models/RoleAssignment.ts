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
import type { AccessRequestWithoutRoleRead } from './AccessRequestWithoutRoleRead';
import {
    AccessRequestWithoutRoleReadFromJSON,
    AccessRequestWithoutRoleReadFromJSONTyped,
    AccessRequestWithoutRoleReadToJSON,
    AccessRequestWithoutRoleReadToJSONTyped,
} from './AccessRequestWithoutRoleRead';
import type { UserRead } from './UserRead';
import {
    UserReadFromJSON,
    UserReadFromJSONTyped,
    UserReadToJSON,
    UserReadToJSONTyped,
} from './UserRead';
import type { EnrollmentMethodWithoutRoleRead } from './EnrollmentMethodWithoutRoleRead';
import {
    EnrollmentMethodWithoutRoleReadFromJSON,
    EnrollmentMethodWithoutRoleReadFromJSONTyped,
    EnrollmentMethodWithoutRoleReadToJSON,
    EnrollmentMethodWithoutRoleReadToJSONTyped,
} from './EnrollmentMethodWithoutRoleRead';
import type { AssignmentMethodEnum } from './AssignmentMethodEnum';
import {
    AssignmentMethodEnumFromJSON,
    AssignmentMethodEnumFromJSONTyped,
    AssignmentMethodEnumToJSON,
    AssignmentMethodEnumToJSONTyped,
} from './AssignmentMethodEnum';
import type { RoleRead } from './RoleRead';
import {
    RoleReadFromJSON,
    RoleReadFromJSONTyped,
    RoleReadToJSON,
    RoleReadToJSONTyped,
} from './RoleRead';

/**
 * Full list of fields for retrieving a single role assignment.
 * @export
 * @interface RoleAssignment
 */
export interface RoleAssignment {
    /**
     * 
     * @type {string}
     * @memberof RoleAssignment
     */
    readonly id: string;
    /**
     * 
     * @type {string}
     * @memberof RoleAssignment
     */
    scopeType: string;
    /**
     * 
     * @type {string}
     * @memberof RoleAssignment
     */
    scopeUuid: string;
    /**
     * 
     * @type {RoleRead}
     * @memberof RoleAssignment
     */
    readonly role: RoleRead;
    /**
     * 
     * @type {string}
     * @memberof RoleAssignment
     */
    roleSlug: string;
    /**
     * 
     * @type {UserRead}
     * @memberof RoleAssignment
     */
    readonly user: UserRead;
    /**
     * User name
     * @type {string}
     * @memberof RoleAssignment
     */
    userUsername: string;
    /**
     * 
     * @type {AssignmentMethodEnum}
     * @memberof RoleAssignment
     */
    readonly assignmentMethod: AssignmentMethodEnum;
    /**
     * 
     * @type {EnrollmentMethodWithoutRoleRead}
     * @memberof RoleAssignment
     */
    readonly enrollmentMethod: EnrollmentMethodWithoutRoleRead;
    /**
     * 
     * @type {AccessRequestWithoutRoleRead}
     * @memberof RoleAssignment
     */
    readonly accessRequest: AccessRequestWithoutRoleRead;
    /**
     * 
     * @type {boolean}
     * @memberof RoleAssignment
     */
    isActive?: boolean;
    /**
     * 
     * @type {Date}
     * @memberof RoleAssignment
     */
    startDate?: Date | null;
    /**
     * 
     * @type {Date}
     * @memberof RoleAssignment
     */
    endDate?: Date | null;
    /**
     * 
     * @type {UserRead}
     * @memberof RoleAssignment
     */
    readonly createdBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof RoleAssignment
     */
    readonly createdAt: Date;
    /**
     * 
     * @type {UserRead}
     * @memberof RoleAssignment
     */
    readonly modifiedBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof RoleAssignment
     */
    readonly modifiedAt: Date;
}



/**
 * Check if a given object implements the RoleAssignment interface.
 */
export function instanceOfRoleAssignment(value: object): value is RoleAssignment {
    if (!('id' in value) || value['id'] === undefined) return false;
    if (!('scopeType' in value) || value['scopeType'] === undefined) return false;
    if (!('scopeUuid' in value) || value['scopeUuid'] === undefined) return false;
    if (!('role' in value) || value['role'] === undefined) return false;
    if (!('roleSlug' in value) || value['roleSlug'] === undefined) return false;
    if (!('user' in value) || value['user'] === undefined) return false;
    if (!('userUsername' in value) || value['userUsername'] === undefined) return false;
    if (!('assignmentMethod' in value) || value['assignmentMethod'] === undefined) return false;
    if (!('enrollmentMethod' in value) || value['enrollmentMethod'] === undefined) return false;
    if (!('accessRequest' in value) || value['accessRequest'] === undefined) return false;
    if (!('createdBy' in value) || value['createdBy'] === undefined) return false;
    if (!('createdAt' in value) || value['createdAt'] === undefined) return false;
    if (!('modifiedBy' in value) || value['modifiedBy'] === undefined) return false;
    if (!('modifiedAt' in value) || value['modifiedAt'] === undefined) return false;
    return true;
}

export function RoleAssignmentFromJSON(json: any): RoleAssignment {
    return RoleAssignmentFromJSONTyped(json, false);
}

export function RoleAssignmentFromJSONTyped(json: any, ignoreDiscriminator: boolean): RoleAssignment {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'],
        'scopeType': json['scope_type'],
        'scopeUuid': json['scope_uuid'],
        'role': RoleReadFromJSON(json['role']),
        'roleSlug': json['role_slug'],
        'user': UserReadFromJSON(json['user']),
        'userUsername': json['user_username'],
        'assignmentMethod': AssignmentMethodEnumFromJSON(json['assignment_method']),
        'enrollmentMethod': EnrollmentMethodWithoutRoleReadFromJSON(json['enrollment_method']),
        'accessRequest': AccessRequestWithoutRoleReadFromJSON(json['access_request']),
        'isActive': json['is_active'] == null ? undefined : json['is_active'],
        'startDate': json['start_date'] == null ? undefined : (new Date(json['start_date'])),
        'endDate': json['end_date'] == null ? undefined : (new Date(json['end_date'])),
        'createdBy': UserReadFromJSON(json['created_by']),
        'createdAt': (new Date(json['created_at'])),
        'modifiedBy': UserReadFromJSON(json['modified_by']),
        'modifiedAt': (new Date(json['modified_at'])),
    };
}

export function RoleAssignmentToJSON(json: any): RoleAssignment {
    return RoleAssignmentToJSONTyped(json, false);
}

export function RoleAssignmentToJSONTyped(value?: Omit<RoleAssignment, 'id'|'role'|'user'|'assignment_method'|'enrollment_method'|'access_request'|'created_by'|'created_at'|'modified_by'|'modified_at'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'scope_type': value['scopeType'],
        'scope_uuid': value['scopeUuid'],
        'role_slug': value['roleSlug'],
        'user_username': value['userUsername'],
        'is_active': value['isActive'],
        'start_date': value['startDate'] == null ? undefined : ((value['startDate'] as any).toISOString()),
        'end_date': value['endDate'] == null ? undefined : ((value['endDate'] as any).toISOString()),
    };
}

