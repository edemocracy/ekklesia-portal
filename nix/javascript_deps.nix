{ pkgs }:
let
  lib = pkgs.lib;
  libs = with pkgs; {

    popper = (fetchurl {
      url = "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.js";
      sha256 = "1bvfn8nrzc0rp0zslsdp7hpjpd80k9h82dfhjb69m16117brzsn6";
    });

    jquery = (fetchurl {
      url = "https://code.jquery.com/jquery-3.4.1.js";
      sha256 = "0mdxjn1lsjs09m2rlh0200mv9lq72b072idz52ralcmajf2ai4ss";
    });

    bootstrap = (fetchurl {
      url = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.js";
      sha256 = "04s871zdfmi5264zixv9i0m45qk22dsz35ic61zx7ak5pd55npd6";
    });

    htmx = (fetchurl {
      url = "https://unpkg.com/htmx.org@1.4.1/dist/htmx.min.js";
      sha256 = "0z3ykfspz9iy23xc8i4qc919rzknbf4sxw9704ckch461f0r2y9l";
    });

  };

in
pkgs.runCommand "ekklesia-portal-js-libs" { }
  ("mkdir -p $out/js" + "\n" +
  lib.concatStringsSep
    "\n"
    (lib.mapAttrsToList
      (name: src: "cp ${src} $out/js/${name}.js")
      libs))
