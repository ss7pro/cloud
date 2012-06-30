#!/bin/bash


RABBITIMQ_HOST=`cat /etc/nova/nova.conf | egrep '^rabbit_host=' | awk -v FS='=' ' { print $2 } '`
RABBITIMQ_PORT=5672

nova_dir_setup () {

	mkdir -p /var/lock/nova
	chmod 775 /var/lock/nova
	chown root:nova /var/lock/nova

}

check_rabbit () {

	echo | timeout -k 1 1 nc ${RABBITIMQ_HOST} ${RABBITIMQ_PORT} 1>/dev/null 2>/dev/null
	RABBITIMQ_STATUS=$?
}

check_nova_network () {
	NOVA_NETWORK_STATUS=`nova-manage service list | grep nova-network | grep ':-)' | wc -l`
}
check_nova_scheduler () {
	NOVA_SCHEDULER_STATUS=`nova-manage service list | grep nova-scheduler | grep ':-)' | wc -l`
}


before_nova_compute () {
	nova_dir_setup
	check_rabbit
	if [ ${RABBITIMQ_STATUS} -ge 1 ] ; then
		exit 1
	fi
	check_nova_network
	if [ ${NOVA_NETWORK_STATUS} -eq 0 ] ; then
		exit 1
	fi
	check_nova_scheduler
	if [ ${NOVA_SCHEDULER_STATUS} -eq 0 ] ; then
		exit 1
	fi
}

before_nova () {
	nova_dir_setup
	check_rabbit
	if [ ${RABBITIMQ_STATUS} -ge 1 ] ; then
		exit 1
	fi
}
