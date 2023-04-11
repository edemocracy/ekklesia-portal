{ pkgs
, deform
, ekklesia-common
, javascriptDeps
, pyProject
, python
, sassPath
, sassc
, webfontsPath
, ...
}:

with builtins;

let
  inherit (pyProject.tool.poetry) version;
in
pkgs.runCommand "ekklesia-portal-static-${version}"
{
  buildInputs = [ sassc ];
  inherit sassPath;
  src = ../src/ekklesia_portal;
} ''
  mkdir -p $out/css
  sassc -I $sassPath $src/sass/portal.sass $out/css/portal.css

  #cp -r $src/static/img $out
  cp $src/static/favicon.ico $out
  cp -r ${javascriptDeps}/js $out
  cp -r ${webfontsPath} $out
  cp -r ${deform}/${python.sitePackages}/deform/static $out/deform
  mkdir $out/debug
  cp ${ekklesia-common}/lib/python*/site-packages/ekklesia_common/debug/static/*.{png,css,js} $out/debug
''
