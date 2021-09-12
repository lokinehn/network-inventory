#main file to do stuff
import os
from sys import argv
from config.main_utils import checkAlive, checkVendor, getAll, createTable, sortOutput
import config.vendors.eltex as eltex
import config.vendors.juniper as juniper
import config.vendors.mikrotik as mikrotik
import config.vendors.arista as arista


def openFile(file_name):
    return open(file_name, 'r').readlines()


def getInventory(*args):
    inventory = []
    for vendor_type in args:
        inventory.extend(vendor_type)
    return inventory

if __name__ == '__main__':
    alive_hosts = []
    #find subnets file to check
    if len(argv) == 1:
        file_name = 'config/subnets.txt'
    else:
        file_name = argv[1]
    for subnet in openFile(file_name):
        subnet_alive_hosts = checkAlive(subnet.strip())
        alive_hosts.extend(subnet_alive_hosts)
    if os.path.isfile('config/exceptions.txt'):
        exception_list = open('config/exceptions.txt').read()
        exception_list = exception_list.split('\n')
        alive_hosts = list(set(alive_hosts) - set(exception_list))
    vendor_dict = checkVendor(alive_hosts)
    eltex_list = getAll(vendor_dict['Eltex'], eltex.Eltex)
    juniper_list = getAll(vendor_dict['Juniper'], juniper.Juniper)
    mikrotik_list = getAll(vendor_dict['Mikrotik'], mikrotik.Mikrotik)
    arista_list = getAll(vendor_dict['Arista'], arista.Arista)
    others_list = getAll(vendor_dict['Others'])
    result = getInventory(eltex_list, juniper_list, mikrotik_list, arista_list, others_list)
    result_list = sortOutput(result)
    for row in result_list:
        print(row)
    createTable(result_list)
