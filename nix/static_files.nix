{ sources ? null }:
let
  deps = import ./deps.nix { inherit sources; };
  inherit (deps) lib pkgs sassc javascriptDeps webfontsPath sassPath deform python;
  inherit (deps.pyProject) version;

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
  cp -r ${deform}/${python.sitePackages}/deform/static $out/deform

''
