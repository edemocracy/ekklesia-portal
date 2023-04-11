#!/usr/bin/env -S nix-build -o docker-image-ekklesia-portal-static.tar
# Run this file: ./docker_static.nix.
# Default tag is the git version. You can set a custom tag with:
# ./docker_static.nix --argstr tag mytag
# It creates a docker image archive called docker-image-ekklesia-portal-static.tar.
# Import into docker with:
# docker load -i docker-image-ekklesia-portal-static.tar
{ pkgs, serveStatic }:

let
  user = "nginx";
  passwd = pkgs.writeTextDir "etc/passwd" ''
    ${user}:x:10:10:${user}:/:/noshell
  '';
in

pkgs.dockerTools.buildLayeredImage {
  name = "ekklesia-portal-static";
  contents = [ passwd ];

  config = {
    ExposedPorts = { "8080/tcp" = { }; };
    User = user;
    Entrypoint = [ "${serveStatic}/bin/run" ];
    Cmd = [ "# runs nginx" ];
  };
}
