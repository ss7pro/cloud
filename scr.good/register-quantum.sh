register_quantum () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}

	QUANTUM_CUR_NETWORK_SERVICE_ID=`keystone service-list | egrep 'quantum | network' | head -1 | awk ' { print $2 } '`
	if [ "${QUANTUM_CUR_NETWORK_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "quantum" --type  "network" --description  "Openstack Glance Service"
	fi
	QUANTUM_CUR_NETWORK_SERVICE_ID=`keystone service-list | egrep 'quantum | network' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "regionOne" --publicurl "http://${QUANTUM_API_IP}:9696/" --adminurl "http://${QUANTUM_API_IP}:9696/" --internalurl "http://${QUANTUM_API_IP}:9696/" --service_id "${QUANTUM_CUR_NETWORK_SERVICE_ID}"

}

