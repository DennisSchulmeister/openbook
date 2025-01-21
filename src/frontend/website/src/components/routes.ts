/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// import type {RouteDetail} from "svelte-spa-router";

import {wrap}             from "svelte-spa-router/wrap";
import Placeholder        from "./app-frame/Placeholder.svelte";
import NotFoundPage       from "./pages/errors/NotFoundPage.svelte";
// import {currentPage}      from "../stores/book.js";

// /**
//  * Update page number in the global store before the router renders the
//  * next page. This makes sure that all components, not just the one chosen
//  * by the router, receive the updated page number.
//  */
// function setPageNumber(detail:RouteDetail): boolean {
//     let page = parseInt(detail?.params?.pageNumber || "1");
//     currentPage.set(page);
//     return true;
// }

export default {
    "/": wrap({
        // @ts-ignore: Temporary silence type error, until svelte-spa-router adds official Svelte 5 support.
        // Issue: https://github.com/ItalyPaleAle/svelte-spa-router/issues/318
        component: Placeholder,
        // conditions: [setPageNumber],
    }),
    
    // "/book/page/:pageNumber": wrap({
    //     // @ts-ignore: Temporary silence type error, until svelte-spa-router adds official Svelte 5 support.
    //     // Issue: https://github.com/ItalyPaleAle/svelte-spa-router/issues/318
    //     component: BookContentPage,
    //     conditions: [setPageNumber],
    // }),

    "*": NotFoundPage,
};
