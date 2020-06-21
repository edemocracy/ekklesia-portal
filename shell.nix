{ sources ? null }:
let
  deps = import ./nix/deps.nix { inherit sources; };
  inherit (deps) pkgs;
  inherit (pkgs) lib stdenv;
  caBundle = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";

in pkgs.mkShell {
  name = "ekklesia-portal";
  buildInputs = deps.shellInputs;
  shellHook = ''
    export PATH=${deps.shellPath}:$PATH
    export PYTHONPATH=./src:../ekklesia-common/src
    # A pure nix shell breaks SSL for git and nix tools which is fixed by setting
    # the path to the certificate bundle.
    export SSL_CERT_FILE=${caBundle}
    export NIX_SSL_CERT_FILE=${caBundle}
    # Make ZIP happy for wheels, doesn't support timestamps before 1980.
    export SOURCE_DATE_EPOCH=315532800
    export JS_PATH=${deps.jsPath}
    export SASS_PATH=${deps.sassPath}
    export WEBFONTS_PATH=${deps.webfontsPath}
  '' +
  lib.optionalString (pkgs.stdenv.hostPlatform.libc == "glibc") ''
    export LOCALE_ARCHIVE=${deps.glibcLocales}/lib/locale/locale-archive
  '';
}
