# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -I nixpkgs=/home/ts/git/nixpkgs -V 3.7 -r pypi2nix_source_deps -E postgresql -E libffi
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
    python = pkgs.python37;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            if [ -e $out/${pkgs.python37.sitePackages}/pip/req/req_install.py ]; then
              sed -i \
                -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"  \
                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"  \
                $out/${pkgs.python37.sitePackages}/pip/req/req_install.py
            fi
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql libffi ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python37-interpreter";
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
      mkDerivation = pythonPackages.buildPythonPackage;
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
    "Chameleon" = python.mkDerivation {
      name = "Chameleon-3.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/96/8c/f8bcdf3563d625f2e6e9c04d02d0fff828777e35484e19035d0e6b0aedda/Chameleon-3.4.tar.gz"; sha256 = "7750865a68b469b34cbc60b9927f7e5c609808b6b966bf75bf8556e6ed48912c"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://chameleon.readthedocs.io";
        license = "BSD-like (http://repoze.org/license.html)";
        description = "Fast HTML/XML Template Compiler.";
      };
    };

    "Jinja2" = python.mkDerivation {
      name = "Jinja2-2.10";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz"; sha256 = "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz"; sha256 = "a6be69091dac236ea9c6bc7d012beab42010fa914c459791d627dad4910eb665"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/pallets/markupsafe";
        license = licenses.bsdOriginal;
        description = "Implements a XML/HTML/XHTML Markup safe string for Python";
      };
    };

    "PyYAML" = python.mkDerivation {
      name = "PyYAML-3.13";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/9e/a3/1d13970c3f36777c583f136c136f804d70f500168edc1edea6daa7200769/PyYAML-3.13.tar.gz"; sha256 = "3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pyyaml.org/wiki/PyYAML";
        license = licenses.mit;
        description = "YAML parser and emitter for Python";
      };
    };

    "SQLAlchemy" = python.mkDerivation {
      name = "SQLAlchemy-1.2.10";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/8a/c2/29491103fd971f3988e90ee3a77bb58bad2ae2acd6e8ea30a6d1432c33a3/SQLAlchemy-1.2.10.tar.gz"; sha256 = "72325e67fb85f6e9ad304c603d83626d1df684fdf0c7ab1f0352e71feeab69d8"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      name = "SQLAlchemy-Searchable-1.0.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/50/03/7d9c0cbafccd29a2ed48cfa6fe0b8de1d9a7798b09db89b7aff0098779e2/SQLAlchemy-Searchable-1.0.3.tar.gz"; sha256 = "b1854f9d41c911f50fa7802b8e0df3c4ad2a10ecdf97cce79dfeae105a5ecbf6"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."SQLAlchemy"
      self."SQLAlchemy-Utils"
      self."psycopg2"
      self."validators"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kvesteri/sqlalchemy-searchable";
        license = licenses.bsdOriginal;
        description = "Provides fulltext search capabilities for declarative SQLAlchemy models.";
      };
    };

    "SQLAlchemy-Utils" = python.mkDerivation {
      name = "SQLAlchemy-Utils-0.33.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/28/17/fedf5a8b2492a7d12986273b7d661419970b1866f3be3f897114aa3c7195/SQLAlchemy-Utils-0.33.3.tar.gz"; sha256 = "4119204ff302906015516992b7481e5aabeeaa61c7b04329f9113e42c097b855"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Jinja2"
      self."SQLAlchemy"
      self."passlib"
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
      name = "WebOb-1.8.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/f2/8a/dd4a3a32fba184e48a50be732aa390f9db2a725a535dcfb9fee781a2943c/WebOb-1.8.2.tar.gz"; sha256 = "1fe722f2ab857685fc96edec567dc40b1875b21219b3b348e58cd8c4d5ea7df3"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://webob.org/";
        license = licenses.mit;
        description = "WSGI request and response object";
      };
    };

    "attrs" = python.mkDerivation {
      name = "attrs-18.1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/e4/ac/a04671e118b57bee87dabca1e0f2d3bda816b7a551036012d0ca24190e71/attrs-18.1.0.tar.gz"; sha256 = "e0d0eb91441a3b53dab4d9b743eafc1ac44476296a2053b6ca3af0b139faf87b"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
      self."zope.interface"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "case-conversion" = python.mkDerivation {
      name = "case-conversion-2.1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/cb/8c/14731e4d4f6fd9876575abc7df9861bcb0a21d764f7ac622ab5485c45afe/case_conversion-2.1.0.tar.gz"; sha256 = "4114aaed4213f2235f1648502fd1793e5fdfa3fa86f85979fd2d0dce1584e197"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."regex"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/AlejandroFrias/case-conversion";
        license = licenses.mit;
        description = "Convert between different types of cases (unicode supported)";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2018.4.16";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/4d/9c/46e950a6f4d6b4be571ddcae21e7bc846fcbb88f1de3eff0f6dd0a6be55d/certifi-2018.4.16.tar.gz"; sha256 = "13e698f54293db9f89122b0581843a782ad0934a4fe0172d2a980ba77fc61bb7"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"; sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "colander" = python.mkDerivation {
      name = "colander-1.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/cc/e2/c4e716ac4a426d8ad4dfe306c34f0018a22275d2420815784005bf771c84/colander-1.4.tar.gz"; sha256 = "e20e9acf190e5711cf96aa65a5405dac04b6e841028fc361d953a9923dbc4e72"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."iso8601"
      self."translationstring"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docs.pylonsproject.org/projects/colander/en/latest/";
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
        description = "A simple schema-based serialization and deserialization library";
      };
    };

    "decorator" = python.mkDerivation {
      name = "decorator-4.3.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/6f/24/15a229626c775aae5806312f6bf1e2a73785be3402c0acdec5dbddd8c11e/decorator-4.3.0.tar.gz"; sha256 = "c39efa13fbdeb4506c476c9b3babf6a718da943dab7811c206005a4a956c080c"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/0d/b8/9ce9e0ee72372d4dc8817e48d26a16d63d4397424cf3b8936b6e565be4ad/dectate-0.13.tar.gz"; sha256 = "299a5d3d674d7cd095c8489331ecece22e5a567ee8a7636e8b57bbb220c568e4"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://dectate.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "A configuration engine for Python frameworks";
      };
    };

    "deform" = python.mkDerivation {
      name = "deform-2.0.5";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/0c/b1/ba711d5808c12538c8504f534d79c124ed834f19ac36f0ac5391c3bbd1c1/deform-2.0.5.tar.gz"; sha256 = "874d3346a02c500432efdcc73b1a7174aa0ea69cd52a99bb9a812967f54f6f79"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Chameleon"
      self."colander"
      self."iso8601"
      self."peppercorn"
      self."translationstring"
      self."zope.deprecation"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docs.pylonsproject.org/projects/deform/en/latest/";
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
        description = "Form library with advanced features like nested forms";
      };
    };

    "idna" = python.mkDerivation {
      name = "idna-2.7";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/65/c4/80f97e9c9628f3cac9b98bfca0402ede54e0563b56482e3e6e45c43c4935/idna-2.7.tar.gz"; sha256 = "684a38a6f903c1d71d6d5fac066b58d7768af4de2b832e426ec79c30daa94a16"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/2d/e1/01431f1afc930befc4a1e32b39e5227124ebcd5ee165683b0d8e80fdb45f/importscan-0.1.tar.gz"; sha256 = "5c003afe8d7f48d684bc9f66e8109952234812b225be324ce572ce4278b18f10"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.bsdOriginal;
        description = "Recursively import modules and sub-packages";
      };
    };

    "iso8601" = python.mkDerivation {
      name = "iso8601-0.1.11";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/c0/75/c9209ee4d1b5975eb8c2cba4428bde6b61bd55664a98290dd015cdb18e98/iso8601-0.1.11.tar.gz"; sha256 = "e8fb52f78880ae063336c94eb5b87b181e6a0cc33a6c008511bac9a6e980ef30"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/micktwomey/pyiso8601";
        license = licenses.mit;
        description = "Simple module to parse ISO 8601 dates";
      };
    };

    "itsdangerous" = python.mkDerivation {
      name = "itsdangerous-0.24";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz"; sha256 = "cbb3fcf8d3e33df861709ecaf89d9e6629cff0a217bc2848f1b41cd30d360519"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/itsdangerous";
        license = licenses.bsdOriginal;
        description = "Various helpers to pass trusted data to untrusted environments and back.";
      };
    };

    "more.forwarded" = python.mkDerivation {
      name = "more.forwarded-0.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/7c/d8/e14f30346a9da2dc705f2206a04c70d40dc03e8238f3a9ac4bb668aedb25/more.forwarded-0.2.tar.gz"; sha256 = "d6e89b4990dc98fe4476d1dea3c49506a3434d5fc8118d48afaeecfcaa0595c3"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."morepath"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/more.static";
        license = licenses.bsdOriginal;
        description = "Forwarded header support for Morepath";
      };
    };

    "more.itsdangerous" = python.mkDerivation {
      name = "more.itsdangerous-0.0.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/56/22/a423e8d148b628cf62f8bc8ec63ffdbda62258783e68c743c987321e68f0/more.itsdangerous-0.0.2.tar.gz"; sha256 = "c0352ec418cb5f356261d88c600c18f7d7627895d357fe2f933fe643e42ba0f2"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."itsdangerous"
      self."morepath"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/morepath/more.itsdangerous";
        license = licenses.bsdOriginal;
        description = "An identity policy for morepath using itsdangerous.";
      };
    };

    "more.transaction" = python.mkDerivation {
      name = "more.transaction-0.8";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/e9/32/4584350d0fbeb8e5ee9ff050872027b6ff6829bc37884864ecd40e8bc1ba/more.transaction-0.8.tar.gz"; sha256 = "ba8db43731973c1e432a9213e4ab2390eccfa260d1e142071907d4c2980b440c"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/99/d9/4b914c4552830546b4e84e9e9c53169eba142631493026a6a0813b564709/morepath-0.18.1.tar.gz"; sha256 = "4b634b52ad79e30cc31d10a5433dffd6105b4f37b45ee25c222b3a4ee67b21d7"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      name = "munch-2.3.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/68/f4/260ec98ea840757a0da09e0ed8135333d59b8dfebe9752a365b04857660a/munch-2.3.2.tar.gz"; sha256 = "6ae3d26b837feacf732fb8aa5b842130da1daf221f5af9f9d4b2a0a6414b0d51"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "oauthlib" = python.mkDerivation {
      name = "oauthlib-2.1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/df/5f/3f4aae7b28db87ddef18afed3b71921e531ca288dc604eb981e9ec9f8853/oauthlib-2.1.0.tar.gz"; sha256 = "ac35665a61c1685c56336bda97d5eefa246f1202618a1d6f34fccb1bdd404162"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/oauthlib/oauthlib";
        license = licenses.bsdOriginal;
        description = "A generic, spec-compliant, thorough implementation of the OAuth request-signing logic";
      };
    };

    "passlib" = python.mkDerivation {
      name = "passlib-1.7.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/25/4b/6fbfc66aabb3017cd8c3bd97b37f769d7503ead2899bf76e570eb91270de/passlib-1.7.1.tar.gz"; sha256 = "3d948f64138c25633613f303bcc471126eae67c04d5e3f6b7b8ce6242f8653e0"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ecollins/passlib";
        license = licenses.bsdOriginal;
        description = "comprehensive password hashing framework supporting over 30 schemes";
      };
    };

    "peppercorn" = python.mkDerivation {
      name = "peppercorn-0.5";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/45/ec/a62ec317d1324a01567c5221b420742f094f05ee48097e5157d32be3755c/peppercorn-0.5.tar.gz"; sha256 = "921cba5d51fa211e6da0fbd2120b9a98d663422a80f5bb669ad81ffb0909774b"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docs.pylonsproject.org/projects/peppercorn/en/latest/";
        license = "BSD-derived (http://www.repoze.org/LICENSE.txt)";
        description = "A library for converting a token stream into a data structure for use in web form posts";
      };
    };

    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.7.5";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b2/c1/7bf6c464e903ffc4f3f5907c389e5a4199666bf57f6cd6bf46c17912a1f9/psycopg2-2.7.5.tar.gz"; sha256 = "eccf962d41ca46e6326b97c8fe0a6687b58dfc1a5f6540ed071ff1474cea749e"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/4a/04/396ec24e806fd3af7ea5d0f3cb6c7bbd4d00f7064712e4dd48f24c02ca95/pyjade-4.0.0.tar.gz"; sha256 = "8d95b741de09c4942259fc3d1ad7b4f48166e69cef6f11c172e4b2c458b1ccd7"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "reg" = python.mkDerivation {
      name = "reg-0.11";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/50/45/cdf15fd2fe84d9bcedc38fb42e5c0836c9e6bf21d9b0f7b40ba4cf488008/reg-0.11.tar.gz"; sha256 = "ce61bc8c37d58477675d8eb4922ef26c1446e1691249de613f629ef286addf04"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "regex" = python.mkDerivation {
      name = "regex-2018.7.11";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/9f/79/adbe79373ec3c56ae61670bbed30609fe4a9b6af835478fa12bf8795cdec/regex-2018.07.11.tar.gz"; sha256 = "9308dbce8e5ff4ee06b172a777f6c7f650a5835a5ad41a6080eb501639c27a2f"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/mrabarnett/mrab-regex";
        license = licenses.psfl;
        description = "Alternative regular expression module, to replace re.";
      };
    };

    "repoze.lru" = python.mkDerivation {
      name = "repoze.lru-0.7";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/12/bc/595a77c4b5e204847fdf19268314ef59c85193a9dc9f83630fc459c0fee5/repoze.lru-0.7.tar.gz"; sha256 = "0429a75e19380e4ed50c0694e26ac8819b4ea7851ee1fc7583c8572db80aff77"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.repoze.org";
        license = "License :: Repoze Public License";
        description = "A tiny LRU cache implementation and decorator";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.19.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/54/1f/782a5734931ddf2e1494e4cd615a51ff98e1879cbe9eecbdfeaf09aa75e9/requests-2.19.1.tar.gz"; sha256 = "ec22d826a36ed72a7358ff3fe56cbd4ba69dd7a6718ffd450ff0e9df7a47ce6a"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "requests-oauthlib" = python.mkDerivation {
      name = "requests-oauthlib-1.0.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/95/be/072464f05b70e4142cb37151e215a2037b08b1400f8a56f2538b76ca6205/requests-oauthlib-1.0.0.tar.gz"; sha256 = "8886bfec5ad7afb391ed5443b1f697c6f4ae98d0e5620839d8b4499c032ada3f"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."oauthlib"
      self."requests"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/requests/requests-oauthlib";
        license = licenses.bsdOriginal;
        description = "OAuthlib authentication support for Requests.";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.11.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz"; sha256 = "70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/six/";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "transaction" = python.mkDerivation {
      name = "transaction-2.2.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/a6/5e/09da91cb9373c73aae41721e5571c47db72fa9e11b259ca8fd3b01e306e9/transaction-2.2.1.tar.gz"; sha256 = "f2242070e437e5d555ea3df809cb517860513254c828f33847df1c5e4b776c7a"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "translationstring" = python.mkDerivation {
      name = "translationstring-1.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/5e/eb/bee578cc150b44c653b63f5ebe258b5d0d812ddac12497e5f80fcad5d0b4/translationstring-1.3.tar.gz"; sha256 = "4ee44cfa58c52ade8910ea0ebc3d2d84bdcad9fa0422405b1801ec9b9a65b72d"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pylonsproject.org";
        license = "BSD-like (http://repoze.org/license.html)";
        description = "Utility library for i18n relied on by various Repoze and Pyramid packages";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.23";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/3c/d2/dc5471622bd200db1cd9319e02e71bc655e9ea27b8e0ce65fc69de0dac15/urllib3-1.23.tar.gz"; sha256 = "a68ac5e15e76e7e5dd2b8f94007233e01effe3e50e8daddf69acfd81cb686baf"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
      name = "validators-0.12.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/45/7b/5b7b74208a3e0744d1a0efbfb1935fa46fa4cfe58d3d63f17c49c58c429c/validators-0.12.2.tar.gz"; sha256 = "172ac45f7d1944ce4beca3c5c53ca7c83e9759e39fd3fedc1cf28e2130268706"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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

    "zope.deprecation" = python.mkDerivation {
      name = "zope.deprecation-4.3.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/a1/18/2dc5e6bfe64fdc3b79411b67464c55bb0b43b127051a20f7f492ab767758/zope.deprecation-4.3.0.tar.gz"; sha256 = "7d52e134bbaaa0d72e1e2bc90f0587f1adc116c4bdf15912afaf2f1e8856b224"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/zopefoundation/zope.deprecation";
        license = licenses.zpl21;
        description = "Zope Deprecation Infrastructure";
      };
    };

    "zope.interface" = python.mkDerivation {
      name = "zope.interface-4.5.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ac/8a/657532df378c2cd2a1fe6b12be3b4097521570769d4852ec02c24bd3594e/zope.interface-4.5.0.tar.gz"; sha256 = "57c38470d9f57e37afb460c399eb254e7193ac7fb8042bd09bdc001981a9c74c"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/zopefoundation/zope.interface";
        license = licenses.zpl21;
        description = "Interfaces for Python";
      };
    };

    "zope.sqlalchemy" = python.mkDerivation {
      name = "zope.sqlalchemy-1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/75/13/b88b597ef6027b5480f68e022206e4b3ee2310a59bbc85bd3e9eca9566b6/zope.sqlalchemy-1.0.tar.gz"; sha256 = "9316a1a8bb9e4f9f59332acf1ad2cc8b664f19a4bde5f68be7f61f3e11f80514"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
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
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
    
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