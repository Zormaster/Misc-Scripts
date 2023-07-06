#!/bin/bash

tail -Fn0 /var/log/apache2/access.log | \
while read line; do
    echo "$line" | grep vmware-ovftool.tar.gz
    if [ $? = 0 ] 
    then
        (
        echo "# Restarting Sensor"
        notify-send 'ESXi Deployment' 'Deploying VMs. Do not turn off the ESXi box.'
        sleep 20
        echo "10"
        sleep 40
        echo "15"
        sleep 1m
        echo "25"
        sleep 2m
        echo "30"
        notify-send 'ESXi Deployment' 'Wait period finished. Begining VM Deployment.'

        echo "# Getting User Input"
        OUTPUT=$(zenity --forms --add-entry=Hostname --add-entry='Company Name' --add-entry='Location' --add-entry='Password' --text="Sensor Configuration")
        HOSTNAME=$(awk -F\| '{print $1}' <<<$OUTPUT)
        COMPANY=$(awk -F\| '{print $2}' <<<$OUTPUT)
        LOCATION=$(awk -F\| '{print $3}' <<<$OUTPUT)
        PASSWORD=$(awk -F\| '{print $4}' <<<$OUTPUT)
        DOMOTZ="Domotz-$COMPANY-$LOCATION"

        echo "40"
        echo "# Setting Hostname"
        ssh-keygen -f "/home/soc/.ssh/known_hosts" -R "172.0.0.16"
        sshpass -p $PASSWORD ssh -o StrictHostKeyChecking=no "root@172.0.0.16" esxcli system hostname set --host=$HOSTNAME

        echo "# Deploying Domotz VM"
	/home/soc/Desktop/Sensor\ Build/vmware-ovftool/ovftool --acceptAllEulas --datastore=datastore1 --powerOn --noSSLVerify --net:"custom=LAN" --name=$DOMOTZ /var/www/html/domotz.ova "vi://root:$PASSWORD@172.0.0.16" 
        echo "60"
        echo "# Deploying Scanner"
        /home/soc/Desktop/Sensor\ Build/vmware-ovftool/ovftool --acceptAllEulas --datastore=datastore1 --noSSLVerify --net:"MGT=MGT" --name=scanner /var/www/html/scanner.ova "vi://root:$PASSWORD@172.0.0.16" 
        echo "70"
        
        echo "# Running Updates"
        echo "80"
        
        vmrc -H 172.0.0.16 -U root -P $PASSWORD -M 1

        echo "100"
        echo "# Deployment Complete"
        ) |
        zenity --progress --title="Deploying VMs" --percentage=0
        notify-send 'ESXi Deployment' 'VMs have been deployed. You may now turn off the device.'
    fi
done

