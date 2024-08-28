#!bin/bash


if [ -f /var/www/wordpress/wp-config.php ]
then
	echo "wordpress already downloaded"
else
	cd /var/www/wordpress/
	wp config create --allow-root --dbname=$SQL_DATABASE --dbuser=$SQL_USER --dbpass=$SQL_PASSWORD --dbhost=mariadb:3306 >> /log.txt
	wp core install     --url=$DOMAIN_NAME --title=$SITE_TITLE --admin_user=$ADMIN_USER --admin_password=$ADMIN_PASSWORD --admin_email=$ADMIN_EMAIL --allow-root >> /log.txt
	wp user create      --allow-root --role=author $USER1_LOGIN $USER1_MAIL --user_pass=$USER1_PASS >> /log.txt

fi

if [ ! -d /run/php ]; then
	mkdir -p /run/php
fi

exec /usr/sbin/php-fpm7.4 -F -R
