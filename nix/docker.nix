#!/usr/bin/env -S nix-build -o docker-image-ekklesia-portal.tar
# Run this file: ./docker.nix
# It creates a docker image archive called docker-image-ekklesia-portal.tar.
# Default tag is the git version. You can set a custom tag with:
# ./docker.nix --argstr tag mytag
# Import into docker with:
# docker load -i docker-image-ekklesia-portal.tar
{ pkgs, serveApp }:

let
  user = "ekklesia-portal";
  passwd = pkgs.writeTextDir "etc/passwd" ''
    ${user}:x:10:10:${user}:/:/noshell
  '';
in

pkgs.dockerTools.buildLayeredImage {
  name = "ekklesia-portal";
  contents = [ passwd ];
  config = {
    ExposedPorts = { "8080/tcp" = { }; };
    User = user;
    Entrypoint = [ "${serveApp}/bin/ekklesia-portal-serve-app" ];
    Cmd = [ "# runs gunicorn" ];
  };
}
