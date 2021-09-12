import subprocess
import datetime
from config.vendors.super_class import Super

class Eltex(Super):

    def getVersion(self): #gets network device version (str)
        version_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.4.1.89.53.4.1.5'.format(self.host), shell=True, stdout=subprocess.PIPE)
        booter_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.4.1.89.2.11.1'.format(self.host), shell=True, stdout=subprocess.PIPE)
        if version_get.returncode == 0:
            version_string = version_get.stdout.decode('utf-8').rstrip().split('\n')[0]
            booter_string = booter_get.stdout.decode('utf-8').rstrip().split('\n')[0]
            booter = booter_string.split(' ')[-1].replace('"','')
            version = version_string.split(' ')[-1].replace('"','')
            total = []
            total.append('OS:{}'.format(version))
            total.append('B:{}'.format(booter))
            return total
        return 'no response'

    def getModel(self): #gets network device model name (str)
        model_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.4.1.89.53.4.1.6'.format(self.host), shell=True, stdout=subprocess.PIPE)
        if model_get.returncode == 0:
            model_string = model_get.stdout.decode('utf-8').rstrip().split('\n')[0]
            model = model_string.split(' ')[3].replace('"', '')
            return model
        return 'no response'

    def getMacs(self): #gets network device mac address(-es) (list)
        mac_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.4.1.89.53.4.1.7'.format(self.host), shell=True, stdout=subprocess.PIPE)
        if mac_get.returncode == 0:
            mac_list = mac_get.stdout.decode('utf-8').rstrip().split('\n')
            macs = []
            for unit_mac in mac_list:
                macs.append(unit_mac.split(':')[-1].strip())
            formated_macs = []
            for mac in macs:
                formated_macs.append(mac.replace(' ',':'))
            return formated_macs
        return 'no response'
