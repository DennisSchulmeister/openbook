OpenBook: Interactive Online Textbooks
=============================================

1. [Description](#description)
1. [Further Documentation](#further-documentation)
1. [Copyright](#copyright)

<p align="center">
   <!-- https://pixabay.com/photos/screwdriver-background-screw-wooden-1008974/ -->
   <img src="_img/under-construction.jpg" alt="Under Construction" width="300">
   <br>
   <b>Under Construction:</b> Development has just started in August 2024. Many features are not built yet!
   In the meantime please continue using <a href="https://www.npmjs.com/package/@dschulmeis/lecture-slides.js" target="_blank">lecture-slides.js</a>.
</p>

Description
-----------

OpenBook is the successor to [lecture-slide.js](https://www.npmjs.com/package/@dschulmeis/lecture-slides.js)
which as been in development since 2017. The main idea is still to create beautiful and engaging
online course materials for my students in the form of interactive online textbooks. Because this
is the form that the previous "lecture slides" have taken now. Instead of "interactive slides with
text" the form has more and more developed into a textbook, which is needed some hacky workarounds.

Also the architecture has shown some age and limitations over time. One of them being that development
of course materials requires solid HTML and to some degree JavaScript knowledge, as they are maintend
in source code form, only. That is a natural form for software developers teaching software development.
It is also great for version control (just use git) and free/libre release of the materials as Open
Educational Resources with permissive licences. Still it hinders wide adoption of the application as
most teachers and course developers prefer a more accessible WYSIWYG user interface.

So that's the product idea of OpenBook. To provide a modern web application and platform that
is easy to use, easy to deploy and easy to create interactive textbooks with. At the same time it
must still be possible to export textbooks as static HTML files for easy deployment on any server or
Learning Management System, versioning with Git and development in source form. Also richer and more
modern interactive elements (e.g. from [H5P](https://h5p.org/)) shall be included.

Further Documentation
---------------------

At the time being there is no full documentation, yet. But README files are available to summarize the
most important points for different target groups:

* [CHANGELOG.md](CHANGELOG.md): Release change log
* [PLANNING.md](PLANNING.md): Planned developments
* [BACKLOG.md](BACKLOG.md): Ideas what could be done
* [HACKING.md](HACKING.md): Information for developers
* [DEPLOYMENT.md](DEPLOYMENT.md): Installation notes for administrators
* [CONTRIBUTORS.md](CONTRIBUTORS.md): List of contributors (patches welcome)
* [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Our community code of conduct

Copyright
---------

OpenBook: Interactive Online Textbooks <br/>
© 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de> <br>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Development funded by the KoLLI research project at DHBW Karlsruhe.
