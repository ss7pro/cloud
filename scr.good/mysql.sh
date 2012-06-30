#!/bin/sh

. settings



setup_mysql () {

	cat > ~/.my.cnf <<MYCNF
[client]
user=root
password=${MYSQL_PASSWORD}
host=%
MYCNF

	cat <<MYSQL_PRESEED | sudo debconf-set-selections
mysql-server-5.1 mysql-server/root_password password $MYSQL_PASSWORD
mysql-server-5.1 mysql-server/root_password_again password $MYSQL_PASSWORD
mysql-server-5.1 mysql-server/start_on_boot boolean true
MYSQL_PRESEED
	apt-get -yy install mysql-server
}

setup_mysql


# API
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE nova;"
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'nova'@'%'  IDENTIFIED BY '${NOVA_MYSQL_PASSWORD}';"
mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON nova.* TO 'nova'@'%';"

# GLANCE
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE glance;"
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'glance'@'%'  IDENTIFIED BY '${GLANCE_MYSQL_PASSWORD}';"
mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON glance.* TO 'glance'@'%';"

# KEYSTONE
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE keystone;"
mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'keystone'@'%'  IDENTIFIED BY '${KEYSTONE_MYSQL_PASSWORD}';"
mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON keystone.* TO 'keystone'@'%';"
