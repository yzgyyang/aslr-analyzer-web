# ASLR Analyzer Flask Web app

This is a Web app aiming to demonstrate ASLR performance on different OSes.

Stack: Python + Flask + Docker + uwsgi + Nginx (reverse proxy)

The site is live on: http://app.charlieyang.me/aslr

## Deployment

Assume the machine for deployment is running Ubuntu 16.04.

### Get source
```
git clone https://github.com/yzgyyang/aslr-analyzer-app/
mv aslr-analyzer-app /var/www/aslr
cd /var/www/aslr
```

### Start Docker x WSGI
```
apt install docker.io
docker build -t aslr_app .
docker run -p 8000:8000 -t aslr_app
```

Management:
```
docker ps
docker stop [num]
```

### Init Nginx
```
apt install nginx
chown www-data:www-data /var/www/aslr -R
```

Management:
```
service nginx [start, stop, restart]
```

### Configure reverse proxy

Remove `default` file from `sites-enabled/`:
```
rm -rf /etc/nginx/sites-enabled/default
```

Add the following to /etc/nginx/sites-available/aslr:
```
upstream aslr {
  server 127.0.0.1:8000;
}
server {
  listen *:80;
  root /var/www/aslr/Flask;

  location /aslr/static {
    alias /var/www/aslr/Flask/static;
  }

  location /aslr {
    proxy_pass http://aslr;
  }
}
```

Make a symlink:
```
ln -s /etc/nginx/sites-available/aslr /etc/nginx/sites-enabled/aslr
```

Restart the server:
```
service nginx restart
```
