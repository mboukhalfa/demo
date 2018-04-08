#download nginx source code and extract it
wget http://nginx.org/download/nginx-1.10.3.tar.gz
tar -xvf nginx-1.10.3.tar.gz

# install depencies and build tools
apt-get update
apt-get install -y build-essential libpcre3 libpcre3-dev openssl libssl-dev

#download upload module
git clone https://github.com/fdintino/nginx-upload-module.git
git clone https://github.com/masterzen/nginx-upload-progress-module.git

cd nginx-1.10.3
groupadd -r nginx
useradd -r -g nginx nginx

./configure --prefix=/etc/nginx \
            --user=nginx\
            --group=nginx\
            --sbin-path=/usr/sbin/nginx \
            --conf-path=/etc/nginx/nginx.conf \
            --error-log-path=/var/log/nginx/error.log \
            --http-log-path=/var/log/nginx/access.log \
            --pid-path=/var/run/nginx.pid \
            --lock-path=/var/run/nginx.lock \
            --with-pcre \
            --with-file-aio \
            --with-http_gzip_static_module \
            --with-http_realip_module \
            --with-http_ssl_module \
            --with-http_stub_status_module \
            --with-http_auth_request_module \
            --add-module=../nginx-upload-module/\
            --add-module=../nginx-upload-progress-module
make
make install

# clean
cd ../
rm -rf nginx-1.10.3 nginx-1.10.3.tar.gz nginx-upload-module ginx-upload-progress-module