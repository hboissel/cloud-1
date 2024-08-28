FROM debian:bullseye-slim@sha256:9058862a1be84689bd13292549ba981364f85ff99e50a612f94b188ac69db137

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install mariadb-server -y

COPY ./conf/50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf
COPY ./tools/configDB.sh ./configDB.sh

RUN chmod +x /configDB.sh

ENTRYPOINT ["bash", "configDB.sh"]
CMD ["mysqld"]
