# Build Python package.
# Can be installed in the current user profile with:
# nix-env -if .
{ sources ? null, system ? builtins.currentSystem }:
let
  deps = import ./nix/deps.nix { inherit sources system; };
  inherit (deps) babel mkPoetryApplication python pyProject;
  inherit (deps.pyProject) version;

in mkPoetryApplication {
  projectDir = ./.;
  inherit python version;

  passthru = {
    inherit deps version;
  };

  postInstall = ''
    ${babel}/bin/pybabel compile -d $out/${python.sitePackages}/ekklesia_portal/translations
  '';
}
