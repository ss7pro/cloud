
setup_firewall () {

	apt-get -yy install shorewall vlan keepalived

	echo "options nf_conntrack hashsize=131072" > /etc/modprobe.d/nf_conntrack.conf
	echo "nf_conntrack" >> /etc/modules

	echo "# nf_conntrack" >> /etc/sysctl.conf
	echo "net.nf_conntrack_max=1048576" >> /etc/sysctl.conf
	echo "net.ipv4.netfilter.ip_conntrack_buckets=131072" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_filter=1" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_ignore=1" >> /etc/sysctl.conf
	echo "net.ipv4.conf.all.arp_announce=2" >> /etc/sysctl.conf

	sysctl -p
}


setup_firewall
