OpenBook Server
===============

This is the server part of OpenBook Studio. For all practical purposes this is a pretty much standard
Django web application, with the notable difference that Django channels is used for real-time communication
over websockets. So an ASGI-capable web server is needed to host the platform. See README files at the
root-level of the project for more information.
