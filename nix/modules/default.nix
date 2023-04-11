{ config, pkgs, lib, ... }:

with builtins;

let
  cfg = config.services.ekklesia.portal;

  configFilename = "ekklesia-portal-config.json";

  configInput =
    pkgs.writeText configFilename
      (toJSON cfg.extraConfig);

  serveApp = pkgs.ekklesia-portal-serve-app.override {
    appConfigFile = "/run/ekklesia-portal/${configFilename}";
    listen = "${cfg.address}:${toString cfg.port}";
    tmpdir = "/tmp";
    inherit (config.nixpkgs.localSystem) system;
  };

  ekklesiaPortalConfig = pkgs.writeScriptBin "ekklesia-portal-config" ''
    systemctl cat ekklesia-portal.service | grep X-ConfigFile | cut -d"=" -f2
  '';

  ekklesiaPortalShowConfig = pkgs.writeScriptBin "ekklesia-portal-show-config" ''
    cat `${ekklesiaPortalConfig}/bin/ekklesia-portal-config`
  '';

in
{
  options.services.ekklesia.portal = with lib; {

    enable = mkEnableOption "Enable the portal component of the Ekklesia e-democracy platform";

    debug = mkOption {
      type = types.bool;
      default = false;
      description = ''
        (UNSAFE) Activate debugging mode for this module.
        Currently shows how secrets are replaced in the pre-start script.
      '';
    };

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

    configFile = mkOption {
      internal = true;
      type = with types; nullOr path;
      default = null;
    };

    staticFiles = mkOption {
      internal = true;
      type = with types; nullOr path;
      default = null;
    };

    app = mkOption {
      internal = true;
      type = with types; nullOr path;
      default = null;
    };

    browserSessionSecretKeyFile = mkOption {
      type = types.str;
      description = "Path to file containing the secret key for browser session signing";
      default = "/var/lib/ekklesia-portal/browser-session-secret-key";
    };

    secretFiles = mkOption {
      type = types.attrs;
      default = { };
      description = ''
        Arbitrary secrets that should be read from a file and
        inserted in the config on startup. Expects an attrset with
        the variable name to replace and a file path to the secret.
      '';
      example = {
        some_secret_api_key = "/var/lib/ekklesia-portal/some-secret-api-key";
      };
    };

    extraConfig = mkOption {
      type = types.attrs;
      default = { };
      description = "Additional config options given as attribute set.";
    };

  };

  config = lib.mkIf cfg.enable {

    services.ekklesia.portal.configFile = configInput;
    services.ekklesia.portal.app = serveApp;
    services.ekklesia.portal.staticFiles = pkgs.ekklesia-portal-static;

    environment.systemPackages = [ ekklesiaPortalConfig ekklesiaPortalShowConfig ];

    users.users.ekklesia-portal = {
      isSystemUser = true;
      group = "ekklesia-portal";
    };
    users.groups.ekklesia-portal = { };

    systemd.services.ekklesia-portal = {

      description = "Ekklesia E-Democracy Portal";
      after = [ "network.target" "postgresql.service" ];
      wantedBy = [ "multi-user.target" ];
      stopIfChanged = false;

      preStart =
        let
          replaceDebug = lib.optionalString cfg.debug "-vv";
          secrets = cfg.secretFiles // {
            browser_session_secret_key = cfg.browserSessionSecretKeyFile;
          };
          replaceSecret = file: var: secretFile:
            "${pkgs.replace}/bin/replace-literal -m 1 ${replaceDebug} -f -e @${var}@ $(< ${secretFile}) ${file}";
          replaceCfgSecret = var: secretFile: replaceSecret "$cfgdir/${configFilename}" var secretFile;
          secretReplacements = lib.mapAttrsToList (k: v: replaceCfgSecret k v) cfg.secretFiles;
        in
        ''
          echo "Prepare config file..."
          cfgdir=$RUNTIME_DIRECTORY
          chmod u+w -R $cfgdir
          cp ${configInput} $cfgdir/${configFilename}

          ${lib.concatStringsSep "\n" secretReplacements}

          echo "Run database migrations if needed..."
          ${serveApp}/bin/migrate
          echo "Pre-start finished."
        '';

      serviceConfig = {
        User = cfg.user;
        Group = cfg.group;
        ExecStart = "${serveApp}/bin/ekklesia-portal-serve-app";
        RuntimeDirectory = "ekklesia-portal";
        StateDirectory = "ekklesia-portal";
        RestartSec = "5s";
        Restart = "always";
        X-ConfigFile = configInput;
        X-App = serveApp;
        X-StaticFiles = cfg.staticFiles;

        DeviceAllow = [
          "/dev/stderr"
          "/dev/stdout"
        ];

        AmbientCapabilities = [ "CAP_NET_BIND_SERVICE" ];
        CapabilityBoundingSet = [ "CAP_NET_BIND_SERVICE" ];
        DevicePolicy = "strict";
        LockPersonality = true;
        NoNewPrivileges = true;
        PrivateDevices = true;
        PrivateTmp = true;
        PrivateUsers = true;
        ProtectClock = true;
        ProtectControlGroups = true;
        ProtectHome = true;
        ProtectHostname = true;
        ProtectKernelLogs = true;
        ProtectKernelModules = true;
        ProtectKernelTunables = true;
        ProtectSystem = "strict";
        RemoveIPC = true;
        RestrictAddressFamilies = [ "AF_INET" "AF_INET6" "AF_UNIX" ];
        RestrictNamespaces = true;
        RestrictRealtime = true;
        RestrictSUIDSGID = true;
        SystemCallArchitectures = "native";
        SystemCallFilter = [
          # deny the following syscall groups
          "~@clock"
          "~@debug"
          "~@module"
          "~@mount"
          "~@reboot"
          "~@cpu-emulation"
          "~@swap"
          "~@obsolete"
          "~@resources"
          "~@raw-io"
        ];
        UMask = "077";

      };

      unitConfig = {
        Documentation = [
          "https://github.com/edemocracy/ekklesia-portal"
          "https://ekklesiademocracy.org"
        ];
      };
    };

  };
}
