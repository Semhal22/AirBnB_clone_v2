#!/usr/bin/env bash
# Sets up web server for deployment of web_static
apt-get -y update > /dev/null 2>&1;
apt-get -y install nginx > /dev/null 2>&1;

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

cat <<EOF > /data/web_static/releases/test/index.html
<html>
    <head></head>
    <body>
      ALX
    </body>
</html>
EOF
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu /data/
chgrp -R ubuntu /data/
cat <<EOF > /etc/nginx/sites-enabled/default
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;

        location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;
        }
}
EOF
nginx -s reload
