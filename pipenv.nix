{ pipenv, python36Packages }:

pipenv.overrideAttrs(oldAttrs: rec {
  inherit (oldAttrs) pname;
  name = "${pname}-${version}";
  version = "11.10.1";

  src = python36Packages.fetchPypi {
    inherit pname version;
    sha256 = "1jw25l66j7g68wq7pdg460y9ij868li12li57pn3avm3nvad9kws";
  };
})
