#!/bin/sh

. settings


setup_rabbit () {

	apt-get install rabbitmq-server
	rabbitmqctl change_password guest ${RABBIT_PASSWORD}
	rabbitmqctl add_user ${RABBIT_USERNAME} ${RABBIT_USER_PASSWORD}
	rabbitmqctl add_vhost /glance
	rabbitmqctl set_permissions -p /glance nova '.*' '.*' '.*'
	rabbitmqctl add_vhost /nova
	rabbitmqctl set_permissions -p /nova nova '.*' '.*' '.*'
}

setup_rabbit
