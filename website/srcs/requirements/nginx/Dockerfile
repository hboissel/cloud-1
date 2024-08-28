FROM alpine:edge@sha256:b93f4f6834d5c6849d859a4c07cc88f5a7d8ce5fb8d2e72940d8edd8be343c04

RUN apk update \
 && apk add --no-cache nginx
 
COPY conf/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/ssl

COPY conf/*.pem /etc/nginx/ssl/

RUN getent group www-data || addgroup -g 82 www-data

RUN adduser -D -H -u 82 -G www-data -s /sbin/nologin www-data

RUN mkdir -p /var/run/nginx \
 && mkdir -p /var/www/wordpress \
 && chmod 755 /var/www/wordpress \
 && chown -R www-data:www-data /var/www/wordpress

CMD [ "nginx", "-g", "daemon off;" ] 
