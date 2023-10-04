#!/usr/bin/env bash
#Deployment of web static in servers

if ! command -v nginx &>/dev/null; then
	sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "This is a test" | sudo tee /data/web_static/releases/test/index.html >/dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"
nginx_config="location /hbnb_static/ {
    alias /data/web_static/current/;
    index index.html;
}"
if ! grep -q "location /hbnb_static/" "$config_file"; then
    sudo sed -i "/location \/ {/a $nginx_config" "$config_file"
fi

sudo service nginx restart

exit 0
