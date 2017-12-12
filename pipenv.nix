{ pipenv, python36Packages }:

pipenv.overrideAttrs(oldAttrs: rec {
  inherit (oldAttrs) pname;
  name = "${pname}-${version}";
  version = "9.0.0";

  src = python36Packages.fetchPypi {
    inherit pname version;
    sha256 = "11wx4lpbfqwhmvj89y5sbzihw052zz52mlbjpgc44cb5bl4zr96i";
  };
})
