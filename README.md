# Ekklesia Portal

Portal of the Ekklesia e-democracy platform.
You can visit a running instance at [antrag.piratenpartei.de](https://antrag.piratenpartei.de)

## Tech Stack

* Backend: [Python 3.8](https://www.python.org)
* Web framework: [Morepath](http://morepath.readthedocs.org )
* Frontend:
  [Pyjade](https://github.com/syrusakbary/pyjade) (like [Pug](https://pugjs.org)),
  [Jinja](https://jinja.palletsprojects.com),
  [Bootstrap 4](https://getbootstrap.com),
  [Sass](https://sass-lang.com),
  Javascript
* Database: [PostgreSQL 12](https://www.postgresql.com)
* Dependency management and build tool: [Nix](https://nixos.org/nix)
* (Optional) Docker / Kubernetes for running Docker images built by Nix

## Development

To get a consistent development environment, we use [Nix](https://nixos.org/nix) to install Python and the project dependencies.
The development environment also includes PostgreSQL 12, linters, a SASS compiler and pytest for running the tests.


### Install Nix

*Installation instructions taken from [Getting Nix](https://nixos.org/download.html). See the link for other installation methods.*

Nix is currently supported on Linux and Mac.
The quickest way to install Nix is to open a terminal and run the following command (as a user other than root with sudo permission):

~~~
curl -L https://nixos.org/nix/install | sh
~~~

Make sure to follow the instructions output by the script.
The installation script requires that you have sudo access to root.


### Install Lorri

The best way to get a development shell is to use [Lorri](https://github.com/target/lorri) which improves the builtin `nix-shell` command.

Install `lorri` (also works for updates):

~~~
nix-env -if https://github.com/target/lorri/archive/master.tar.gz
~~~

This is enough to use `lorri shell` needed for the quick start section below.

We also recommend using the `direnv` integration.
This will automatically enter the development shell when changing to the project directory.
Please follow the [Lorri Installation Instructions](https://github.com/target/lorri#setup-on-nixos-or-with-home-manager-on-linux).


### Project Quick Start

The following instructions assume that Nix is already installed, `lorri` is available in PATH and an empty + writable PostgreSQL database can be accessed somehow.

1. Clone the repository with:
    ~~~Shell
    git clone https://github.com/Piratenpartei/ekklesia-portal
    ~~~
2. Enter nix shell in the project root folder to open a shell which is your dev environment:
    ~~~Shell
    cd ekklesia-portal
    lorri shell
    ~~~
3. Compile translations and CSS:
    ~~~Shell
    ipython makebabel.ipy compile
    sassc -I $SASS_PATH src/ekklesia_portal/sass/portal.sass \
      src/ekklesia_portal/static/css/portal.css
    ~~~
4. Create a config file named `config.yml` using the config template from `src/ekklesia_portal/config.example.yml`
    or skip this to use the default settings from `src/ekklesia_portal/default_settings.py`.
    Make sure that the database connection string points to an empty + writable database.
5. Initialize the dev database with a custom config file:
    ~~~Shell
    python tests/create_test_db.py -c config.yml
    ~~~
6. The development server can be run with a custom config file by executing:
    ~~~Shell
    python src/ekklesia_portal/runserver.py --debug -c config.yml
    ~~~

### Running PostgreSQL as User

You can run a PostgreSQL database server with your user permissions if you don't want to use an existing database server. Run the pg_ctl commands from the nix shell.

Run as user:

~~~Shell
pg_ctl -D ~/postgresql init
postgres -D ~/postgresql -k /tmp -h ''
~~~

Create database (in another terminal):

~~~Shell
createdb -h /tmp ekklesia_portal
~~~

You can connect to the database with psql now:
~~~Shell
psql -h /tmp ekklesia_portal
~~~

The database can be used by ekklesia_portal with the following connection string in the config file:

~~~YAML
database:
    uri: "postgresql+psycopg2:///ekklesia_portal?host=/tmp"
~~~

### Generate CSS

CSS is compiled from Sass files that include files from Bootstrap and Font-Awesome. sassc is used as Sass compiler.

Generate CSS with:

~~~Shell
sassc -I $SASS_PATH src/ekklesia_portal/sass/portal.sass \
  src/ekklesia_portal/static/css/portal.css
~~~

## Running Tests

1. Enter nix shell in the project root folder to open a shell which is your test environment:
    ~~~Shell
    cd ekklesia-portal
    nix-shell
    ~~~
2. Compile translations:
    ~~~Shell
    ipython makebabel.ipy compile
    ~~~
3. Create a config file named `testconfig.yml` using the config template from `tests/testconfig.example.yml`
    Make sure that the database connection string points to an empty + writable database.
4. Initialize the test database:
    ~~~Shell
    python tests/create_test_db.py -c testconfig.yml
    ~~~
6. The tests can be run with `pytest` from the repository root directory.


## Updating The Development Environment

`lorri shell` always installs changed dependencies and tools before entering the development shell which takes some seconds.

When using the `direnv` integration, running `lorri daemon` in the background automatically updates the development shell when something changes.
Press Enter in the development shell to trigger the first daemon build or to see the changes in the shell made by `direnv`.

You can also trigger an update by running `lorri watch --once` if you don't want to run `lorri daemon`.

## Editor / IDE Integration

*Tested with VSCode, Pycharm*

Run this to build the environment:

~~~
./python_dev_env.nix
~~~

This creates a directory 'pyenv' that is similar to a Python virtualenv.
The 'pyenv' should be picked up by the IDE using the Python interpreter in the directory.
A restart may be required.

## Running In Production

A production environment can be built by Nix. The generated output doesn't have additional requirements.
The application can be run by a start script directly or using the Docker image built by Nix.
Static assets are built separately and can be served by the included minimal Nginx.
As for the application itself, we can build a standalone start script or a Docker image.

### Without Docker

- Build and run app with the config file `config.yml`:
    ~~~
    nix-build nix/serve_app.nix -o serve_app && serve_app/bin/run config.yml
    ~~~
- Build static assets and run Nginx:
    ~~~
    nix-build nix/serve_static.nix -o serve_static && serve_static/bin/run
    ~~~
- Build static assets for use with another web server:
    ~~~
    nix-build nix/static_files.nix -o static_files
    ~~~

### With Docker

By default, Docker images are tagged with a version string derived from the last Git tag.
You can set a different tag by adding `--argstr tag mytag` to the `docker*.nix` calls.

- Build and import app image
    ~~~
    ./docker.nix --argstr tag mytag
    docker load -i docker-image-ekklesia-portal.tar
    ~~~
- Build and import static file image
    ~~~
    ./docker_static.nix --argstr tag mytag
    docker load -i docker-image-ekklesia-portal-static.tar
    ~~~
- Run app container
    ~~~
    docker run -p 127.0.0.1:8080:8080 -it -v $(pwd)/config-docker.yml:/config.yml ekklesia-portal:mytag
    ~~~
- Run static file container
    ~~~
    docker run -p 127.0.0.1:8081:8080 -it ekklesia-portal-static:mytag
    ~~~

The app is now served at port 8080 and static files at port 8081 which are
only reachable from localhost (127.0.0.1).


## History

Ekklesia Portal started as an improved implementation of Wikiarguments in Python 3.x using the Flask micro web framework.
The project is now based on the [Morepath](https://github.com/morepath/morepath) web framework and tries to explore ideas from the Ruby project [Trailblazer](https://trailblazer.to).

## License

AGPLv3, see LICENSE

## Authors

* Tobias 'dpausp'
* Joscha ’GamesGamble’
