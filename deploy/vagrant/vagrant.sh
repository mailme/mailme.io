#!/bin/bash

export PATH=$PATH:/usr/bin:/usr/sbin:/bin:/sbin

function run_updates(){
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade
}

hostname mailme.local
echo mailme.local > /etc/hostname
echo mailme.local > /etc/mailname
echo "127.0.0.1 mailme mailme.local\n" >> /etc/hosts

run_updates

# TODO: Puppet
