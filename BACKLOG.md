OpenBook: Development Backlog
=============================

1. [Short-Term TODOs](#short-term-todos)
1. [General Ideas](#general-ideas)

Short-Term TODOs
----------------

In no particular order:

-[ ] Additional Django packages
  -[ ] [Integrate Django REST Framework](https://www.django-rest-framework.org/)
  -[ ] [Integrate Django Vector DB](https://pkavumba.github.io/django-vectordb/)
  -[ ] [Django Image Uploader Widget](https://github.com/inventare/django-image-uploader-widget)
  -[ ] [Django Import Export](https://github.com/django-import-export/django-import-export)
  -[ ] [Django Color Field](https://github.com/fabiocaccamo/django-colorfield)
  -[ ] [Django Tree Node](https://github.com/fabiocaccamo/django-treenode)
  -[ ] [Django Env Notice](https://github.com/dizballanze/django-admin-env-notice)
  -[ ] [Django QL](https://github.com/ivelum/djangoql)
  -[ ] [Integrate Unfold Admin](https://unfoldadmin.com/) or
       [Django Admin Volt](https://github.com/app-generator/django-admin-volt) or
       [Django Jet Reboot](https://github.com/assem-ch/django-jet-reboot?tab=readme-ov-file)
  -[ ] [Integrate Django SAML2 Auth](https://github.com/grafana/django-saml2-auth)

-[ ] Frontend projects
  -[X] Scaffold frontend SPA (svelte + routing)
  -[ ] Scaffold core component library (svelte web components)
  -[ ] Fix: esbuild build errors for the frontend/admin package
  -[ ] Fix: esbuild watch mode not watching static files

-[ ] Library manager
  -[ ] Finish data model
  -[ ] Create REST endpoints
  -[ ] Create admin pages
  -[ ] Implement ZIP file import/export

-[ ] Learning content app
  -[ ] Define data model
  -[ ] Create REST endpoints
  -[ ] Create admin pages
  -[ ] HTML rendering

-[ ] Define other core apps and data model

General Ideas
-------------

Even though the precursor to OpenBook - lecture-slides.js - has been around
since 2017, development of this successor is still in the very early stages.
The following list contains a few very high-level ideas on what we want to work
in the future in no particular order.

Want to pick up a topic or plan a project with your students? We are looking forward
to hearing from you. Let's get in contact. :-)

* Modern redesign of the old lecture-slides.js library
* Modern redesign of the old ls-xyz plugins (using a light-weight web component framework)
* WYSIWYG online editor to edit textbooks directly in the browser
* Running textbooks directly from the textbook server
* Static export of textbooks for deployment on a static web server / upload in a learning management system
* Import and export of textbooks as ZIP bundles for backups and migration to another server
* Many more content plugins :-)
* Possibility for students to make annotations and notes in the textbook
* Graded learning quizzes with server backend (know which student scored in which test)
* Anonymous learning statistics (how many of a course have read which pages?)
