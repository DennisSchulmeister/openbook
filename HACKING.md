Developer Notes for OpenBook
===================================

This document serves as a cheat sheet for developers to get started quickly. There are no
fancy things -- if you already know Python, Poetry, Django, NPM, … But finding the right
information might not be easy when working with so much different technology. This document
tries to summarize the most important things.

1. [Quick Start](#quick-start)
1. [Technology Choices](#technology-choices)
1. [Dependency Policy](#dependency-policy)
1. [Directory Layout](#directory-layout)
1. [Poetry Package Management](#poetry-package-management)
1. [Django Web Framework](#django-web-framework)
1. [Django Project vs. App](#django-project-vs-app)
1. [Core Data Model and Object Permissions](#core-data-model-and-object-permissions)
1. [Creating Fixtures](#creating-fixtures)
1. [SQLite Shell](#sqlite-shell)
1. [NPM and esbuild](#npm-and-esbuild)

Quick Start
-----------

The following tools must be available on your development machine:

* Python
* Node.js
* Redis

Then you can install all dependent libraries:

```sh
poetry install
npm install
```

To run all components locally:

```sh
npm start
```

This will start the following things:

* Daphne Webserver in watch mode
* Redis Key/Value-Store
* A local fake SMTP server
* Esbuild in watch mode

The setup will be fairly similar to a typical production environment minus the database.
For local development we use SQLite as per Django's defaults.

Technology Choices
------------------

The OpenBook Server is built with the following technology:

* Python
* Poetry - Package Management
* Django Web Framework - Core Server Framework
* Django REST Framework - API Endpoints for the frontend and external clients
* Django Channels - Websocket Support

The idea is to keep the technical requirements lean to enable easy deployment in custom environments.
Therefor the choice of Django might be considered "conservative", but in fact it contains all the needed
functionality like HTTP request routing, server-side templates, database access, ... in a single, stable
and well maintained dependency. 

The frontend is a single page app, composed of a core library and several add-on libraries, that
can also run stand-alone without server backend. In part this is due to the development history
of the project starting as a pure static SPA in 2017. But it has the nice advantage to still allow
static deployments of course materials on any web server or learning management system. Therefor,
for the frontend we use the following additional things:

 * esbuild - Bundler
 * npm - Package manager
 * TypeScript - Type annotations for JavaScript

Dependency Policy
-----------------

There are no hard rules whether to allow or avoid external dependencies. But we try to not depend too
much on external dependencies as they might cause major rewrites when their API changes or they become
unmaintained. Generally speaking, dependencies are okay, when they are either small or would be too
costly to reimplement.

### Small Dependencies

These should be limited and scope and either easy to replace or dispensible.
E.g. [Django Color Field](https://github.com/fabiocaccamo/django-colorfield), which is used to add
color pickers to the admin interface. Having color pickers is nice but not mission critical. Plus, we
could reimplement the widget with acceptable effort, if needed.

Still, if a dependency is too small (think if small utilities with a few lines of code), it is probably
best to implement the functionality oneself.

### Too Costly to Reimplement

These bring a major advantage, drastically decreasing "time to market". Using an external library makes
perfectly sense but comes at a price. If they ever go away, most likely major parts must be rewritten.
So they should either be time-proven an API-stable (think [Django](https://www.djangoproject.com/) or
[Django REST Framework](https://www.djangoproject.com/)) or at least somewhat limited in scope
([lua-wrapper](https://pypi.org/project/lua-wrapper/)).

Directory Layout
----------------

Here are a few important directories and files that you might want to know about:

```text
.                                       Root directory with this file
├── src                                 Main source directory
│   ├── openbook                        The server application built with Django
│   │   ├── local_settings.py           Use this for your own server configuration
│   │   ├── settings.py                 Internal settings of the server
│   │   └── ...
│   └── manage.py                       Django CLI for the server
│
├── frontend
│   ├── admin                           Static files and browser code for the Django admin
│   └── app                             Single page app for the actual frontend built with Svelte
│
└── libraries                           Custom element libraries built with Svelte for textbook content
│   └── ...
```

Poetry Package Management
-------------------------

Python dependencies are managed with [Poetry](https://python-poetry.org/), which is similar in spirit
to NPM for Node.js developers. It handles installation and upgrades of all required external Python
packages, which for this reason need to be declared in the [pyproject.toml](pyproject.toml) file,
plus it fully automates the usage of virtual environments. The most important commands are:

* `poetry init` - Start a new project with the Poetry package manager (already done of course 🙂)
* `poetry install` - Install all dependencies specified in [pyproject.toml](pyproject.toml)
* `poetry add xyz` - Add another dependency to library `xyz`
* `poetry remove xyz` - Remove dependency to library `xyz` again
* `poetry show --tree` - Show all direct and indirect dependencies
* `poetry shell` - Start a new shell with the Python environment enabled
* `poetry run xyz` - Run console command `xyz` in the Python environment
* `poetry list` - Show all available sub-commands
* `poetry env use $(which python)` - Create new virtual Python environment
* `poetry env list` - List available environments
* `poetry env remove xyz` - Delete environment

Django Web Framework
--------------------

[Django](https://www.djangoproject.com/) is our server-side main framework. It comes with its own
CLI called `django-admin` or `manage.py` inside the project directory. Actually both are identical,
but with the latter a few environment variables point to the current project.

Important commands at the root-level, outside Django projects:

* `django-admin xyz` - Run Django admin command `xyz`
* `django-admin startproject xyz` - Add new Django project `xyz` to the workspace

Important commands inside project directories:

* `./manage.py xyz` - Run Django management command `xyz`
* `./manage.py startapp xyz` - Add Django app `xyz` to the Django project
* `./manage.py runserver` - Start development server
* `./manage.py test` - Run unit tests
* `./manage.py collectstatic` - Collect static files into `_static/` directory
* `./manage.py dbshell` - Open a database shell to inspect the database

After each change to the database model, the following commands need to be run:

* `./manage.py makemigrations` - Create migrations from latest model changes
* `./manage.py migrate` - Run database migrations

Once the changes shall be committed to version control, it makes sense to "squash" the migrations,
to have only one migration file for all changes:

* `./manage.py squashmigrations` - Reduce multiple migrations into one

Django Project vs. App
----------------------

Each Django web application consists of a _Django project_, representing the web application
itself, and usually multiple _Django apps_, representing single functional units. Both are
Python modules with certain required source files. Though the whole source code could easily
live inside the project module, the Django developers recommend splitting the project into
multiple apps to foster separation of concerns and code re-use.

When you have a project like `openbook` the Django Admin command created a top-level
directory of that name, containing a sub-directory of the same name. But to avoid having
three nested directories of the same name, that directory was renamed to `src`, inside
which the `openbook` Django project lives, inside which several apps live. Technically
the apps could also live a siblings to the project, but allos us to use the sibling
directories for other things.


```text
.                                 Root directory with this file
└── src                           Main source directory
    ├── manage.py                 Django CLI
    └── openbook                  Django project
        ├── settings.py           Django configuration
        ├── app_1                 Django Application
        │   └── ...
        ├── app_2                 Django Application
        │   └── ...
        └── ...                   Django Application
```

Core Data Model and Object Permissions
--------------------------------------

The foundational data model fulfills the following requirements:

* Learning content is organized into textbooks such as "Web Development", "Python I", etc.
* Textbooks have teachers and students who access and edit its content.
* Books are placed in a hierarchical ordered library (e.g., study program / subject area).
* Books can have more than one location in the library (e.g. two different study programs)
* Users with different roles like (e.g., author, reviewer) work on the books.

Note that we use some slightly different words than in a traditional LMS. Here we split learning
content (textbooks) from its usage (courses):

* Courses can marked as template courses that are only used to create new identical courses.
* Courses are held and supported by teachers.
* Courses use one or more textbooks for their learning content.
* Courses are also structured in a hierarchical way (e.g., study program).
* Courses have students assigned.
* Thus persons in a course have different roles (e.g, teacher, student).
* Permissions depend on the role a user has within a course (e.g., teacher, student).
* Roles exist only within their respecitve scope (textbook or course).
* The scope owner always has full permissions, regardless of their assigned role.

To better understand where we are coming from, consider the module "Distributed System Development"
(Entwicklung verteilter Systeme) in the "Business Informatics" (Wirtschaftsinformatik) degree programme
at DHBW Karlsruhe. The module comprises the two lectures "Web Programming" and "Distributed Systems",
which are held in parallel by different lecturers in up to five cohorts. Each cohort is a "course" in
which the students and teachers are enrolled, and each lecture is a "textbook" used within the course.
The textbooks are further developed and reused a year later in the new courses.

We handle as much of the permission logic as possible within the Django permissions system and
minimize custom logic in the REST layer. This means favoring `DjangoObjectPermissions` and related
classes when defining REST endpoints. Note that `DjangoModelPermissionsOrAnonReadOnly` is the
default defined in `settings.py`, giving anonymous users read-access by default.

We provide our own implementation of Django's object-level permission hooks, as it appears simpler
than reusing existing third-party libraries.

#### Caveats

* The Django model layer intentionaly checks no permissions. Permissions checking must be handled
  by higher levels like Django Admin or the REST layer.

* Django REST Framework checks permissions on the `get_object()` method. It may be necessary to
  manually call the inherited method, when it is replaced with a custom implementation or the
  generic REST views are not used.

* Limitations of object permissions in Django REST Framework: ([Source](https://www.django-rest-framework.org/api-guide/permissions/)):
  * For performance reasons the generic views will not automatically apply object level permissions
    to each instance in a queryset when returning a list of objects.

  * Often when you're using object level permissions you'll also want to filter the queryset appropriately,
    to ensure that users only have visibility onto instances that they are permitted to view.

  * Because the `get_object()` method is not called, object level permissions from the `has_object_permission()`
    method are not applied when creating objects. In order to restrict object creation you need to implement
    the permission check either in your `Serializer` class or override the `perform_create()` method of your
    `ViewSet` class.

Creating Fixtures
-----------------

Fixtures are a good way to provide initial data for developers and end-users to get started with
the OpenBook server. Here are a few hints on what to consider:

* **Hand-edited YAML Format:** Use `python manage.py dumpdata --format yaml myapp` to create a data
  dump on the console. Copy the relevant parts into a new `fixtures/myapp/xyz.yaml` file. Note that
  the file extension must be exactly `.yaml` for Django to recognize the fixture. Clean up the file,
  bring all entries in logical order, remove unneeded `null` properties and add comments.

* **Natural Keys:** When using the `dumpdata` command make sure to enable natural keys. Thus the
  full command becomes: `python manage.py dumpdata --format yaml --natural-foreign --natural-primary myapp`.
  This avoids a problem with generic relations: Each model with a generic relation must have a foreign
  key on the `ContentType` model that contains a list of all known models. This uses an auto-incremented
  ID that is not stable. Without natural keys the fixtures would contain the raw ID of the content type,
  that would most-likely not reference the model we want during import of the fixture.

* **Load Initial Data:** Once your new fixture is working, consider adding it to the `load_initial_data`
  management command. The source code is in the `openbook/core/management` directory. This allows other
  developers and users to import a complete set of initial data with only one command.

**Natural keys, part II:** Why are we not using natural keys for our models? After writing the lines
above the initial plan was to add natural keys to all own models, so that the fixtures would be free
from UUIDs and generally much easier to read. But the attached trade-offs quickly outgrew the benefit:

* Adding natural keys to each model increases the size considerably: `natural_key()` method, custom
  manager, unique constraint for each model. But that alone would have been okay, as we didn't want
  to introduce a dependency to [Django Natural Keys](https://pypi.org/project/natural-keys/) to keep
  the dependencies minimal.

* Many models have a name, that would be a perfect fit for the natural key. But it might be problematic
  to make them unique.

* Generic relations are still problematic due to the `object_id` property. That was the real killer.
  Why all the effort, if each generic relation still references the UUID of the related object?
  For this to work the UUID of the related object must be enforced during import, neglecting the reason
  to add natural keys in the first place.

  There is a work-around using [custom serializers and deserializers](https://stackoverflow.com/a/70700302).
  But that is quite a lot of code that needs deep understanding of Django's inner workings. 🤯
  Clearly something to avoid, if at all possible.

Thankfuly using UUIDs the problem is not as large as if we were using the traditional auto-incremented
IDs. With auto-incremented IDs natural keys are needed to ensure stable keys. Otherwise entries will
not be imported if the ID is already used by another entry and imported foreign keys will reference
the wrong object. UUIDs are supposed to be globally unique by default, avoiding most of the problems
in the first place.

SQLite Shell
------------

The command `./manage.py dbshell?` drops you into a database shell where you can execute SQL
commands against the database. Unfortunately the SQLite shell typically used during development
is very spartan. The `SELECT` output doesn't even show the column names. The following special
commands mitigate this a litte:

* `.tables` - List available tables
* `.mode column` - Turn column mode on to align the SELECT output in columns
* `.headers on` - Show column names in the first line
* `.quit` - Leave SQLite Shell (and use a proper tool 😛)

Make sure to use an extra wide terminal window, as the lines are still unreadebl when wrapped.

NPM and esbuild
---------------

OpenBook uses a mixture of traditional server-side rendering and more modern client-side rendering.
Server-side rendering using Django views and templates is used for server-provided pages like the admin
panel, WYSIWYG editor and server-controlled content that can be embedded into textbooks (e.g. surveys).
The textbooks, on the other hand, are displayed in a single page app, that can also be used without the
server backend.

For both parts the NPM package index is indispensible to mange client-side dependencies. We therefor use
a subset of Node.js and NPM to pull client-side libraries and bundle them into distribution files with
[esbuild](https://esbuild.github.io/).

The root-level [package.json](package.json) defines a NPM workspace, so that all NPM projects share
a global `node_modules` directory. It also defines most build-tools via its `devDependencies`, so
that they need not be maintained in several locations. Besides that, each sub-project has its own
`package.json` for runtime dependencies, additional development dependencies and run scripts. Typical
run scripts are:

* `npm run build` - Build distribution files
* `npm run clean` - Delete distribution files
* `npm run watch` - Start watch mode for automatical rebuilds
* `npm run check` - Run all checks and tests: eslint, TypeScript, unit tests
* `npm run start` or `npm start` - Run from built distribution files

Less-often used commands:

* `npm run test` - Run unit tests only
* `npm run tsc` - Check source code with TypeScript only
* `npm run lint` - Check source code with eslint only
* `npm run lintfix` - Auto-correct eslint findings (be careful!)
* `npm run prettier` - Check source code formatting with prettier
* `npm run format` - Auto-correct prettier findings (be careful!)
