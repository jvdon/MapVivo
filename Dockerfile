FROM mysql
EXPOSE 3306 33060
ENV MYSQL_ROOT_PASSWORD="root"
CMD [ "/bin/curl -o /tmp/create_database.sql https://raw.githubusercontent.com/jvdon/MapVivo/main/create_database.sql && /bin/mysql -u root -p'root' < /tmp/create_database.sql" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "echo 'SELECT version();'| mysql -p'root'" ]
