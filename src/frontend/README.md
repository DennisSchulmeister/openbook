OpenBook Frontend
========================

This is the JavaScript / TypeScript code for the OpenBook Frontend. This is not
the single page app that renders textbooks, but the user interface of server backend.
It is mainly used to pull external libraries from the NPM package index and build a
distribution bundle. The source code is split between two distinct directories:

* `admin`: JS/CSS bundle for the Django Admin
* `website`: JS/CSS bundle for the public website

The admin bundle is used in a few templates that extend the Django Admin. It is separate from
the rest of the website as the Django Admin evolves independently of our public website.

For the single page app, see the [libraries](../../../libraries) directory.
