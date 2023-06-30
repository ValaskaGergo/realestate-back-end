### Development, production környezet inicializálása

##### Sajátgépen szükséges

- **Python: 3.9**
- **Virtualenv: 3.x**
- **Pip: 3.x**
- **NGINX: 1.x**
- **Supervisor: 4.x**
- 
sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y python3.4-dev
sudo apt-get install -y libpq-dev

##### Virtualenvben szükséges

- **Gunicorn:** benne van a requirements-ben

##### Virtualenv

~~~
[host@host ~]$ python3.9 -m venv venv
[host@host ~]$ source venv/bin/activate
(venv)[host@host ~]$ pip install --upgrade pip
(venv)[host@host ~]$ pip install -r requirements.txt
(venv)[host@host ~]$ gunicorn --reload --threads 2 app:app -b localhost:3001 &
      ctrl-c
(venv)[host@host ~]$ pkill gunicorn
~~~

##### Supervisor

~~~
[root@root ~]# mkdir -p /var/log/api.anlibreeders.com
[root@root ~]# echo_supervisord_conf > /etc/supervisord.conf # csak ha nem létezik
[root@root ~]# cp /etc/supervisord.conf /etc/supervisord.conf.old
[root@root ~]# cp api.anlibreeders.com.ini /etc/supervisor.d/ #: development mappaban van
[root@root ~]# supervisorctl reread
[root@root ~]# supervisorctl update
[root@root ~]# supervisorctl status
[host@host ~]$ curl -LI http://127.0.0.1:3001/ -o /dev/null -w '%{http_code}\n' -s
[root@root ~]# supervisorctl stop/start api.anlibreeders.com.me
~~~

##### NGINX

~~~
[root@root ~]# mkdir -p /var/log/api.anlibreeders.com
[root@root ~]# vim /etc/nginx/nginx.conf #: legyen benne alul az: include sites-enabled/*;
[root@root ~]# cp api.anlibreeders.com /etc/nginx/sites-available/ #: development mappaban van
[root@root ~]# ln -s /etc/nginx/sites-available/api.anlibreeders.com /etc/nginx/sites-enabled/
[root@root ~]# nginx -t
[root@root ~]# systemctl reload nginx
~~~

~~~
[root@root ~]# vim /etc/hosts # Az /etc/hosts-ba fel kell venni a (sub)domaineket:
~~~

~~~
127.0.0.1    www.anlibreeders.com
127.0.0.1    anlibreeders.com
127.0.0.1    www.api.anlibreeders.com
127.0.0.1    api.anlibreeders.com
127.0.0.1    www.socket.anlibreeders.com
127.0.0.1    socket.anlibreeders.com
~~~

##### LOCALHOST SSL

~~~
[host@host ~]$ mkdir cert # ezt bárhol a saját gépeden
[host@host ~]$ openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout RootCA.key -out RootCA.pem -subj "/C=US/CN=Example-Root-CA"
[host@host ~]$ openssl x509 -outform pem -in RootCA.pem -out RootCA.crt
[host@host ~]$ touch domains.ext
[host@host ~]$ vim domains.ext
~~~

~~~
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = www.anlibreeders.com
DNS.2 = anlibreeders.com
DNS.3 = www.api.anlibreeders.com
DNS.4 = api.anlibreeders.com
DNS.5 = www.socket.anlibreeders.com
DNS.6 = socket.anlibreeders.com
~~~

~~~
[host@host ~]$ openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=localhost.local"
[host@host ~]$ openssl x509 -req -sha256 -days 1024 -in localhost.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out localhost.crt
~~~

##### NPM

~~~
[host@host ~]$ cd app/static
[host@host ~]$ npm install
~~~

##### DB

~~~
[host@anlibreeders-back-end ~]$ flask db init
[host@anlibreeders-back-end ~]$ flask db migrate
[host@anlibreeders-back-end ~]$ flask db upgrade
~~~

##### CREATE ADMIN SETTINGS

~~~
[host@anlibreeders-back-end ~]$ flask commands create-admin-settings
~~~

##### HELP

Amikor egy user admin lesz, az **user_permission** tábla legyen... \
**is_worker**: True \
**is_admin**: True


**Magyarország**: 
Cég, magánszemély, mindenkinek 27%

**EU**:
EU-s adószámosok, nullás, 
Uniós ország, eus adószámmal nem rendelkező cég, az adott ország áfája.
Eu-s magánszemély, az adott országban lévő áfát számoljuk.

**Harmadik ország**:
Magánszemély és cég, mindenki nullás.


##### 3RD APIs
~~~
https://vatlayer.com
gyorgyi.szuhai@gmail.com
LwdvKLjev8EsDsv
~~~