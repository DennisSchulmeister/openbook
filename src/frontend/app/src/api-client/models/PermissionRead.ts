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
 * Permission
 * @export
 * @interface PermissionRead
 */
export interface PermissionRead {
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    permString: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    permDisplayName: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    app: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    appDisplayName: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    model: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    modelDisplayName: string;
    /**
     * 
     * @type {string}
     * @memberof PermissionRead
     */
    codename: string;
}

/**
 * Check if a given object implements the PermissionRead interface.
 */
export function instanceOfPermissionRead(value: object): value is PermissionRead {
    if (!('permString' in value) || value['permString'] === undefined) return false;
    if (!('permDisplayName' in value) || value['permDisplayName'] === undefined) return false;
    if (!('app' in value) || value['app'] === undefined) return false;
    if (!('appDisplayName' in value) || value['appDisplayName'] === undefined) return false;
    if (!('model' in value) || value['model'] === undefined) return false;
    if (!('modelDisplayName' in value) || value['modelDisplayName'] === undefined) return false;
    if (!('codename' in value) || value['codename'] === undefined) return false;
    return true;
}

export function PermissionReadFromJSON(json: any): PermissionRead {
    return PermissionReadFromJSONTyped(json, false);
}

export function PermissionReadFromJSONTyped(json: any, ignoreDiscriminator: boolean): PermissionRead {
    if (json == null) {
        return json;
    }
    return {
        
        'permString': json['perm_string'],
        'permDisplayName': json['perm_display_name'],
        'app': json['app'],
        'appDisplayName': json['app_display_name'],
        'model': json['model'],
        'modelDisplayName': json['model_display_name'],
        'codename': json['codename'],
    };
}

export function PermissionReadToJSON(json: any): PermissionRead {
    return PermissionReadToJSONTyped(json, false);
}

export function PermissionReadToJSONTyped(value?: PermissionRead | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'perm_string': value['permString'],
        'perm_display_name': value['permDisplayName'],
        'app': value['app'],
        'app_display_name': value['appDisplayName'],
        'model': value['model'],
        'model_display_name': value['modelDisplayName'],
        'codename': value['codename'],
    };
}

