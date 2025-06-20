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
 * HTML Component
 * @export
 * @interface PatchedHTMLComponent
 */
export interface PatchedHTMLComponent {
    /**
     * 
     * @type {string}
     * @memberof PatchedHTMLComponent
     */
    readonly id?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedHTMLComponent
     */
    library?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedHTMLComponent
     */
    tagName?: string;
    /**
     * 
     * @type {Array<string>}
     * @memberof PatchedHTMLComponent
     */
    readonly definitions?: Array<string>;
}

/**
 * Check if a given object implements the PatchedHTMLComponent interface.
 */
export function instanceOfPatchedHTMLComponent(value: object): value is PatchedHTMLComponent {
    return true;
}

export function PatchedHTMLComponentFromJSON(json: any): PatchedHTMLComponent {
    return PatchedHTMLComponentFromJSONTyped(json, false);
}

export function PatchedHTMLComponentFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedHTMLComponent {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'library': json['library'] == null ? undefined : json['library'],
        'tagName': json['tag_name'] == null ? undefined : json['tag_name'],
        'definitions': json['definitions'] == null ? undefined : json['definitions'],
    };
}

export function PatchedHTMLComponentToJSON(json: any): PatchedHTMLComponent {
    return PatchedHTMLComponentToJSONTyped(json, false);
}

export function PatchedHTMLComponentToJSONTyped(value?: Omit<PatchedHTMLComponent, 'id'|'definitions'> | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'library': value['library'],
        'tag_name': value['tagName'],
    };
}

