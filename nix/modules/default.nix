{ config, pkgs, lib, ... }:

with builtins;

let
  cfg = config.services.ekklesia.portal;

  defaultConfig = {

  };

  appConfigFile =
    pkgs.writeText "ekklesia-portal-config.json"
      (toJSON
        (lib.recursiveUpdate defaultConfig cfg.extraConfig));

  serveApp = import ../serve_app.nix {
    inherit appConfigFile;
    listen = "${cfg.address}:${toString cfg.port}";
    tmpdir = "/tmp";
  };

  staticFiles = import ../static_files.nix { };

  ekklesiaPortalConfig = pkgs.writeScriptBin "ekklesia-portal-config" ''
    systemctl cat ekklesia-portal.service | grep X-ConfigFile | cut -d"=" -f2
  '';

  ekklesiaPortalShowConfig = pkgs.writeScriptBin "ekklesia-portal-show-config" ''
    cat `${ekklesiaPortalConfig}/bin/ekklesia-portal-config`
  '';

in {
  options.services.ekklesia.portal = with lib; {

    enable = mkEnableOption "Enable the portal component of the Ekklesia e-democracy platform";

    user = mkOption {
      type = types.str;
      default = "ekklesia-portal";
      description = "User to run ekklesia-portal.";
    };

    group = mkOption {
      type = types.str;
      default = "ekklesia-portal";
      description = "Group to run ekklesia-portal.";
    };

    port = mkOption {
      type = types.int;
      default = 10000;
      description = "Port for gunicorn app server";
    };

    address = mkOption {
      type = types.str;
      default = "127.0.0.1";
      description = "Address for gunicorn app server";
    };

    extraConfig = mkOption {
      type = types.attrs;
      default = {};
      description = "Additional config options given as attribute set.";
    };

  };

  config = lib.mkIf cfg.enable {

    environment.systemPackages = [ ekklesiaPortalConfig ekklesiaPortalShowConfig ];

    users.users.ekklesia-portal = { };
    users.groups.ekklesia-portal = { };

    systemd.services.ekklesia-portal = {

      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      serviceConfig = {
        User = cfg.user;
        Group = cfg.group;
        ExecStartPre = "${serveApp}/bin/migrate";
        ExecStart = "${serveApp}/bin/run";
        X-ConfigFile = appConfigFile;
      };

    };

  };
}
