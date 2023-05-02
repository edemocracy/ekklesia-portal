# Ekklesia Portal

This repository is part of the [Ekklesia e-democracy](https://ekklesiademocracy.org)
platform. It provides the motion portal Web UI, the public API and administrative interface.

You can find more development and operation documentation in the
[Ekklesia Documentation](https://ekklesiademocracy.org)

## Tech Stack

- Backend:
    - Main language: [Python 3.11](https://www.python.org)
    - Web framework: [Morepath](http://morepath.readthedocs.org)
    - Testing: [pytest](https://pytest.org),
      [WebTest](https://docs.pylonsproject.org/projects/webtest/en/latest/)
- Frontend
    - Templates [PyPugJS](https://github.com/kakulukia/pypugjs) (similar to [Pug](https://pugjs.org))
      with [Jinja](https://jinja.palletsprojects.com) as template engine.
    - [Sass](https://sass-lang.com) Framework [Bootstrap 4](https://getbootstrap.com)
    - [htmx](https://htmx.org) for "AJAX" requests directly from HTML.
- Database: [PostgreSQL 15](https://www.postgresql.com)
- Dependency management and build tool: [Nix](https://nixos.org/nix)
- Documentation: [Sphinx](https://sphinx-doc.org) with [MyST Markdown](https://myst-parser.readthedocs.io) parser.
- (Optional) Run on NixOS with the included NixOS module
- (Optional) Docker / Podman for running container images (built by Nix)

## Development

To get a consistent development environment, we use
[Nix](https://nixos.org/nix) to install Python and the project
dependencies. The development environment also includes PostgreSQL,
code linters, a SASS compiler and pytest for running the tests.

### Development Quick Start

This section describes briefly how to set up a development environment to run a local instance of the application.

Setting up the environment for testing and running tests is described in the
section [Testing](https://docs.ekklesiademocracy.org/en/latest/development/testing.html)
in the Ekklesia documentation.

The following instructions assume that *Nix* is already installed, has Nix
flakes enabled, and an empty + writable PostgreSQL database can be accessed somehow.

If you don't have *Nix* with Flakes support and or can’t use an existing
PostgreSQL server, have a look at the [Development Environment](https://docs.ekklesiademocracy.org/en/latest/development/dev_env.html)
section in the Ekklesia documentation.

It's strongly recommended to also follow the instructions at
`Setting up the Cachix Binary Cache <https://docs.ekklesiademocracy.org/en/latest/development/dev_env.html#setting-up-the-cachix-binary-cache>`
or the first step will take a long time to complete.

1. Clone the repository and enter nix shell in the project root folder to open a shell which is
   your dev environment:

   ```
   git clone https://github.com/edemocracy/ekklesia-portal
   cd ekklesia-portal
   nix develop
   ```

2. Compile translations and CSS (look at `dodo.py` to see what this does):

   ```
   doit
   ```

3. Create a config file named `config.yml` using the config template
   from `src/ekklesia_portal/config.example.yml` or skip this to use
   the default settings from `src/ekklesia_portal/default_settings.py`.
   Make sure that the database connection string points to an
   empty + writable database.

4. Set up the dev database (look at `flake.nix` to see what this does):

   ```
   create_dev_db
   ```

5. Run the development server (look at `flake.nix` to see what this does):
   ```
   run_dev
   ```

Run `help` to see all commonly used dev shell commands.

## Running In Production

A production environment can be built by Nix. The generated output
doesn’t have additional requirements. The application can be run by a
start script directly, using the included NixOS module or the Docker image
built by Nix. Static assets are built separately and can be served by the
included minimal Nginx. As for the application itself, we can build a
standalone start script or a Docker image.

See the [Ekklesia Operations Manual](https://docs.ekklesiademocracy.org/en/latest/operations/index.html)
for more information.

## History

Ekklesia Portal started as an improved implementation of Wikiarguments
in Python 3.x using the Flask micro web framework. The project is now
based on the [Morepath](https://github.com/morepath/morepath) web
framework and tries to explore ideas from the Ruby project
[Trailblazer](https://trailblazer.to).

## License

AGPLv3, see LICENSE

## Active Authors

- Tobias ‘dpausp’
- Nico ‘kaenganxt’
- Holger ‘plexar’
