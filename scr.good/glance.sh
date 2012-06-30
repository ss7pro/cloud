#!/bin/sh

. settings


setup_glance () {
	apt-get -yy install glance



	for i in 'glance-api' 'glance-registry' ; do
		service $i stop
		cat /etc/init/$i.conf  | sed '/^start on/s//#start on/' > /etc/init/$i.conf.tmp
		mv  /etc/init/$i.conf.tmp /etc/init/$i.conf
		mkdir -p /var/log/dt/$i
		chmod 750 /var/log/dt/$i
		chown glance:syslog /var/log/dt/$i
		mkdir -p /etc/service/.$i
		touch /etc/service/.$i/down
		mv /etc/service/.$i /etc/service/$i
		cat > /etc/service/$i/run <<EOF
#!/bin/bash
exec setuidgid glance ${i} 2>&1
EOF
		chmod 755 /etc/service/$i/run
		mkdir -p /etc/service/$i/log
		cat > /etc/service/$i/log/run <<EOF
#!/bin/bash
exec setuidgid glance multilog t s16777215 n10 /var/log/dt/${i}
EOF
		chmod 755 /etc/service/$i/log/run
	done
}


setup_glance
