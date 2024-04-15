FROM mysql
EXPOSE 3306 33060
ENV MYSQL_ROOT_PASSWORD="root"
ENV MYSQL_DATABASE_NAME="cache"
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "echo 'SELECT version();'| mysql -p'root'" ]
