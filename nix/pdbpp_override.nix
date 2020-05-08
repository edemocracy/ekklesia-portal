{ pkgs, python }:

self: super: let

  addBuildInputs = packageName: inputs:
    python.overrideDerivation super."${packageName}" (old: {
      buildInputs = old.buildInputs ++ inputs;
    });

in
{
  fancycompleter = addBuildInputs "fancycompleter" [ self.setupmeta self.setuptools-scm ];
  pdbpp = addBuildInputs "pdbpp" [ self.setuptools-scm ];
}
