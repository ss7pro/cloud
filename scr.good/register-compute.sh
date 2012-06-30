#!/bin/bash

. settings

register_compute () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}

	NOVA_API_CUR_SERVICE_ID=`keystone service-list | egrep 'nova' | egrep 'compute' | head -1 | awk ' { print $2 } '`
	if [ "${NOVA_API_CUR_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "nova" --type  "compute" --description  "Nova Compute Service"
	fi
	NOVA_API_CUR_SERVICE_ID=`keystone service-list | egrep 'nova' | egrep 'compute' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "r4cz1" --publicurl "http://${NOVA_API_IP}:8774/v2/"'$(tenant_id)s' --adminurl "http://${NOVA_API_IP}:8774/v2/"'$(tenant_id)s' --internalurl "http://${NOVA_API_IP}:8774/v2/"'$(tenant_id)s' --service_id "${NOVA_API_CUR_SERVICE_ID}"

}

register_compute
