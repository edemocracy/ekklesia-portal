{ pkgs, python }:

with pkgs.python37Packages;

let
  addBuiltInputs = packageName: inputs:
    {
      "${packageName}" = python.overrideDerivation super."${packageName}" (old: {
        buildInputs = old.buildInputs ++ inputs;
      });
    };
in

self: super: {
  inherit (pkgs) zsh;

  "setuptools-scm" = setuptools_scm;

  "importlib-metadata" = python.overrideDerivation super."importlib-metadata" (old: {
    buildInputs = old.buildInputs ++ [ setuptools_scm ];
  });

  "py" = python.overrideDerivation super."py" (old: {
    buildInputs = old.buildInputs ++ [ setuptools_scm ];
  });

  "pytest-mock" = python.overrideDerivation super."pytest-mock" (old: {
    buildInputs = old.buildInputs ++ [ setuptools_scm ];
  });

  "zipp" = python.overrideDerivation super."zipp" (old: {
    buildInputs = old.buildInputs ++ [ pytestrunner ];
  });

  "faker" = python.overrideDerivation super."faker" (old: {
    buildInputs = old.buildInputs ++ [ pytestrunner ];
  });
}
