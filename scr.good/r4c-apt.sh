#!/bin/bash


cat > /etc/apt/preferences.d/r4c <<EOF
Package: *
Pin: release l=r4c
Pin-Priority: 1001
EOF



cat > /etc/apt/sources.list.d/r4c.list <<EOF
deb http://10.76.0.117/r4c precise main universe
deb-src http://10.76.0.117/r4c precise main universe
EOF
