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
