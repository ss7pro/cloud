
MYSQL_PASSWORD=foh9ieYah5IeShoogoh7kae2
NOVA_MYSQL_PASSWORD=WiThagaijoh8oQuae7umoihe6shujey5

setup_nova () {
	apt-get install nova-ajax-console-proxy nova-api nova-api-ec2 nova-api-metadata nova-api-os-compute nova-api-os-volume nova-cert nova-common nova-compute nova-compute-qemu nova-compute-uml nova-console nova-doc nova-network nova-objectstore nova-scheduler nova-vncproxy nova-volume python-nova python-novaclient

	mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE nova;"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'nova'@'localhost'  IDENTIFIED BY '${NOVA_MYSQL_PASSWORD}';"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON nova.* TO 'nova'@'localhost';"
}

setup_nova
