#!/bin/sh

. settings


setup_keystone () {

	apt-get -y install pwgen keystone python-mysqldb
	service keystone stop
	cat /etc/init/keystone.conf  | sed '/^start on/s//#start on/' > /etc/init/keystone.conf.tmp
	mv /etc/init/keystone.conf.tmp /etc/init/keystone.conf
	mkdir -p /var/log/dt/keystone
	chmod 750 /var/log/dt/keystone
	chown keystone:syslog /var/log/dt/keystone
	mkdir -p /etc/service/.keystone
	touch /etc/service/.keystone/down
	mv /etc/service/.keystone /etc/service/keystone
	cat > /etc/service/keystone/run <<EOF
#!/bin/bash
exec setuidgid keystone keystone-all 2>&1
EOF
	chmod 755 /etc/service/keystone/run
	mkdir -p /etc/service/keystone/log
	cat > /etc/service/keystone/log/run <<EOF
#!/bin/bash
exec setuidgid keystone multilog t s16777215 n10 /var/log/dt/keystone
EOF
	chmod 755 /etc/service/keystone/log/run
}


populate_keystone () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}


# TENANT
	keystone tenant-create --name=admin
	keystone tenant-create --name=service

	KEYSTONE_ADMIN_TENANT_ID=`keystone tenant-list | egrep '\s+admin' | head -1 | awk ' { print $2 } '`
	KEYSTONE_SERVICE_TENANT_ID=`keystone tenant-list | egrep '\s+service' | head -1 | awk ' { print $2 } '`


# ROLES
	for i in 'admin' 'Member' 'KeystoneAdmin' 'KeystoneServiceAdmin' 'sysadmin' 'netadmin' ; do
		KEYSTONE_CUR_ROLE_ID=`keystone role-list | egrep "${i}" | head -1 | awk ' { print $2 } '`
		if [ "${KEYSTONE_CUR_ROLE_ID}" == "" ] ; then
			keystone role-create --name=$i
		fi
	done

	KEYSTONE_ADMIN_ROLE_ID=`keystone role-list | egrep '\s+admin' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_ADMIN_ROLE_ID}" == "" ] ; then
		echo "Nie ma admin role"
		exit 1
	fi
	KEYSTONE_KEYSTONEADMIN_ROLE_ID=`keystone role-list | egrep '\s+KeystoneAdmin' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_KEYSTONEADMIN_ROLE_ID}" == "" ] ; then
		echo "Nie ma keystoneadmin role"
		exit 1
	fi
	KEYSTONE_KEYSTONESERVICEADMIN_ROLE_ID=`keystone role-list | egrep '\s+KeystoneServiceAdmin' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_KEYSTONESERVICEADMIN_ROLE_ID}" == "" ] ; then
		echo "Nie ma keystoneserviceadmin role"
		exit 1
	fi

# USERS

	keystone user-create --name=admin --pass="${KEYSTONE_ADMIN_PASSWORD}"
	keystone user-create --name=glance --pass="${KEYSTONE_SERVICE_PASSWORD}"
	keystone user-create --name=nova --pass="${KEYSTONE_SERVICE_PASSWORD}"

	KEYSTONE_ADMIN_USER_ID=`keystone user-list | egrep '\s+admin' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_ADMIN_USER_ID}" == "" ] ; then
		echo "Nie ma admin user"
		exit 1
	fi
	KEYSTONE_GLANCE_USER_ID=`keystone user-list | egrep '\s+glance' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_GLANCE_USER_ID}" == "" ] ; then
		echo "Nie ma glance user"
		exit 1
	fi
	KEYSTONE_NOVA_USER_ID=`keystone user-list | egrep '\s+nova' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_NOVA_USER_ID}" == "" ] ; then
		echo "Nie ma nova user"
		exit 1
	fi

# ADD ROLES

# U: admin, R: admin, T:admin
	keystone user-role-add --user "${KEYSTONE_ADMIN_USER_ID}" --tenant_id "${KEYSTONE_ADMIN_TENANT_ID}" --role "${KEYSTONE_ADMIN_ROLE_ID}"

# U: admim, R:KeystoneAdmin, T:admin
	keystone user-role-add --user "${KEYSTONE_ADMIN_USER_ID}" --tenant_id "${KEYSTONE_ADMIN_TENANT_ID}" --role "${KEYSTONE_KEYSTONEADMIN_ROLE_ID}"


# U: admin, R:KeystoneServiceAdmin, T:admin
	keystone user-role-add --user "${KEYSTONE_ADMIN_USER_ID}" --tenant_id "${KEYSTONE_ADMIN_TENANT_ID}" --role "${KEYSTONE_KEYSTONESERVICEADMIN_ROLE_ID}"

# U: nova, R:admin, T:service
	keystone user-role-add --user "${KEYSTONE_NOVA_USER_ID}" --tenant_id "${KEYSTONE_SERVICE_TENANT_ID}" --role "${KEYSTONE_ADMIN_ROLE_ID}"

# U:glance, R:admin, T:service
	keystone user-role-add --user "${KEYSTONE_GLANCE_USER_ID}" --tenant_id "${KEYSTONE_SERVICE_TENANT_ID}" --role "${KEYSTONE_ADMIN_ROLE_ID}"

	KEYSTONE_CUR_IDENTITY_SERVICE_ID=`keystone service-list | egrep 'keystone | identity' | head -1 | awk ' { print $2 } '`
	if [ "${KEYSTONE_CUR_IDENTITY_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "keystone" --type  "identity" --description  "Openstack Identity Service"
	fi
	KEYSTONE_CUR_IDENTITY_SERVICE_ID=`keystone service-list | egrep 'keystone | identity' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "r4cz1" --publicurl "http://${KEYSTONE_IP}:5000/v2.0" --adminurl "http://${KEYSTONE_IP}:35357/v2.0" --internalurl "http://${KEYSTONE_IP}:5000/v2.0" --service_id "${KEYSTONE_CUR_IDENTITY_SERVICE_ID}"

}

register_glance () {

	export SERVICE_TOKEN=${KEYSTONE_SERVICE_TOKEN}
	export SERVICE_ENDPOINT=${KEYSTONE_SERVICE_ENDPOINT}

	GLANCE_CUR_IMAGE_SERVICE_ID=`keystone service-list | egrep 'glance | image' | head -1 | awk ' { print $2 } '`
	if [ "${GLANCE_CUR_IMAGE_SERVICE_ID}" == "" ] ; then
		keystone  service-create --name "glance" --type  "image" --description  "Openstack Glance Service"
	fi
	GLANCE_CUR_IMAGE_SERVICE_ID=`keystone service-list | egrep 'glance | image' | head -1 | awk ' { print $2 } '`
	keystone  endpoint-create --region "r4cz1" --publicurl "http://${GLANCE_IP}:9292/v1" --adminurl "http://${GLANCE_IP}:9292/v1" --internalurl "http://${GLANCE_IP}:9292/v1" --service_id "${GLANCE_CUR_IMAGE_SERVICE_ID}"

}


#setup_keystone
#populate_keystone
register_glance
