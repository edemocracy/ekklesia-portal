#!/usr/bin/env -S nix-build -o docker-image.tar
# Run this file with ./docker.nix.
# It creates a docker image archive called docker-image.tar.
# Import into docker with:
# docker load -i docker-image.tar
{ sources ? null }:
let
  ekklesia-portal = import ./. { inherit sources; };
  deps = ekklesia-portal.deps;

in deps.pkgs.dockerTools.buildLayeredImage {
  name = "ekklesia-portal";
  tag = "latest";

  config = {
    Entrypoint = "${deps.gunicorn}/bin/gunicorn";
    Cmd = [
      "ekklesia_portal.app:make_wsgi_app()"
      "--pythonpath"
      "${deps.python}/lib/python3.7/site-packages,${ekklesia-portal}/lib/python3.7/site-packages"
      "-b 0.0.0.0:8080"
    ];
  };
}
