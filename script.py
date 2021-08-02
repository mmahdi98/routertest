import pandas as pd
import requests, zipfile, io
url = 'https://download.ip2location.com/lite/IP2LOCATION-LITE-DB1.CSV.ZIP'
file_name = 'IP2LOCATION-LITE-DB1.CSV'
ip = '2.177.223.205'
net_mask = '255.255.255.255'
gateway = '2.177.128.1'
interface = 'ppp0'
print('Started...')
r = requests.get(url)
print('IPs Downloaded.')
zipfile.ZipFile(io.BytesIO(r.content)).extract(file_name)
print(file_name + ' File Extracted.')
all_ip = pd.read_csv(file_name)
all_ip.columns = ['first', 'last', 'id', 'country']
del all_ip['country']
iran_ips = all_ip[all_ip.id == 'IR']
iran_ips.to_csv('iran_ips0.csv')
net_masks = []
network_ip = []
lf = iran_ips['first'].tolist()
ll = iran_ips['last'].tolist()
n = len(lf)
for i in range(n):
    s = int(lf[i])
    mask1 = int(ll[i]) - s
    mask = 0
    for j in range(0, 32):
        if mask1 & (2**j) != 0:
            mask += 2**j
        else:
            break
    mask = 2**32 - mask - 1
    a4 = mask%256
    b4 = s%256
    mask //= 256
    s //= 256
    a3 = mask%256
    b3 = s%256
    mask //= 256
    s //= 256
    a2 = mask%256
    b2 = s%256
    mask //= 256
    s //= 256
    a1 = mask
    b1 = s
    network_ip.append(str(b1)+'.'+str(b2)+'.'+str(b3)+'.'+str(b4))
    net_masks.append(str(a1)+'.'+str(a2)+'.'+str(a3)+'.'+str(a4))
iran_ips = pd.DataFrame({'network': network_ip, 'netmask': net_masks})
iran_ips.to_csv('iran_ips.csv')
print('Done!')
#print route -n netwrok[i] netmask netwask[i] dev interface
#print route -n ipofinterface netmask net_mask dev interface 
with open('install.sh', 'w') as install_file:
    install_file.writelines('route add -net {} netmask 255.255.255.255 dev {}\n'.format(ip, interface))
    for i in range(n):
        install_file.writelines('route add -net {} netmask {} gw {} dev {}\n'.format(network_ip[i], net_masks[i], gateway, interface))
with open('uninstall.sh', 'w') as uninstall_file:
    uninstall_file.writelines('route del -net {} netmask 255.255.255.255\n'.format(ip))
    for i in range(n):
        uninstall_file.writelines('route del -net {} netmask {}\n'.format(network_ip[i], net_masks[i]))


