Stack
=====

The backend stack is Django 2.1 with all the goodies that it has to over

The front end framework is to be decided, if any

DevOps
======

The test configuration will be hosted on DigitalOcean under my stolaconsulting
domain, but eventually will be migrated to either AWS (or DO with Kubernetes).
The plan is to containerize the application and run with uWSGI.

The database will be either MySQL or PostgresSQL (do a pros and cons list and
migrate soonish)

StyleGuide
==========

CSS
---

Color-Theme:
    - header & footer: #2d3246
    - link highlight: #ff0090

Models
======

User:
    - username
    - password
    - email
    - first_name
    - last_name

Profile (1-to-1) with User:
    - email_verified
