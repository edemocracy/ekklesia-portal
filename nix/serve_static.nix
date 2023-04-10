#!/usr/bin/env -S nix-build -o serve_static
{ pkgs
, lib
, staticFiles
, listen ? "127.0.0.1:8081"
, serverName ? "localhost"
}:
let
  nginx = pkgs.callPackage ./nginx.nix { };
  mimeTypeFile = "${nginx}/conf/mime.types";
  nginxConf = pkgs.writeText
    "nginx.conf"
    (import ./nginx.conf.nix {
      inherit staticFiles listen serverName mimeTypeFile;
    });

  runNginx = pkgs.writeShellScriptBin "run" ''
    echo serving static files with Nginx on ${listen}...
    ${nginx}/bin/nginx -c ${nginxConf}
  '';

in
pkgs.buildEnv {
  name = "ekklesia-portal-serve-static";
  paths = [ runNginx ];
}
