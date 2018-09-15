Ekklesia Portal
===============

Portal of the Ekklesia e-democracy platform.

Features
--------

* 


Tech Stack
----------

* Backend: Python 3.7
* Web framework: [Morepath](https://github.com/morepath/morepath)
* Frontend: Pyjade, Bootstrap 4, SASS, Javascript
* Database: PostgreSQL 10
* Package management: [Nix Package Manager](https://nixos.org/nix), [Pipenv](https://pipenv.org)


Development
-----------

### Quick Start

The shell environment for development can be prepared using the [Nix Package Manager](https://nixos.org/nix).
It includes Python 3.7, PostgreSQL 10, a SASS compiler and [Pipenv](https://pipenv.org) which is used to install Python development dependencies.

1. Install Nix and run `nix-shell` in the project root folder to open a shell which makes the shell environment available.
2. Inside the Nix shell, install Python dependencies with `pipenv install --python 3 --dev`.
3. Make Python dependencies available: `pipenv shell`
4. Create a config file named `config.yml` using the config template from `src/ekklesia_portal/config.example.yml` or skip this to use the default settings from `src/ekklesia_portal/default_settings.py`.
5. The development server can be run with a custom config file by executing `python src/ekklesia_portal/runserver.py --debug -c config.yml`


Histoy
-------

Ekklesia Portal started as an improved implementation of Wikiarguments in Python 3.x using the Flask micro web framework.
The project is now based on the [Morepath](https://github.com/morepath/morepath) web framework and tries to explore ideas from the Ruby project [Trailblazer](https://trailblazer.to).

License
-------

AGPLv3, see LICENSE

Authors
-------

Tobias 'dpausp'

