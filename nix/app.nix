# Build the actual Python application using poetry2nix.
{ babel
, mkPoetryApplication
, pyProject
, python
, ...
}:

mkPoetryApplication {
  projectDir = ./..;
  inherit python;

  passthru = {
    inherit (pyProject) version;
  };

  postInstall = ''
    ${babel}/bin/pybabel compile -d $out/${python.sitePackages}/ekklesia_portal/translations
  '';
}


