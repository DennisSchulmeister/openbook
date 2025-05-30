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
 * User (Full Profile)
 * @export
 * @interface UserDetailsRead
 */
export interface UserDetailsRead {
    /**
     * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
     * @type {string}
     * @memberof UserDetailsRead
     */
    username: string;
    /**
     * 
     * @type {string}
     * @memberof UserDetailsRead
     */
    readonly fullName: string;
    /**
     * 
     * @type {string}
     * @memberof UserDetailsRead
     */
    firstName?: string;
    /**
     * 
     * @type {string}
     * @memberof UserDetailsRead
     */
    lastName?: string;
    /**
     * URL for profile picture
     * @type {string}
     * @memberof UserDetailsRead
     */
    readonly profilePicture: string;
    /**
     * 
     * @type {string}
     * @memberof UserDetailsRead
     */
    readonly description: string;
}

/**
 * Check if a given object implements the UserDetailsRead interface.
 */
export function instanceOfUserDetailsRead(value: object): value is UserDetailsRead {
    if (!('username' in value) || value['username'] === undefined) return false;
    if (!('fullName' in value) || value['fullName'] === undefined) return false;
    if (!('profilePicture' in value) || value['profilePicture'] === undefined) return false;
    if (!('description' in value) || value['description'] === undefined) return false;
    return true;
}

export function UserDetailsReadFromJSON(json: any): UserDetailsRead {
    return UserDetailsReadFromJSONTyped(json, false);
}

export function UserDetailsReadFromJSONTyped(json: any, ignoreDiscriminator: boolean): UserDetailsRead {
    if (json == null) {
        return json;
    }
    return {
        
        'username': json['username'],
        'fullName': json['full_name'],
        'firstName': json['first_name'] == null ? undefined : json['first_name'],
        'lastName': json['last_name'] == null ? undefined : json['last_name'],
        'profilePicture': json['profile_picture'],
        'description': json['description'],
    };
}

export function UserDetailsReadToJSON(json: any): UserDetailsRead {
    return UserDetailsReadToJSONTyped(json, false);
}

export function UserDetailsReadToJSONTyped(value?: Omit<UserDetailsRead, 'full_name'|'profile_picture'|'description'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'username': value['username'],
        'first_name': value['firstName'],
        'last_name': value['lastName'],
    };
}

