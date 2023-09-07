FROM basic-base

CMD makedir -p /var/www/html

WORKDIR /var/www/html/

ADD VERSION /var/www/html/
ADD Dockerfile /var/www/html/
RUN cat Dockerfile
