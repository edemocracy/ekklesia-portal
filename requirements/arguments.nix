{ pkgs ? import <nixpkgs> {}
}:

let
  req = import ./requirements.nix {};
  inherit (pkgs) lib;
  
  binPathInputs = lib.filter (x: lib.isDerivation x) (lib.attrValues req.pkgs);

  paths = map ( p: "${p}/bin" ) binPathInputs;
  buildPathVar = lib.concatMapStringsSep "\n" (p: "addToSearchPath _PATH ${p}") paths;

  shellHook = buildPathVar + "\n" + ''
    export PATH=$_PATH
  '';
  
  postBuild = buildPathVar + "\n" + ''
    makeWrapper $out/bin/python3 $out/bin/python-wrapper --set PATH $_PATH'';

  interpreter = if lib.inNixShell 
  then 
    lib.overrideDerivation req.interpreter (attrs: { inherit shellHook; })
  else
    req.interpreter.override { inherit postBuild; };

in {
  inherit (req) pkgs;
  inherit interpreter;
}
