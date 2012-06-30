#!/bin/bash

. settings

register_ec2 () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}

	EC2_API_CUR_SERVICE_ID=`keystone service-list | egrep 'ec2' | head -1 | awk ' { print $2 } '`
	if [ "${EC2_API_CUR_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "ec2" --type  "ec2" --description  "EC2 Service"
	fi
	EC2_API_CUR_SERVICE_ID=`keystone service-list | egrep 'ec2' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "r4cz1" --publicurl "http://${NOVA_API_IP}:8773/services/Cloud" --adminurl "http://${NOVA_API_IP}:8773/services/Admin" --internalurl "http://${NOVA_API_IP}:8773/services/Cloud" --service_id "${EC2_API_CUR_SERVICE_ID}"

}

register_ec2
