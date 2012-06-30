#!/bin/bash

. settings

setup_novnc () {
	apt-get -yy novnc python-numpy

	for i in 'nova-novncproxy' ; do
		service novnc stop
		update-rc.d -f novnc remove
		mkdir -p /var/log/dt/$i
		chmod 750 /var/log/dt/$i
		chown nova:syslog /var/log/dt/$i
		mkdir -p /etc/service/.$i
		touch /etc/service/.$i/down
		mv /etc/service/.$i /etc/service/$i
		cat > /etc/service/$i/run <<EOF
#!/bin/bash
exec setuidgid nova $i --config-file=/etc/nova/nova.conf --web /usr/share/novnc/ 2>&1
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

setup_novnc
