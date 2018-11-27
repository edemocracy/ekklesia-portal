{ pkgs }:

(pkgs.pipenv.override { python3Packages = pkgs.python37Packages; }).overrideAttrs(oldAttrs: {
    name = "pipenv-2018.10.28";
    src = pkgs.fetchFromGitHub {
        owner = "pypa";
        repo = "pipenv";
        rev = "e8bf34b5481a368211e757ea5cae66f10b3077e1";
        sha256 = "1np49ghkk33b13hwiqalprhcxawc3qxjc0dm5bf9wc3578q8jfrq";
    };
})
