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
      self."pytest"
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
      self."SQLAlchemy"
      self."psycopg2"
      self."pytest"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-utils";
        license = licenses.bsdOriginal;
        description = "Various utility functions for SQLAlchemy.";
      };
    };



    "WebOb" = python.mkDerivation {
      name = "WebOb-1.7.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/46/87/2f96d8d43b2078fae6e1d33fa86b95c228cebed060f4e3c7576cc44ea83b/WebOb-1.7.3.tar.gz"; sha256 = "e65ca14b9f5ae5b031988ffc93f8b7f305ddfcf17a4c774ae0db47bcb3b87283"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };



    "WebTest" = python.mkDerivation {
      name = "WebTest-2.0.29";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/94/de/8f94738be649997da99c47b104aa3c3984ecec51a1d8153ed09638253d56/WebTest-2.0.29.tar.gz"; sha256 = "dbbccc15ac2465066c95dc3a7de0d30cde3791e886ccbd7e91d5d2a2580c922d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."WebOb"
      self."beautifulsoup4"
      self."coverage"
      self."six"
      self."waitress"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webtest.pythonpaste.org/";
        license = licenses.mit;
        description = "Helper to test WSGI applications";
      };
    };



    "Werkzeug" = python.mkDerivation {
      name = "Werkzeug-0.12.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/56/41/c095a77eb2dd69bf278dd664a97d3416af04e9ba1a00b8c138f772741d31/Werkzeug-0.12.2.tar.gz"; sha256 = "903a7b87b74635244548b30d30db4c8947fe64c5198f58899ddcd3a13c23bb26"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://werkzeug.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "The Swiss Army knife of Python web development";
      };
    };



    "beautifulsoup4" = python.mkDerivation {
      name = "beautifulsoup4-4.6.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/fa/8d/1d14391fdaed5abada4e0f63543fef49b8331a34ca60c88bd521bcf7f782/beautifulsoup4-4.6.0.tar.gz"; sha256 = "808b6ac932dccb0a4126558f7dfdcf41710dd44a4ef497a0bb59a77f9f078e89"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.crummy.com/software/BeautifulSoup/bs4/";
        license = licenses.mit;
        description = "Screen-scraping library";
      };
    };



    "certifi" = python.mkDerivation {
      name = "certifi-2017.11.5";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/23/3f/8be01c50ed24a4bd6b8da799839066ce0288f66f5e11f0367323467f0cbc/certifi-2017.11.5.tar.gz"; sha256 = "5ec74291ca1136b40f0379e1128ff80e866597e4e2c1e755739a913bbc3613c0"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };



    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"; sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };



    "coverage" = python.mkDerivation {
      name = "coverage-4.4.2";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/0b/e1/190ef1a264144c9b073b7353c259ca5431b5ddc8861b452e858fcbd0e9de/coverage-4.4.2.tar.gz"; sha256 = "309d91bd7a35063ec7a0e4d75645488bfab3f0b66373e7722f23da7f5b0f34cc"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ned/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
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
      propagatedBuildInputs = [
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://dectate.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A configuration engine for Python frameworks";
      };
    };



    "idna" = python.mkDerivation {
      name = "idna-2.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/f4/bd/0467d62790828c23c47fc1dfa1b1f052b24efdf5290f071c7a91d0d82fd3/idna-2.6.tar.gz"; sha256 = "2c6a5de3089009e3da7c5dde64a141dbc8551d5b7f6cf4ed7c2568d0cc520a8f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };



    "importscan" = python.mkDerivation {
      name = "importscan-0.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/2d/e1/01431f1afc930befc4a1e32b39e5227124ebcd5ee165683b0d8e80fdb45f/importscan-0.1.tar.gz"; sha256 = "5c003afe8d7f48d684bc9f66e8109952234812b225be324ce572ce4278b18f10"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."py"
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.bsdOriginal;
        description = "Recursively import modules and sub-packages";
      };
    };



    "more.pathtool" = python.mkDerivation {
      name = "more.pathtool-0.6.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/43/12/e114e13cad4979165ac285768caf778ee7fa012b5ce43d39f4b056d00b3f/more.pathtool-0.6.1.tar.gz"; sha256 = "af21a8364f4b15cd748492abd9a46c0024957ebe96bb771e060e775846924e09"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."dectate"
      self."morepath"
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/morepath/more.pathtool";
        license = licenses.bsdOriginal;
        description = "Information about path configuration in Morepath";
      };
    };



    "more.transaction" = python.mkDerivation {
      name = "more.transaction-0.8";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/e9/32/4584350d0fbeb8e5ee9ff050872027b6ff6829bc37884864ecd40e8bc1ba/more.transaction-0.8.tar.gz"; sha256 = "ba8db43731973c1e432a9213e4ab2390eccfa260d1e142071907d4c2980b440c"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."WebTest"
      self."coverage"
      self."morepath"
      self."pytest"
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
      self."WebTest"
      self."dectate"
      self."importscan"
      self."pytest"
      self."reg"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://morepath.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A micro web-framework with superpowers";
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



    "py" = python.mkDerivation {
      name = "py-1.5.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/56/d7/a20e836f5489f5d9d9ac7a6326ca9a1c36762dd182be5507da03a09785a9/py-1.5.1.tar.gz"; sha256 = "e85aaa3c2e837413c6387eb2a4efbe7ff93658813d13986da004984ffe84b3a3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
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



    "pytest" = python.mkDerivation {
      name = "pytest-3.2.5";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/1f/f8/8cd74c16952163ce0db0bd95fdd8810cbf093c08be00e6e665ebf0dc3138/pytest-3.2.5.tar.gz"; sha256 = "6d5bd4f7113b444c55a3bbb5c738a3dd80d43563d063fc42dcb0aaefbdd78b81"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."py"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pytest.org";
        license = licenses.mit;
        description = "pytest: simple powerful testing with Python";
      };
    };



    "pytest-localserver" = python.mkDerivation {
      name = "pytest-localserver-0.3.7";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/41/d6/90242691486b2fc42cd2dd73023760a065263d5551ef34f8e209b6fa8576/pytest-localserver-0.3.7.tar.gz"; sha256 = "d828d79232456d0b4eb863e9de2c85699259f436a3185e39d0d5001b8c8521b0"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Werkzeug"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://bitbucket.org/pytest-dev/pytest-localserver/";
        license = licenses.mit;
        description = "py.test plugin to test server connections locally.";
      };
    };



    "reg" = python.mkDerivation {
      name = "reg-0.11";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/50/45/cdf15fd2fe84d9bcedc38fb42e5c0836c9e6bf21d9b0f7b40ba4cf488008/reg-0.11.tar.gz"; sha256 = "ce61bc8c37d58477675d8eb4922ef26c1446e1691249de613f629ef286addf04"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pytest"
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
      propagatedBuildInputs = [
      self."coverage"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.repoze.org";
        license = "License :: Repoze Public License";
        description = "A tiny LRU cache implementation and decorator";
      };
    };



    "requests" = python.mkDerivation {
      name = "requests-2.18.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/b0/e1/eab4fc3752e3d240468a8c0b284607899d2fbfb236a56b7377a329aa8d09/requests-2.18.4.tar.gz"; sha256 = "9c443e7324ba5b85070c4a818ade28bfabedf16ea10206da1132edaa6dda237e"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."certifi"
      self."chardet"
      self."idna"
      self."urllib3"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-requests.org";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
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
      self."coverage"
      self."zope.interface"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/transaction";
        license = licenses.zpl21;
        description = "Transaction management for Python";
      };
    };



    "urllib3" = python.mkDerivation {
      name = "urllib3-1.22";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/ee/11/7c59620aceedcc1ef65e156cc5ce5a24ef87be4107c2b74458464e437a5d/urllib3-1.22.tar.gz"; sha256 = "cc44da8e1145637334317feebd728bd869a35285b93cbb4cca2577da7e62db4f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."certifi"
      self."idna"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description = "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };



    "validators" = python.mkDerivation {
      name = "validators-0.12.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/8f/b5/9c9bf9cc9b50acea54a175eee97b0092f7676dbd6a17e00591588640acc3/validators-0.12.0.tar.gz"; sha256 = "bf1aa66554df0a7907f0e78b6d356e2ce30d6f2e73fefd1f3b14d20114341066"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."decorator"
      self."pytest"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/validators";
        license = licenses.bsdOriginal;
        description = "Python Data Validation for Humans™.";
      };
    };



    "waitress" = python.mkDerivation {
      name = "waitress-1.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/3c/68/1c10dd5c556872ceebe88483b0436140048d39de83a84a06a8baa8136f4f/waitress-1.1.0.tar.gz"; sha256 = "d33cd3d62426c0f1b3cd84ee3d65779c7003aae3fc060dee60524d10a57f05a9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/Pylons/waitress";
        license = licenses.zpl21;
        description = "Waitress WSGI server";
      };
    };



    "zope.interface" = python.mkDerivation {
      name = "zope.interface-4.4.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/bd/d2/25349ed41f9dcff7b3baf87bd88a4c82396cf6e02f1f42bb68657a3132af/zope.interface-4.4.3.tar.gz"; sha256 = "d6d26d5dfbfd60c65152938fcb82f949e8dada37c041f72916fef6621ba5c5ce"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.interface";
        license = licenses.zpl21;
        description = "Interfaces for Python";
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