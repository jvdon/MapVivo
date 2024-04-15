FROM mysql
EXPOSE 3306 33060
ENV MYSQL_ROOT_PASSWORD="root"
RUN "mysql -u root -p'root' < $(curl )"
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "echo 'SELECT version();'| mysql -p'root'" ]
