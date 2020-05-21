{ sources ? null }:
let
  deps = import ./deps.nix { inherit sources; };
  inherit (deps) lib pkgs sassc javascriptDeps webfontsPath sassPath deform;
  version = import ./version.nix;

in
pkgs.runCommand "ekklesia-portal-static-${version}" {
  buildInputs = [ sassc ];
  inherit sassPath;
  src = ../src/ekklesia_portal;
} ''
  mkdir -p $out/css
  sassc -I $sassPath $src/sass/portal.sass $out/css/portal.css

  #cp -r $src/static/img $out
  cp -r ${javascriptDeps}/js $out
  cp -r ${webfontsPath} $out
  cp -r ${deform}/lib/python3.8/site-packages/deform/static $out/deform

''
