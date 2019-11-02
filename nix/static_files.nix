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
  outs=$out/static
  mkdir -p $outs
  #cp -r $src/static/img $outs
  cp -r ${javascriptDeps}/js $outs
  cp -r ${webfontsPath} $outs
  cp -r ${deform}/lib/python3.7/site-packages/deform/static $outs/deform

  mkdir $outs/css
  sassc -I $sassPath $src/sass/portal.sass $outs/css/portal.css
''
