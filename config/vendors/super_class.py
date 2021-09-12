import subprocess
import datetime

 
class Super:
    def __init__(self, host):
        self.host = host
    
    def snmpCheck(self):
        return subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.2.1.1.1.0'.format(self.host), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode

    def getHostname(self):
        hostname_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.2.1.1.5.0'.format(self.host), shell=True, stdout=subprocess.PIPE)
        if hostname_get.returncode == 0:
            hostname_string = hostname_get.stdout.decode('utf-8').rstrip().split('\n')[0]
            hostname = hostname_string.split(' ')[-1].replace('"', '')
            return hostname
        return 'no response'

    def getUptime(self):
        uptime_get = subprocess.run('snmpwalk -v2c -c public {} 1.3.6.1.2.1.1.3'.format(self.host), shell=True, stdout=subprocess.PIPE)
        if uptime_get.returncode == 0:
            uptime_list = uptime_get.stdout.decode('utf-8').rstrip().split(' ')
            uptime_sticks = int(uptime_list[3][1:-3])
            uptime = str(datetime.timedelta(seconds=uptime_sticks))
            return uptime
        return 'no response'
