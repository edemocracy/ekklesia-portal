# This Flake uses devenv and flake-parts.
# https://devenv.sh
# https://flake.parts
# https://devenv.sh/guides/using-with-flake-parts/
{
  description = "ekklesia-portal";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    devenv.url = "github:cachix/devenv";
    poetry2nix = {
      url = "github:dpausp/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix2container.url = "github:nlewo/nix2container";
    nix2container.inputs.nixpkgs.follows = "nixpkgs";
    mk-shell-bin.url = "github:rrbutani/nix-mk-shell-bin";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
        inputs.flake-parts.flakeModules.easyOverlay
      ];
      systems = [ "x86_64-linux" "x86_64-darwin" "aarch64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }:
        let
          deps = import ./nix/deps.nix {
            poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
            inherit pkgs;
          };

          app = pkgs.callPackage ./nix/app.nix deps;

          serveApp = pkgs.callPackage ./nix/serve_app.nix {
            inherit app;
            inherit (deps) gunicorn;
          };

          docker = pkgs.callPackage ./nix/docker.nix {
            serveApp = serveApp.override {
              appConfigFile = "/config.yml";
              listen = "0.0.0.0:8080";
              tmpdir = "/dev/shm";
            };
          };

          staticFiles = pkgs.callPackage ./nix/static_files.nix deps;

          serveStatic = pkgs.callPackage ./nix/serve_static.nix {
            inherit staticFiles;
          };

          dockerStatic = pkgs.callPackage ./nix/docker_static.nix {
            serveStatic = serveStatic.override {
              listen = "0.0.0.0:8080";
            };
          };

          venv = pkgs.buildEnv {
            name = "ekklesia-portal-venv";
            ignoreCollisions = true;
            paths = with deps;
              [ pythonDev ] ++
              linters;
          };
        in
        {
          # Per-system attributes can be defined here. The self' and inputs'
          # module parameters provide easy access to attributes of the same
          # system.
          # The Nix overlay is available as `overlays.default`.
          overlayAttrs = {
            inherit (config.packages)
              ekklesia-portal
              ekklesia-portal-static
              ekklesia-portal-serve-app;
          };

          checks = {
            inherit (config.packages) ekklesia-portal-serve-app;
          };

          formatter = pkgs.nixpkgs-fmt;


          packages = {
            # The `nix run` command uses the `default` attribute here.
            # Runs the application using the `gunicorn` app server.
            default = serveApp;
            # Build container images and Python 'virtualenv'.
            inherit docker dockerStatic venv;
            # ekklesia-portal-* packages are also exported via the default overlay.
            ekklesia-portal = app;
            ekklesia-portal-static = staticFiles;
            ekklesia-portal-serve-app = serveApp;
          };

          devenv.shells.default =
            {
              name = "ekklesia-portal";
              env = {
                PYTHONPATH = "./src:../ekklesia-common/src";
                JS_PATH = deps.jsPath;
                SASS_PATH = deps.sassPath;
                WEBFONTS_PATH = deps.webfontsPath;
              };

              packages = deps.shellInputs;

              scripts = {
                build_python_venv.exec = ''
                  nix build .#venv -o venv
                  echo "Created directory 'venv' which is similar to a Python virtualenv."
                  echo "Provides linters and a Python interpreter with runtime dependencies and test tools."
                  echo "The 'venv' should be picked up py IDE as a possible project interpreter (restart may be required)."
                  echo "Tested with VSCode, Pycharm."
                '';
                build_docker_app.exec = ''
                  out=docker-image-ekklesia-portal.tar.gz
                  nix build .#docker -o $out
                  echo "Built container image for the application".
                  echo "Load the image with:"
                  echo "docker load -i $out"
                '';
                build_docker_static.exec = ''
                  out=docker-image-ekklesia-portal-static.tar.gz
                  nix build .#dockerStatic -o $out
                  echo "Built container image for the static files (assets)".
                  echo "Load the image with:"
                  echo "docker load -i $out"
                '';
                build_docker.exec = ''
                  build_docker_app
                  build_docker_static
                '';
                run_dev.exec = ''
                  python src/ekklesia_portal/runserver.py -b localhost --reload -p 8080 -c config.yml | tee run_dev.log.json | eliot-tree -l0
                '';
                debug_dev.exec = ''
                  python src/ekklesia_portal/runserver.py -b localhost -p 8080 -c config.yml --debug
                '';
                create_dev_db.exec = ''
                  python tests/create_test_db.py --config-file config.yml
                '';
                create_test_db.exec = ''
                  python tests/create_test_db.py
                '';
                doit_auto.exec = ''
                  echo "Recompiling CSS and translation files if source files change..."
                  ls src/ekklesia_portal/translations/*/*/*.po src/ekklesia_portal/sass/*.sass | entr doit
                '';
                help.exec = ''
                  cat << END
                  # Development Shell Commands
                  (standard tools + commands defined in flake.nix)

                  ## Basic
                  doit                     Build CSS and translation files (once).
                  create_test_db           Set up PostgreSQL database for testing, using config.yml.
                  pytest                   Run Python test suite.
                  run_dev                  Run application in dev mode with formatted log output.

                  ## Development
                  doit_auto                Build CSS and translation files (when inputs change).
                  doit babel_extractupdate Extract translatable strings from code.
                  debug_dev                Debug application in dev mode (use this with breakpoints).
                  build_python_venv        Build 'virtualenv' for IDE integration.
                  console                  Run IPython REPL for interaction with application objects.

                  ## Container
                  build_docker             Build both container images, for application and static file serving.
                  build_docker_app         Build container image for serving the application.
                  build_docker_static      Build container image for service static files (assets).
                  END
                '';
              };
            };

        };

      flake = {
        # The usual flake attributes can be defined here, including system-
        # agnostic ones like nixosModule and system-enumerating ones, although
        # those are more easily expressed in perSystem.

        # Using this NixOS module requires the default overlay from here.
        # Example, when `ekklesiaPortal` is the Flake:
        # nixpkgs.overlays = [ ekklesiaPortal.overlays.default ];
        # imports = [ ekklesiaPortal.nixosModules.default ];
        nixosModules.default = import nix/modules/default.nix;
      };
    };
}
