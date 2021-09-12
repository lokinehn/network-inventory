# network-inventory

Simple python script to inventory your network devices (Hostname, IP address, Vendor name, Model, Version, Uptime)

Requirements:

Linux OS with fping and snmpwalk packages installed


Use:
1) python main.py --- will start scanning with default subnet indicated in config/subnets.txt
2) python main.py test.txt --- will start scanning subnets indicated in "test.txt" file

*Added Vendors: Mikrotik, Eltex, Juniper, Arista
