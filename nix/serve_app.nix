#!/usr/bin/env -S nix-build -o serve_app
{ pkgs
, lib
, app
, gunicorn
, appConfigFile ? null
, listen ? "127.0.0.1:10080"
, tmpdir ? null
, system ? builtins.currentSystem
}:
let
  inherit (app) dependencyEnv src;
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

  runGunicorn = pkgs.writeShellScriptBin "ekklesia-portal-serve-app" ''
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
    ${lib.optionalString (tmpdir != null) "export TMPDIR=${tmpdir}"}
    cd ${src}
    ${dependencyEnv}/bin/python "$@"
  '';

in
pkgs.buildEnv {
  ignoreCollisions = true;
  name = "ekklesia-portal-serve-app";
  paths = [ runGunicorn runMigrations runAlembic runPython ];
}
