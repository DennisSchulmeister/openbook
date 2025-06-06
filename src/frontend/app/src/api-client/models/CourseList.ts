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
 * Reduced list of fields for filtering a list of courses.
 * @export
 * @interface CourseList
 */
export interface CourseList {
    /**
     * 
     * @type {string}
     * @memberof CourseList
     */
    readonly id: string;
    /**
     * 
     * @type {string}
     * @memberof CourseList
     */
    readonly slug: string;
    /**
     * 
     * @type {string}
     * @memberof CourseList
     */
    readonly name: string;
    /**
     * Flag that this course is only used for creating other courses.
     * @type {boolean}
     * @memberof CourseList
     */
    readonly isTemplate: boolean;
    /**
     * 
     * @type {UserRead}
     * @memberof CourseList
     */
    readonly owner: UserRead;
    /**
     * 
     * @type {UserRead}
     * @memberof CourseList
     */
    readonly createdBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof CourseList
     */
    readonly createdAt: Date | null;
    /**
     * 
     * @type {UserRead}
     * @memberof CourseList
     */
    readonly modifiedBy: UserRead;
    /**
     * 
     * @type {Date}
     * @memberof CourseList
     */
    readonly modifiedAt: Date | null;
}

/**
 * Check if a given object implements the CourseList interface.
 */
export function instanceOfCourseList(value: object): value is CourseList {
    if (!('id' in value) || value['id'] === undefined) return false;
    if (!('slug' in value) || value['slug'] === undefined) return false;
    if (!('name' in value) || value['name'] === undefined) return false;
    if (!('isTemplate' in value) || value['isTemplate'] === undefined) return false;
    if (!('owner' in value) || value['owner'] === undefined) return false;
    if (!('createdBy' in value) || value['createdBy'] === undefined) return false;
    if (!('createdAt' in value) || value['createdAt'] === undefined) return false;
    if (!('modifiedBy' in value) || value['modifiedBy'] === undefined) return false;
    if (!('modifiedAt' in value) || value['modifiedAt'] === undefined) return false;
    return true;
}

export function CourseListFromJSON(json: any): CourseList {
    return CourseListFromJSONTyped(json, false);
}

export function CourseListFromJSONTyped(json: any, ignoreDiscriminator: boolean): CourseList {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'],
        'slug': json['slug'],
        'name': json['name'],
        'isTemplate': json['is_template'],
        'owner': UserReadFromJSON(json['owner']),
        'createdBy': UserReadFromJSON(json['created_by']),
        'createdAt': (json['created_at'] == null ? null : new Date(json['created_at'])),
        'modifiedBy': UserReadFromJSON(json['modified_by']),
        'modifiedAt': (json['modified_at'] == null ? null : new Date(json['modified_at'])),
    };
}

export function CourseListToJSON(json: any): CourseList {
    return CourseListToJSONTyped(json, false);
}

export function CourseListToJSONTyped(value?: Omit<CourseList, 'id'|'slug'|'name'|'is_template'|'owner'|'created_by'|'created_at'|'modified_by'|'modified_at'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
    };
}

