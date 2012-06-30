#!/bin/bash

. settings


setup_nova_api () {
	apt-get -yy install nova-cert nova-api daemontools daemontools-run

	for i in 'nova-api' 'nova-cert' ; do
		service $i stop
		cat /etc/init/$i.conf  | sed '/^start on/s//#start on/' > /etc/init/$i.conf.tmp
		mv /etc/init/$i.conf.tmp /etc/init/$i.conf
		mkdir -p /var/log/dt/$i
		chmod 750 /var/log/dt/$i
		chown nova:syslog /var/log/dt/$i
		mkdir -p /etc/service/.$i
		touch /etc/service/.$i/down
		mv /etc/service/.$i /etc/service/$i
		mkdir -p /etc/service/.helpers
		cp dthelper.sh /etc/service/.helpers
		cat > /etc/service/$i/run <<EOF
#!/bin/bash

. /etc/service/.helpers/dthelper.sh

before_nova

exec setuidgid nova ${i} --config-file=/etc/nova/nova.conf 2>&1
EOF
		chmod 755 /etc/service/$i/run
		mkdir -p /etc/service/$i/log
		cat > /etc/service/$i/log/run <<EOF
#!/bin/bash
exec setuidgid nova multilog t s16777215 n10 /var/log/dt/${i}
EOF
		chmod 755 /etc/service/$i/log/run
	done


	
}

setup_nova_api
