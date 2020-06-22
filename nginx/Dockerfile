FROM nginx:latest

RUN apt-get update -y && \
apt-get install -y nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir -p /var/www

COPY ./static /var/www