import requests

URL = 'https://api.ipify.org?format=json'

res = requests.get(URL)
#print(res.text)
ip_dict = res.json()

ip = ip_dict['ip']
print(ip)