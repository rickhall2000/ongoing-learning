FROM ubuntu:latest
RUN apt-get update && apt-get install apache2 -y
WORKDIR /var/www/html/
COPY index.html .
ADD https://assets.stickpng.com/images/62a9c7c08ff6441a2952dad3.png ./logo.png
CMD ["ls"]
