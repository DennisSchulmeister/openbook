OpenBook Studio: Development Plan
=================================

This living document briefly lists the topics that are currently being worked on
or we we plan to do. Want to pick up a topic? Have more ideas? Let's get in touch. 🤠

Library Manager
---------------

[ ] Basic admin page for each model

[ ] Check dependencies of all installed libraries
    [ ] Management command
    [ ] Admin action for a single library in the Library search page
    [ ] Custom admin page to check all installed libraries

[ ] Install library from ZIP file
    [ ] Reintroduce Django Ninja dependency for publish/download API
    [ ] Management command to install a ZIP file from local or remote installation
    [ ] Management command to install all or a single pre-installed library
    [ ] Custom admin page to install from uploaded ZIP file or remote installation

[ ] De-installation / removal of libraries
    [ ] Hook into model delete (post-delete hook) to delete media files ([ChatGPT](https://chatgpt.com/share/d93a0196-93b1-4dc1-9ea4-e1fea0832de3))
    [ ] Management command to de-install a library

Feedback Surveys
----------------

[ ] Very basic data-model for sent-in feedback
[ ] Plug-in for old lecture-slide.js to send surveys to the server

Core Architecture
-----------------

[ ] Rewrite core lecture-slides.js into @openbook-studio/core library

    * New library shall be web component based (e.g with Tonic or Lit)

    * Must be possible to create textbooks without JavaScript code at all
        * `<open-book>` custom element to configure and render the textbook
        * JavaScript API as events and methods to this component
        * By default: Split code so that index.html only contains configuration

    * Define better HTML structure for textbook pages

    * Allow multiple "parser" implementations that read-in the HTML code, so
      that old lecture-slide.js style HTML code can still be used

[ ] Rewrite old lecture-slides.js plugins

WYSIWYG Editor
--------------

[ ] Define UI mockups. Some random thoughts:

    * Toggle edit mode button in the textbook header
    * Floating action button to open popover with editing functions
        * Edit common textbook attributes / configuration
        * Edit page and chapter structure (insert pages, move pages, ...)
        * Insert new component
        * …

[ ] Start building it :-)
[ ] Download textbook as ZIP file for deployment on a static web server
[ ] (Re)import textbook from uploaded ZIP file

Catalogue / Browser
-------------------

[ ] Allow definition of a "directory" hierarchy for textbooks
[ ] Flag for private/public textbooks (private = not shown in catalogue)
[ ] Access password for private textbooks similar to Moodle course password
[ ] Nice UI to browse available textbooks
