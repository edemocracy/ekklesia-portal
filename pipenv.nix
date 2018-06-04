{ pipenv, python36Packages }:

pipenv.overrideAttrs(oldAttrs: rec {
  inherit (oldAttrs) pname;
  name = "${pname}-${version}";
  version = "2018.5.18";

  src = python36Packages.fetchPypi {
    inherit pname version;
    sha256 = "1knyknmykjj7gixdpfyns77sv4mizl68addk09ajmw9z5aqaif84";
  };
})
