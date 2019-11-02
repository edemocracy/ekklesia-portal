#!/usr/bin/env -S nix-build -o docker-image-ekklesia-portal-static.tar
# Run this file: ./docker_static.nix.
# It creates a docker image archive called docker-image-ekklesia-portal-static.tar.
# Import into docker with:
# docker load -i docker-image-ekklesia-portal-static.tar
{ sources ? null }:

with builtins;

let
  serveStatic = import ./nix/serve_static.nix {
    inherit sources;
    listen = "0.0.0.0:8080";
  };

  deps = import ./nix/deps.nix { inherit sources; };
  inherit (deps) pkgs;
  version = import ./nix/git_version.nix { inherit pkgs; };
  user = "nginx";
  passwd = pkgs.writeTextDir "etc/passwd" ''
    ${user}:x:10:10:${user}:/:/noshell
  '';
in

pkgs.dockerTools.buildLayeredImage {
  name = "ekklesia-portal-static";
  tag = trace "Tagging image with ${version}" version;
  contents = [ passwd ];

  config = {
    ExposedPorts = { "8080/tcp" = {}; };
    User = user;
    Entrypoint = "${serveStatic}/bin/run";
    Cmd = [ "# runs nginx" ];
  };
}
