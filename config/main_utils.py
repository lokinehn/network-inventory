import subprocess
import ipaddress
import csv

def createTable(inventory_list):
    with open('./inventory_files/inventory.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Hostname', 'IP', 'Vendor', 'Model', 'Mac-address', 'Version', 'Uptime'])
        for row in inventory_list:
            writer.writerow(list(row.values()))


def checkAlive(net_address):
    try:
        subnet = ipaddress.ip_network(net_address)
        fping_output = subprocess.run('fping -g -r 1 {}'.format(subnet), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
        alive_hosts = []
        for host in fping_output.strip().split('\n'):
            if host.find('alive') != -1:
                alive_hosts.append(host.replace(' is alive', ''))
        with open('config/last_alived_hosts.txt', 'w') as f:
            for host in alive_hosts:
                f.write(host + '\n')
        return alive_hosts
    except ValueError:
        print('Wrong network address')

def checkVendor(alive_hosts):
    vendor_dict = {}
    eltex = []
    arista = []
    mikrotik = []
    juniper = []
    other_shit = []
    for host in alive_hosts:
        print('Now checking host --- {}'.format(host))
        snmpwalk_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.2.1.1.1.0'.format(host), shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')
        if snmpwalk_get.find('MES') != -1:
            eltex.append(host)
        elif snmpwalk_get.find('Juniper') != -1:
            juniper.append(host)
        elif snmpwalk_get.find('Arista') != -1:
            arista.append(host)
        elif snmpwalk_get.find('RouterOS') != -1:
            mikrotik.append(host)
        else:
            other_shit.append(host)
    vendor_dict['Eltex'] = eltex
    vendor_dict['Juniper'] = juniper
    vendor_dict['Mikrotik'] = mikrotik
    vendor_dict['Arista'] = arista
    vendor_dict['Others'] = other_shit
    return vendor_dict

def sortOutput(result):
    addresses = []
    for line in result:
        addresses.append(ipaddress.ip_address(line['IP']))
        addresses.sort()
        result_list = []
        for address in addresses:
            for line in result:
                if line['IP'] == str(address):
                    result_list.append(line)
    return result_list

def getAll(hosts, class_name=None):
    inventory = []
    for host in hosts:
        if not class_name:
            host_inventory = {'IP': host, 'hostname': "Not answered by SNMP or didn't get by any template"}
            inventory.append(host_inventory)
        else:
            ins = class_name(host)
            host_inventory = {'IP': host, 'hostname': ins.getHostname(), 'vendor': str(ins.__class__.__name__), 'model': ins.getModel(), 'mac-address': ','.join(ins.getMacs()), 'version': ins.getVersion(), 'uptime': ins.getUptime()}
            inventory.append(host_inventory)
            host_inventory = {'IP': host}
    return inventory
