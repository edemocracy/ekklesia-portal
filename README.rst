***************
Ekklesia Portal
***************

This repository is part of the `Ekklesia e-democracy <https://ekklesiademocracy.org>`_
platform. It provides the motion portal Web UI, the public API and administrative interface.

You can find more development and operation documentation in the
`Ekklesia Documentation <https://ekklesiademocracy.org>`_


Tech Stack
==========

* Backend:

    * Main language: `Python 3.9 <https://www.python.org>`_
    * Web framework: `Morepath <http://morepath.readthedocs.org>`_
    * Testing: `pytest <https://pytest.org>`_,
      `WebTest <https://docs.pylonsproject.org/projects/webtest/en/latest/>`_

* Frontend

    * Templates `Pyjade <https://github.com/syrusakbary/pyjade>`_ (syntax like `Pug <https://pugjs.org>`_)
      with `Jinja <https://jinja.palletsprojects.com>`_ as template engine.
    * `Sass <https://sass-lang.com>`_ Framework `Bootstrap 4 <https://getbootstrap.com>`_
    * `htmx <https://htmx.org>`_ for "AJAX" requests directly from HTML.

* Database: `PostgreSQL 13 <https://www.postgresql.com>`_
* Dependency management and build tool: `Nix <https://nixos.org/nix>`_
* (Optional) Docker / Kubernetes for running Docker images built by Nix


Development
===========

To get a consistent development environment, we use
`Nix <https://nixos.org/nix>`_ to install Python and the project
dependencies. The development environment also includes PostgreSQL,
code linters, a SASS compiler and pytest for running the tests.

Development Quick Start
-----------------------

This section describes briefly how to set up a development environment to run a local instance of the application.

Setting up the environment for testing and running tests is described in the
section `Testing <https://docs.ekklesiademocracy.org/en/latest/development/testing.html>`_
in the Ekklesia documentation.

The following instructions assume that *Nix* and *lorri* are already installed,
and an empty + writable PostgreSQL database can be accessed somehow.

If you don't have *Nix* and *lorri* or can’t use an existing PostgreSQL server,
have a look at the section `Development Environment <https://docs.ekklesiademocracy.org/en/latest/development/dev_env.html>`_
in the Ekklesia documentation.

It's strongly recommended to also follow the instructions at
`Setting up the Cachix Binary Cache <https://docs.ekklesiademocracy.org/en/latest/development/dev_env.html#setting-up-the-cachix-binary-cache>`
or the first step will take a long time to complete.

1. Clone the repository and enter nix shell in the project root folder to open a shell which is
   your dev environment::

    git clone https://github.com/edemocracy/ekklesia-portal
    cd ekklesia-portal
    lorri shell


2. Compile translations and CSS (look at dodo.py to see what this does)::

    doit

3. Create a config file named ``config.yml`` using the config template
   from ``src/ekklesia_portal/config.example.yml`` or skip this to use
   the default settings from ``src/ekklesia_portal/default_settings.py``.
   Make sure that the database connection string points to an
   empty + writable database.

4. Initialize the dev database with a custom config file::

    python tests/create_test_db.py -c config.yml


5. The development server can be run with a custom config file by
   executing::

    python src/ekklesia_portal/runserver.py –debug -c config.yml 2>&1 | eliot-tree -l0


6. You can run ``doit auto`` to automatically compile translations and CSS when the input files change.


Running In Production
=====================

A production environment can be built by Nix. The generated output
doesn’t have additional requirements. The application can be run by a
start script directly, using the included NixOS module or the Docker image
built by Nix. Static assets are built separately and can be served by the
included minimal Nginx. As for the application itself, we can build a
standalone start script or a Docker image.

See the `Ekklesia Operations Manual <https://docs.ekklesiademocracy.org/en/latest/operations/index.html>`_
for more information.

History
=======

Ekklesia Portal started as an improved implementation of Wikiarguments
in Python 3.x using the Flask micro web framework. The project is now
based on the `Morepath <https://github.com/morepath/morepath>`__ web
framework and tries to explore ideas from the Ruby project
`Trailblazer <https://trailblazer.to>`__.

License
=======

AGPLv3, see LICENSE

Active Authors
==============

* Tobias ‘dpausp’
* Holger ‘plexar’
* Nico ‘kaenganxt’
