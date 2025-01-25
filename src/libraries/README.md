OpenBook: Libraries
===================

This directory contains the frontend libraries for textbooks made with OpenBook. This includes the
core library (required by all textbooks) as well as extension libraries maintained by the OpenBook
project with additional features and content types.

Note that for each library **two** bundles are built:

 * `./{library}/dist/**`: Bundle for publishing on npmjs.org

 * `../src/_media/lib/{library}/**`:
   Pre-installed version shipped with the OpenBook server
