server {
    listen 80;
    server_name www.api.anlibreeders.com api.anlibreeders.com;

    location / {
        return 301 https://api.anlibreeders.com$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name api.anlibreeders.com;

    ssl on;
    ssl_certificate /etc/letsencrypt/live/api.anlibreeders.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.anlibreeders.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        add_header 'Access-Control-Allow-Origin' 'https://anlibreeders.com';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PUT';
        add_header 'Access-Control-Allow-Headers' 'User-Agent,Keep-Alive,Content-Type, X-API-KEY';

        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
        proxy_pass http://127.0.0.1:3001;
    }

    access_log /var/log/api.anlibreeders.com/api.anlibreeders.com.nginx.access.log;
    error_log /var/log/api.anlibreeders.com/api.anlibreeders.com.nginx.error.log;
}