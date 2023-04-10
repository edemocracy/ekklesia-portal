{ stdenv, lib, nginxMainline, fetchurl, zlib, libxcrypt }:

let
  tmp = "/dev/shm";
in

nginxMainline.overrideAttrs (oldAttrs: rec {
  buildInputs = [ libxcrypt zlib ];

  configureFlags = [
    "--error-log-path=/dev/stderr"
    "--http-client-body-temp-path=${tmp}"
    "--http-log-path=/dev/stdout"
    "--pid-path=${tmp}/nginx.pid"
    "--without-http_access_module"
    "--without-http_auth_basic_module"
    "--without-http_autoindex_module"
    "--without-http_browser_module"
    "--without-http_empty_gif_module"
    "--without-http_fastcgi_module"
    "--without-http_geo_module"
    "--without-http_grpc_module"
    "--without-http_limit_req_module"
    "--without-http_map_module"
    "--without-http_memcached_module"
    "--without-http_mirror_module"
    "--without-http_proxy_module"
    "--without-http_referer_module"
    "--without-http_rewrite_module"
    "--without-http_scgi_module"
    "--without-http_split_clients_module"
    "--without-http_ssi_module"
    "--without-http_upstream_hash_module"
    "--without-http_upstream_ip_hash_module"
    "--without-http_upstream_keepalive_module"
    "--without-http_upstream_zone_module"
    "--without-http_userid_module"
    "--without-http_uwsgi_module"
  ];

  NIX_CFLAGS_COMPILE = [
    "-Wno-error=implicit-fallthrough"
  ] ++ lib.optional stdenv.isDarwin "-Wno-error=deprecated-declarations";

  configurePlatforms = [ ];

  hardeningEnable = lib.optional (!stdenv.isDarwin) "pie";

  enableParallelBuilding = true;

  postInstall = ''
    mv $out/sbin $out/bin
    rm -rf $out/html
    rm $out/conf/{fastcgi,scgi,uwsgi,win-utf,koi-win}*
    rm $out/conf/*.default
  '';
})
