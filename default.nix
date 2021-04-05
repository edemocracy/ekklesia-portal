# Build Python package.
# Can be installed in the current user profile with:
# nix-env -if .
{ sources ? null, system ? builtins.currentSystem }:
let
  deps = import ./nix/deps.nix { inherit sources system; };
  inherit (deps) babel pkgs mkPoetryApplication python pyProject;
  inherit (deps.pyProject) version;
  src = pkgs.nix-gitignore.gitignoreSource
    [ "cookiecutter" ]
    ./.;

in mkPoetryApplication {
  doCheck = false;
  projectDir = ./.;
  inherit python src version;

  passthru = {
    inherit deps src version;
  };

  postInstall = ''
    ${babel}/bin/pybabel compile -d $out/${python.sitePackages}/ekklesia_portal/translations
  '';
}
