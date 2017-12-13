# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -V 3.6 -r pypi2nix_source_deps -E postgresql -E libffi
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python36;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            sed -i               -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"                  $out/${pkgs.python35.sitePackages}/pip/req/req_install.py
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql libffi ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python36-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -f $prog ]; then
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
          ln -s ${pythonPackages.python.executable}               python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs //                                            { meta = drv.meta; });
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "Jinja2" = python.mkDerivation {
      name = "Jinja2-2.10";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz"; sha256 = "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."MarkupSafe"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://jinja.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "A small but fast and easy to use stand-alone template engine written in pure python.";
      };
    };



    "MarkupSafe" = python.mkDerivation {
      name = "MarkupSafe-1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz"; sha256 = "a6be69091dac236ea9c6bc7d012beab42010fa914c459791d627dad4910eb665"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/pallets/markupsafe";
        license = licenses.bsdOriginal;
        description = "Implements a XML/HTML/XHTML Markup safe string for Python";
      };
    };



    "PyYAML" = python.mkDerivation {
      name = "PyYAML-3.12";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz"; sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pyyaml.org/wiki/PyYAML";
        license = licenses.mit;
        description = "YAML parser and emitter for Python";
      };
    };



    "SQLAlchemy" = python.mkDerivation {
      name = "SQLAlchemy-1.1.15";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/c2/f6/11fcc1ce19a7cb81b1c9377f4e27ce3813265611922e355905e57c44d164/SQLAlchemy-1.1.15.tar.gz"; sha256 = "8b79a5ed91cdcb5abe97b0045664c55c140aec09e5dd5c01303e23de5fe7a95a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."psycopg2"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.sqlalchemy.org";
        license = licenses.mit;
        description = "Database Abstraction Library";
      };
    };



    "SQLAlchemy-Searchable" = python.mkDerivation {
      name = "SQLAlchemy-Searchable-0.10.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/77/7c/e767325f3a666095fda7f97cd611c6ab47b27d23c9db8bf3b755f0d2e8a3/SQLAlchemy-Searchable-0.10.6.tar.gz"; sha256 = "84f0bff434a17d64e8f7f394065b21855bd3c8a3ede770a25c84127e5d0f95f7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."SQLAlchemy"
      self."SQLAlchemy-Utils"
      self."psycopg2"
      self."pyparsing"
      self."validators"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-searchable";
        license = licenses.bsdOriginal;
        description = "Provides fulltext search capabilities for declarative SQLAlchemy models.";
      };
    };



    "SQLAlchemy-Utils" = python.mkDerivation {
      name = "SQLAlchemy-Utils-0.32.21";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/6b/8c/bf6539a85705e845e9f83908cc290dd34c352d90d9a86134124bd4b64acd/SQLAlchemy-Utils-0.32.21.tar.gz"; sha256 = "e35431b0e57c4f7030ff598c23813c8b7b04b508ce10e8e9ebe448645b38d6d7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Jinja2"
      self."SQLAlchemy"
      self."psycopg2"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-utils";
        license = licenses.bsdOriginal;
        description = "Various utility functions for SQLAlchemy.";
      };
    };



    "WebOb" = python.mkDerivation {
      name = "WebOb-1.7.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/75/34/731e23f52371852dfe7490a61644826ba7fe70fd52a377aaca0f4956ba7f/WebOb-1.7.4.tar.gz"; sha256 = "8d10af182fda4b92193113ee1edeb687ab9dc44336b37d6804e413f0240d40d9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };



    "attrs" = python.mkDerivation {
      name = "attrs-17.3.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3f/a4/d0db68156abbdee228ce69a786ecb512da40b36b1289aadb9e3f9fd45121/attrs-17.3.0.tar.gz"; sha256 = "c78f53e32d7cf36d8597c8a2c7e3c0ad210f97b9509e152e4c37fa80869f823c"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };



    "decorator" = python.mkDerivation {
      name = "decorator-4.1.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/bb/e0/f6e41e9091e130bf16d4437dabbac3993908e4d6485ecbc985ef1352db94/decorator-4.1.2.tar.gz"; sha256 = "7cb64d38cb8002971710c8899fbdfb859a23a364b7c99dab19d1f719c2ba16b5"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/micheles/decorator";
        license = licenses.bsdOriginal;
        description = "Better living through Python with decorators";
      };
    };



    "dectate" = python.mkDerivation {
      name = "dectate-0.13";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/0d/b8/9ce9e0ee72372d4dc8817e48d26a16d63d4397424cf3b8936b6e565be4ad/dectate-0.13.tar.gz"; sha256 = "299a5d3d674d7cd095c8489331ecece22e5a567ee8a7636e8b57bbb220c568e4"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://dectate.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A configuration engine for Python frameworks";
      };
    };



    "importscan" = python.mkDerivation {
      name = "importscan-0.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/2d/e1/01431f1afc930befc4a1e32b39e5227124ebcd5ee165683b0d8e80fdb45f/importscan-0.1.tar.gz"; sha256 = "5c003afe8d7f48d684bc9f66e8109952234812b225be324ce572ce4278b18f10"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.bsdOriginal;
        description = "Recursively import modules and sub-packages";
      };
    };



    "more.transaction" = python.mkDerivation {
      name = "more.transaction-0.8";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/e9/32/4584350d0fbeb8e5ee9ff050872027b6ff6829bc37884864ecd40e8bc1ba/more.transaction-0.8.tar.gz"; sha256 = "ba8db43731973c1e432a9213e4ab2390eccfa260d1e142071907d4c2980b440c"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."morepath"
      self."transaction"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/morepath/more.transaction";
        license = licenses.bsdOriginal;
        description = "transaction integration for Morepath";
      };
    };



    "morepath" = python.mkDerivation {
      name = "morepath-0.18.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/99/d9/4b914c4552830546b4e84e9e9c53169eba142631493026a6a0813b564709/morepath-0.18.1.tar.gz"; sha256 = "4b634b52ad79e30cc31d10a5433dffd6105b4f37b45ee25c222b3a4ee67b21d7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."PyYAML"
      self."WebOb"
      self."dectate"
      self."importscan"
      self."reg"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://morepath.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A micro web-framework with superpowers";
      };
    };



    "munch" = python.mkDerivation {
      name = "munch-2.2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/92/58/c17cf679a2b9b65541cc71ba13a950289b7d34dd0967e34b8816a4d87044/munch-2.2.0.tar.gz"; sha256 = "62fb4fb318e965a464b088e6af52a63e0905a50500b770596a939d3855e7aa15"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/Infinidat/munch";
        license = licenses.mit;
        description = "A dot-accessible dictionary (a la JavaScript objects).";
      };
    };



    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.7.3.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/dd/47/000b405d73ca22980684fd7bd3318690cc03cfa3b2ae1c5b7fff8050b28a/psycopg2-2.7.3.2.tar.gz"; sha256 = "5c3213be557d0468f9df8fe2487eaf2990d9799202c5ff5cb8d394d09fad9b2a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };



    "pyjade" = python.mkDerivation {
      name = "pyjade-4.0.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4a/04/396ec24e806fd3af7ea5d0f3cb6c7bbd4d00f7064712e4dd48f24c02ca95/pyjade-4.0.0.tar.gz"; sha256 = "8d95b741de09c4942259fc3d1ad7b4f48166e69cef6f11c172e4b2c458b1ccd7"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/syrusakbary/pyjade";
        license = licenses.mit;
        description = "Jade syntax template adapter for Django, Jinja2, Mako and Tornado templates";
      };
    };



    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3c/ec/a94f8cf7274ea60b5413df054f82a8980523efd712ec55a59e7c3357cf7c/pyparsing-2.2.0.tar.gz"; sha256 = "0832bcf47acd283788593e7a0f542407bd9550a55a8a8435214a1960e04bcb04"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pyparsing.wikispaces.com/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };



    "reg" = python.mkDerivation {
      name = "reg-0.11";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/50/45/cdf15fd2fe84d9bcedc38fb42e5c0836c9e6bf21d9b0f7b40ba4cf488008/reg-0.11.tar.gz"; sha256 = "ce61bc8c37d58477675d8eb4922ef26c1446e1691249de613f629ef286addf04"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."repoze.lru"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://reg.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Clever dispatch";
      };
    };



    "repoze.lru" = python.mkDerivation {
      name = "repoze.lru-0.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/12/bc/595a77c4b5e204847fdf19268314ef59c85193a9dc9f83630fc459c0fee5/repoze.lru-0.7.tar.gz"; sha256 = "0429a75e19380e4ed50c0694e26ac8819b4ea7851ee1fc7583c8572db80aff77"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.repoze.org";
        license = "License :: Repoze Public License";
        description = "A tiny LRU cache implementation and decorator";
      };
    };



    "six" = python.mkDerivation {
      name = "six-1.11.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz"; sha256 = "70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/six/";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "transaction" = python.mkDerivation {
      name = "transaction-2.1.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/27/c5/27f1953db67de21832fd977684e639e41c7738dc449886419bb2aa235094/transaction-2.1.2.tar.gz"; sha256 = "b9bc365e7dba3877e0f6fdee32aa029b8c0c1eb4fe227f524bffd5fc46064bd5"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."zope.interface"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/transaction";
        license = licenses.zpl21;
        description = "Transaction management for Python";
      };
    };



    "validators" = python.mkDerivation {
      name = "validators-0.12.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/8f/b5/9c9bf9cc9b50acea54a175eee97b0092f7676dbd6a17e00591588640acc3/validators-0.12.0.tar.gz"; sha256 = "bf1aa66554df0a7907f0e78b6d356e2ce30d6f2e73fefd1f3b14d20114341066"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."decorator"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/validators";
        license = licenses.bsdOriginal;
        description = "Python Data Validation for Humans™.";
      };
    };



    "zope.interface" = python.mkDerivation {
      name = "zope.interface-4.4.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/bd/d2/25349ed41f9dcff7b3baf87bd88a4c82396cf6e02f1f42bb68657a3132af/zope.interface-4.4.3.tar.gz"; sha256 = "d6d26d5dfbfd60c65152938fcb82f949e8dada37c041f72916fef6621ba5c5ce"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.interface";
        license = licenses.zpl21;
        description = "Interfaces for Python";
      };
    };



    "zope.sqlalchemy" = python.mkDerivation {
      name = "zope.sqlalchemy-0.7.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/14/95/47ef5f5fbf5f18dc95d6d39b7dbd690818b541afa724d14ed176e415b134/zope.sqlalchemy-0.7.7.tar.gz"; sha256 = "5da8ff6b060f3a47fc0cbc61cfd6a83b959b5e730f95e492edcf7b9bf3ec987a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."SQLAlchemy"
      self."transaction"
      self."zope.interface"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/zope.sqlalchemy";
        license = licenses.zpl21;
        description = "Minimal Zope/SQLAlchemy transaction integration";
      };
    };

  };
  localOverridesFile = ./requirements_override.nix;
  overrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [

  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [overrides] else [] ) ++ commonOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )