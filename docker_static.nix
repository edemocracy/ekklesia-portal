#!/usr/bin/env -S nix-build -o docker-image-ekklesia-portal-static.tar
# Run this file: ./docker_static.nix.
# Default tag is the git version. You can set a custom tag with:
# ./docker_static.nix --argstr tag mytag
# It creates a docker image archive called docker-image-ekklesia-portal-static.tar.
# Import into docker with:
# docker load -i docker-image-ekklesia-portal-static.tar
{ sources ? null, tag ? null }:

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
  tag =
    if tag == null then
      trace "Automatically tagging image with version ${version}" version
    else
      trace "Tagging image with custom tag '${tag}'" tag;
  contents = [ passwd ];

  config = {
    ExposedPorts = { "8080/tcp" = {}; };
    User = user;
    Entrypoint = [ "${serveStatic}/bin/run" ];
    Cmd = [ "# runs nginx" ];
  };
}
