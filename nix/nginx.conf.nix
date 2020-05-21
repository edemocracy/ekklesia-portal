{ staticFiles, listen, serverName, mimeTypeFile }:
''
daemon off;

events {
    worker_connections  1024;
}


http {
    include ${mimeTypeFile};
    sendfile off;
    error_log /dev/stderr;
    access_log /dev/stdout;

    server {
        listen ${listen};
        server_name ${serverName};
        client_body_buffer_size 1m;
        client_max_body_size    1m;

        location /static {
            add_header Access-Control-Allow-Origin *;
            add_header Cache-Control public;
            alias ${staticFiles};
        }
    }
}
''
