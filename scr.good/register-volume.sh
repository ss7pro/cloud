#!/bin/bash

. settings

register_volume () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}

	NOVA_API_CUR_SERVICE_ID=`keystone service-list | egrep 'nova' | egrep 'volume' | head -1 | awk ' { print $2 } '`
	if [ "${NOVA_API_CUR_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "nova" --type  "volume" --description  "Nova Volume Service"
	fi
	NOVA_API_CUR_SERVICE_ID=`keystone service-list | egrep 'nova' | egrep 'volume' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "r4cz1" --publicurl "http://${NOVA_API_IP}:8776/v1/"'$(tenant_id)s' --adminurl "http://${NOVA_API_IP}:8776/v1/"'$(tenant_id)s' --internalurl "http://${NOVA_API_IP}:8776/v1/"'$(tenant_id)s' --service_id "${NOVA_API_CUR_SERVICE_ID}"

}

register_volume
