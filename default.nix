# Build Python package.
# Can be installed in the current user profile with:
# nix-env -if .
{ sources ? null }:
let
  deps = import ./nix/deps.nix { inherit sources; };
  inherit (deps) buildPythonApplication lib pkgs babel installLibs testLibs;
  version = import ./nix/version.nix;

in buildPythonApplication rec {
  pname = "ekklesia-portal";
  inherit version;

  src = pkgs.nix-gitignore.gitignoreSource
          [ "cookiecutter" "mockup" "old" ]
          ./.;

  doCheck = false;
  catchConflicts = false;

  buildInputs = testLibs;
  propagatedBuildInputs = installLibs;

  postInstall = ''
    ${babel}/bin/pybabel compile -d $out/lib/*/site-packages/ekklesia_portal/translations
  '';

  passthru = {
    inherit deps version;
    inherit (deps) python;
  };
}
