#!/usr/bin/env -S nix-build -o serve_app
{ sources ? null,
  appConfigFile ? null,
  listen ? "127.0.0.1:8000",
  tmpdir ? null
}:
let
  ekklesia-portal = import ../. { inherit sources; };
  deps = ekklesia-portal.deps;
  inherit (deps) pkgs gunicorn python lib;
  pythonpath = "${python}/lib/python3.7/site-packages,${ekklesia-portal}/lib/python3.7/site-packages";

  gunicornConf = pkgs.writeText
                "gunicorn_config.py"
                (import ./gunicorn_config.py.nix {
                   inherit listen pythonpath;
                });

  runGunicorn = pkgs.writeShellScriptBin "run" ''
    app_config=${if appConfigFile == null then "`pwd`/$1" else appConfigFile}
    ${lib.optionalString (tmpdir != null) "export TMPDIR=${tmpdir}"}

    ${gunicorn}/bin/gunicorn -c ${gunicornConf} \
      "ekklesia_portal.app:make_wsgi_app(settings_filepath='$app_config')"
  '';

in pkgs.buildEnv {
  name = "ekklesia-portal-serve-app";
  paths = [ runGunicorn ];
}
