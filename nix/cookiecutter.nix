# generated using pypi2nix tool (version: 2.0.4)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python38 -e cookiecutter --basename cookiecutter
#

{ pkgs ? import <nixpkgs> {},
  overrides ? ({ pkgs, python }: self: super: {})
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python38;
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python38-interpreter";
        buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter} \
              $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "
              (selectPkgsFn pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -x "$prog" ] && [ -f "$prog" ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          ln -s ${pythonPackages.python.executable} \
              python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };

      interpreter = interpreterWithPackages builtins.attrValues;
    in {
      __old = pythonPackages;
      inherit interpreter;
      inherit interpreterWithPackages;
      mkDerivation = args: pythonPackages.buildPythonPackage (args // {
        nativeBuildInputs = (args.nativeBuildInputs or []) ++ args.buildInputs;
      });
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (
          drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; }
        );
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {
    "arrow" = python.mkDerivation {
      name = "arrow-0.15.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0d/e1/bad2eff749887d400c9fb9041846517c1cc7b66951052a7751316940c3a1/arrow-0.15.6.tar.gz";
        sha256 = "eb5d339f00072cc297d7de252a2e75f272085d1231a3723f1026d1fa91367118";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."python-dateutil"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://arrow.readthedocs.io";
        license = licenses.asl20;
        description = "Better dates & times for Python";
      };
    };

    "binaryornot" = python.mkDerivation {
      name = "binaryornot-0.4.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a7/fe/7ebfec74d49f97fc55cd38240c7a7d08134002b1e14be8c3897c0dd5e49b/binaryornot-0.4.4.tar.gz";
        sha256 = "359501dfc9d40632edc9fac890e19542db1a287bbcfa58175b66658392018061";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."chardet"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/audreyr/binaryornot";
        license = licenses.bsdOriginal;
        description = "Ultra-lightweight pure Python package to check if a file is binary or text.";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2020.4.5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b8/e2/a3a86a67c3fc8249ed305fc7b7d290ebe5e4d46ad45573884761ef4dea7b/certifi-2020.4.5.1.tar.gz";
        sha256 = "51fcb31174be6e6664c5f69e3e1691a2d72a1a12e90f872cbdb1567eb47b6519";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifiio.readthedocs.io/en/latest/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };

    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz";
        sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "click" = python.mkDerivation {
      name = "click-7.1.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/27/6f/be940c8b1f1d69daceeb0032fee6c34d7bd70e3e649ccac0951500b4720e/click-7.1.2.tar.gz";
        sha256 = "d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/click/";
        license = licenses.bsdOriginal;
        description = "Composable command line interface toolkit";
      };
    };

    "cookiecutter" = python.mkDerivation {
      name = "cookiecutter-1.7.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f2/6d/eb4edcf99c3dd17b6d931c5b0b19e093a7147400840f3d8985901c27029f/cookiecutter-1.7.2.tar.gz";
        sha256 = "efb6b2d4780feda8908a873e38f0e61778c23f6a2ea58215723bcceb5b515dac";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."binaryornot"
        self."click"
        self."jinja2"
        self."jinja2-time"
        self."markupsafe"
        self."poyo"
        self."python-slugify"
        self."requests"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/cookiecutter/cookiecutter";
        license = licenses.bsdOriginal;
        description = "A command-line utility that creates projects from project templates, e.g. creating a Python package project from a Python package project template.";
      };
    };

    "idna" = python.mkDerivation {
      name = "idna-2.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cb/19/57503b5de719ee45e83472f339f617b0c01ad75cba44aba1e4c97c2b0abd/idna-2.9.tar.gz";
        sha256 = "7588d1c14ae4c77d74036e8c22ff447b26d0fde8f007354fd48a7814db15b7cb";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "jinja2" = python.mkDerivation {
      name = "jinja2-2.11.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/64/a7/45e11eebf2f15bf987c3bc11d37dcc838d9dc81250e67e4c5968f6008b6c/Jinja2-2.11.2.tar.gz";
        sha256 = "89aab215427ef59c34ad58735269eb58b1a5808103067f7bb9d5836c651b3bb0";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."markupsafe"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/jinja/";
        license = licenses.bsdOriginal;
        description = "A very fast and expressive template engine.";
      };
    };

    "jinja2-time" = python.mkDerivation {
      name = "jinja2-time-0.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/de/7c/ee2f2014a2a0616ad3328e58e7dac879251babdb4cb796d770b5d32c469f/jinja2-time-0.2.0.tar.gz";
        sha256 = "d14eaa4d315e7688daa4969f616f226614350c48730bfa1692d2caebd8c90d40";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."arrow"
        self."jinja2"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/hackebrot/jinja2-time";
        license = licenses.mit;
        description = "Jinja2 Extension for Dates and Times";
      };
    };

    "markupsafe" = python.mkDerivation {
      name = "markupsafe-1.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094/MarkupSafe-1.1.1.tar.gz";
        sha256 = "29872e92839765e546828bb7754a68c418d927cd064fd4708fab9fe9c8bb116b";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "poyo" = python.mkDerivation {
      name = "poyo-0.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7d/56/01b496f36bbd496aed9351dd1b06cf57fd2f5028480a87adbcf7a4ff1f65/poyo-0.5.0.tar.gz";
        sha256 = "e26956aa780c45f011ca9886f044590e2d8fd8b61db7b1c1cf4e0869f48ed4dd";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/hackebrot/poyo";
        license = licenses.mit;
        description = "";
      };
    };

    "python-dateutil" = python.mkDerivation {
      name = "python-dateutil-2.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/be/ed/5bbc91f03fa4c839c4c7360375da77f9659af5f7086b7a7bdda65771c8e0/python-dateutil-2.8.1.tar.gz";
        sha256 = "73ebfe9dbf22e832286dafa60473e4cd239f8592f699aa5adaf10050e6e1823c";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://dateutil.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Extensions to the standard Python datetime module";
      };
    };

    "python-slugify" = python.mkDerivation {
      name = "python-slugify-4.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/92/5f/7b84a0bba8a0fdd50c046f8b57dcf179dc16237ad33446079b7c484de04c/python-slugify-4.0.0.tar.gz";
        sha256 = "a8fc3433821140e8f409a9831d13ae5deccd0b033d4744d94b31fea141bdd84c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."text-unidecode"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/un33k/python-slugify";
        license = licenses.mit;
        description = "A Python Slugify application that handles Unicode";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.23.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f5/4f/280162d4bd4d8aad241a21aecff7a6e46891b905a4341e7ab549ebaf7915/requests-2.23.0.tar.gz";
        sha256 = "b3f43d496c6daba4493e7c431722aeb7dbc6288f52a6e04e7b6023b0247817e6";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."chardet"
        self."idna"
        self."urllib3"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://requests.readthedocs.io";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
      };
    };

    "setuptools" = python.mkDerivation {
      name = "setuptools-46.1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b5/96/af1686ea8c1e503f4a81223d4a3410e7587fd52df03083de24161d0df7d4/setuptools-46.1.3.zip";
        sha256 = "795e0475ba6cd7fa082b1ee6e90d552209995627a2a227a47c6ea93282f4bfb1";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description = "Easily download, build, install, upgrade, and uninstall Python packages";
      };
    };

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b2/f7/60a645aae001a2e06cf4b8db2fba9d9f36b8fd378f10647e3e218b61b74b/setuptools_scm-3.5.0.tar.gz";
        sha256 = "5bdf21a05792903cafe7ae0c9501182ab52497614fa6b1750d9dbae7b60c1a87";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.14.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/21/9f/b251f7f8a76dec1d6651be194dfba8fb8d7781d10ab3987190de8391d08e/six-1.14.0.tar.gz";
        sha256 = "236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "text-unidecode" = python.mkDerivation {
      name = "text-unidecode-1.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ab/e2/e9a00f0ccb71718418230718b3d900e71a5d16e701a3dae079a21e9cd8f8/text-unidecode-1.3.tar.gz";
        sha256 = "bad6603bb14d279193107714b288be206cac565dfa49aa5b105294dd5c4aab93";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kmike/text-unidecode/";
        license = licenses.artistic2;
        description = "The most basic Text::Unidecode port";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.25.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/05/8c/40cd6949373e23081b3ea20d5594ae523e681b6f472e600fbc95ed046a36/urllib3-1.25.9.tar.gz";
        sha256 = "3018294ebefce6572a474f0604c2021e33b3fd8006ecd11d62107a5d2a963527";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description = "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.34.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/75/28/521c6dc7fef23a68368efefdcd682f5b3d1d58c2b90b06dc1d0b805b51ae/wheel-0.34.2.tar.gz";
        sha256 = "8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python";
      };
    };
  };
  localOverridesFile = ./cookiecutter_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
        (let src = pkgs.fetchFromGitHub { owner = "nix-community"; repo = "pypi2nix-overrides"; rev = "100c15ec7dfe7d241402ecfb1e796328d0eaf1ec"; sha256 = "0akfkvdakcdxc1lrxznh1rz2811x4pafnsq3jnyr5pn3m30pc7db"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
  ];
  paramOverrides = [
    (overrides { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [localOverrides] else [] ) ++ commonOverrides ++ paramOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )