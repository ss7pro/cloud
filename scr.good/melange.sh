
MYSQL_PASSWORD=foh9ieYah5IeShoogoh7kae2
MELANGE_MYSQL_PASSWORD=ro8mohgh1faiZah2Iraecheezeph1chi

setup_melange () {
	apt-get install python-kombu

	mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE melange;"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'melange'@'localhost'  IDENTIFIED BY '${MELANGE_MYSQL_PASSWORD}';"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON melange.* TO 'melange'@'localhost';"
}

setup_melange
