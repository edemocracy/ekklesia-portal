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
