# Ekklesia Portal

Portal of the Ekklesia e-democracy platform.

## Tech Stack

* Backend: [Python 3.7](https://www.python.org)
* Web framework: [Morepath](http://morepath.readthedocs.org )
* Frontend: Pyjade, [Bootstrap 4](https://getbootstrap.com), [Sass](https://sass-lang.com), Javascript
* Database: [PostgreSQL 11](https://www.postgresql.com)
* Package management: [Nix Package Manager](https://nixos.org/nix)

## Development

### Quick Start

The shell environment for development can be prepared using the Nix Package Manager.
It includes Python 3.7, PostgreSQL 11, development / testing tools and dependencies for the project itself. 
The following instructions assume that the Nix package manager is already installed, `nix-shell` is available in PATH and an empty + writable PostgreSQL database can be accessed somehow.

1. Clone the repository with:
    ~~~Shell
    git clone https://github.com/Piratenpartei/ekklesia-portal
    ~~~
2. Enter nix shell in the project root folder to open a shell which is your dev environment:
    ~~~Shell
    cd ekklesia-portal
    nix-shell
    ~~~
3. Compile translations:
    ~~~Shell
    ipython makebabel.ipy compile
    ~~~
4. Create a config file named `config.yml` using the config template from `src/ekklesia_portal/config.example.yml`
    or skip this to use the default settings from `src/ekklesia_portal/default_settings.py`.
    Make sure that the database connection string points to an empty + writable database.
5. Initialize the test database with a custom config file: 
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
The repository includes compiled CSS so you don't have to run the following command if you are not changing the Sass files.

Generate CSS with:

~~~Shell
sassc src/ekklesia_portal/sass/portal.sass \
  src/ekklesia_portal/static/css/portal.css
~~~

## History

Ekklesia Portal started as an improved implementation of Wikiarguments in Python 3.x using the Flask micro web framework.
The project is now based on the [Morepath](https://github.com/morepath/morepath) web framework and tries to explore ideas from the Ruby project [Trailblazer](https://trailblazer.to).

## License

AGPLv3, see LICENSE

## Authors

* Tobias 'dpausp'
* Joscha ’GamesGamble’
