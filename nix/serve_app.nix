#!/usr/bin/env -S nix-build -o serve_app
{ sources ? null,
  appConfigFile ? null,
  listen ? "127.0.0.1:8080",
  tmpdir ? null
}:
let
  ekklesia-portal = import ../. { inherit sources; };
  inherit (ekklesia-portal) dependencyEnv deps src;
  inherit (deps) pkgs gunicorn lib;
  pythonpath = "${dependencyEnv}/${dependencyEnv.sitePackages}";

  exportConfigEnvVar =
    lib.optionalString
      (appConfigFile != null)
      "export EKKLESIA_PORTAL_CONFIG=\${EKKLESIA_PORTAL_CONFIG:-${appConfigFile}}";

  gunicornConf = pkgs.writeText
                "gunicorn_config.py"
                (import ./gunicorn_config.py.nix {
                   inherit listen pythonpath;
                });

  runGunicorn = pkgs.writeShellScriptBin "run" ''
    ${exportConfigEnvVar}
    ${lib.optionalString (tmpdir != null) "export TMPDIR=${tmpdir}"}

    ${gunicorn}/bin/gunicorn -c ${gunicornConf} \
      "ekklesia_portal.app:make_wsgi_app()"
  '';

  runMigrations = pkgs.writeShellScriptBin "migrate" ''
    ${runAlembic}/bin/alembic upgrade head
  '';

  runAlembic = pkgs.writeShellScriptBin "alembic" ''
    ${exportConfigEnvVar}
    cd ${src}
    ${dependencyEnv}/bin/alembic "$@"
  '';

  runPython = pkgs.writeShellScriptBin "python" ''
    ${exportConfigEnvVar}
    cd ${src}
    ${dependencyEnv}/bin/python "$@"
  '';

in pkgs.buildEnv {
  name = "ekklesia-portal-serve-app";
  paths = [ runGunicorn runMigrations runAlembic runPython ];
}
