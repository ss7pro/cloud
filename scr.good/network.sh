#!/bin/bash

. settings

setup_nova_api () {
	apt-get -yy install nova-network python-configobj bridge-utils python-mysqldb daemontools daemontools-run

	echo "options nf_conntrack hashsize=131072" > /etc/modprobe.d/nf_conntrack.conf
	echo "# nf_conntrack" >> /etc/sysctl.conf
	echo "net.nf_conntrack_max=1048576" >> /etc/sysctl.conf
	echo "net.ipv4.netfilter.ip_conntrack_buckets=131072" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_filter=1" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_ignore=1" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_announce=2" >> /etc/sysctl.conf

	sysctl -p

	for i in 'nova-network' ; do
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
