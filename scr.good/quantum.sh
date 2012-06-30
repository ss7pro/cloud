#!/bin/bash

. settings


setup_quantum () {

	mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE quantum;"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'quantum'@'localhost'  IDENTIFIED BY '${QUANTUM_MYSQL_PASSWORD}';"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON quantum.* TO 'quantum'@'localhost';"
	mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE DATABASE quantum;"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "CREATE USER 'quantum'@'localhost'  IDENTIFIED BY '${QUANTUM_MYSQL_PASSWORD}';"
        mysql -u root -p"${MYSQL_PASSWORD}" -e "GRANT ALL ON quantum.* TO 'quantum'@'localhost';"

	for i in 'quantum' ; do
		service $i stop
		cat /etc/init/$i.conf  | sed '/^start on/s//#start on/' > /etc/init/$i.conf.tmp
		mv /etc/init/$i.conf.tmp /etc/init/$i.conf
		mkdir -p /var/log/dt/$i
		chmod 750 /var/log/dt/$i
		chown quantum:syslog /var/log/dt/$i
		mkdir -p /etc/service/.$i
		touch /etc/service/.$i/down
		mv /etc/service/.$i /etc/service/$i
		cat > /etc/service/$i/run <<EOF
#!/bin/bash
exec setuidgid quantum ${i} --config-file=/etc/quantum.conf 2>&1
EOF
		chmod 755 /etc/service/$i/run
		mkdir -p /etc/service/$i/log
		cat > /etc/service/$i/log/run <<EOF
#!/bin/bash
exec setuidgid quantum multilog t s16777215 n10 /var/log/dt/${i}
EOF
		chmod 755 /etc/service/$i/log/run
	done


}


setup_quantum
