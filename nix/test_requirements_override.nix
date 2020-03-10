{ pkgs, python }:

self: super: let

  addBuildInputs = packageName: inputs:
    python.overrideDerivation super."${packageName}" (old: {
      buildInputs = old.buildInputs ++ inputs;
    });

in
{
  inflect = addBuildInputs "inflect" [ self.toml ];
  faker = addBuildInputs "faker" [ self.toml ];
  pytest-mock = addBuildInputs "pytest-mock" [ self.setuptools-scm ];
}
