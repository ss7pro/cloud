#!/bin/bash


apt-get -yy install xfsprogs


for i in /dev/sdc:drv1 /dev/sdd:drv2 /dev/sde:drv3 /dev/sdf:drv4 ; do
	d=`echo $i | awk -v FS=':' ' { print $1 } '`
	l=`echo $i | awk -v FS=':' ' { print $2 } '`
	mkfs.xfs -L $l $d
	mkdir -p /srv/ceph/osd/$l
	echo "LABEL=\"${l}\" /srv/ceph/osd/${l} xfs nodev,noexec,noatime,nodiratime,noquota 0 3" >> /etc/fstab
done
