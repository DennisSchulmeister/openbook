<!--
OpenBook: Interactive Online Textbooks - Server
© 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Placeholder for the start page until we have proper content to show.
 -->
<script lang="ts">
    import {i18n}  from "../../stores/i18n.js";    
</script>

<div>
    <h1>{$i18n.Placeholder.Title}</h1>
    <p>
        {@html $i18n.Placeholder.Text}
    </p>
    <img src="placeholder.svg" alt="">
</div>

<style>
    div {
        flex: 1;
        align-self: center;
        text-align: center;
    }

    img {
        display: block;
        width: 30em;
        max-width: 100%;
        margin-top: 3em;
    }

    p {
        color: darkred; 
    }
</style>