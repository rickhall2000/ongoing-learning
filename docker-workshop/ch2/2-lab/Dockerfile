FROM ubuntu:18.04
ENV DEBIAL_FRONTEND=noninteractive
# This never finishes. I think there is an issue with php
RUN apt-get update && apt-get -y install apache2 php
COPY *.php /var/www/html
WORKDIR /var/www/html
EXPOSE 80
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]
