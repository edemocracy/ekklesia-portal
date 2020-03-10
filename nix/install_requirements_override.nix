{ pkgs, python }:

self: super: let

  addBuildInputs = packageName: inputs:
    python.overrideDerivation super."${packageName}" (old: {
      buildInputs = old.buildInputs ++ inputs;
    });

  py = pkgs.python37Packages;
in
{
  more-babel-i18n = addBuildInputs "more-babel-i18n" [ py.setuptools_scm ];
  more-browser-session = addBuildInputs "more-browser-session" [ py.setuptools_scm ];
  munch = addBuildInputs "munch" [ py.pbr ];
  pyrsistent = addBuildInputs "pyrsistent" [ py.pbr ];
}
