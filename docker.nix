#!/usr/bin/env -S nix-build -o docker-image-ekklesia-portal.tar
# Run this file: ./docker.nix
# It creates a docker image archive called docker-image-ekklesia-portal.tar.
# Default tag is the git version. You can set a custom tag with:
# ./docker.nix --argstr tag mytag
# Import into docker with:
# docker load -i docker-image-ekklesia-portal.tar
{ sources ? null, tag ? null }:

with builtins;

let
  serveApp = import ./nix/serve_app.nix {
    inherit sources;
    appConfigFile = "/config.yml";
    listen = "0.0.0.0:8080";
    tmpdir = "/dev/shm";
  };

  deps = import ./nix/deps.nix { inherit sources; };
  inherit (deps) pkgs;
  version = import ./nix/git_version.nix { inherit pkgs; };
  user = "ekklesia-portal";
  passwd = pkgs.writeTextDir "etc/passwd" ''
    ${user}:x:10:10:${user}:/:/noshell
  '';
in

pkgs.dockerTools.buildLayeredImage {
  name = "ekklesia-portal";
  contents = [ passwd ];
  tag =
    if tag == null then
      trace "Automatically tagging image with version ${version}" version
    else
      trace "Tagging image with custom tag '${tag}'" tag;

  config = {
    ExposedPorts = { "8080/tcp" = {}; };
    User = user;
    Entrypoint = "${serveApp}/bin/run";
    Cmd = [ "# runs gunicorn" ];
  };
}
