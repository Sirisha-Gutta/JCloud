import base64
import os
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
import requests
import hashlib
import urllib.request
import platform
import time
import json

host = "127.0.0.1"
port = "8088"
url = "http://"+host+":"+port

os.environ['PORT'] = port
print("Checking if the site is available on the specified PORT....")
if (os.environ.get('PORT')==port):
    print("Set to the correct port: ",port)
try:
    page_response = urllib.request.urlopen("{0}/stats".format(url)).getcode()
    print("Connected to the specified PORT {0}".format(page_response))
except:
    print("Connecting to the application ... ")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    my_file = Path.cwd() / "App/broken-hashserve_win.exe"
    subprocess.Popen(my_file)
    
print('==================================================================')
print("Checking if SHA512 hashed out password matches to the request")
hash_object = hashlib.sha512('angrymonkey'.encode())
hex_dig = base64.b64encode(hash_object.digest()).decode()
print("SHA-512: ", hex_dig)

headers = {'Content-Type': 'application/json', }
data = '{"password":"angrymonkey"}'
start_time = time.time()
response = requests.post(url+'/hash', headers=headers, data=data)
total_time = time.time() - start_time

if (total_time > 1):
    print('Job identifier took {0} seconds to return results'.format(total_time))
else:
    print('Job identifier returned immediately')

identifier = response.text
print("job identifier: ", identifier)

password_response = requests.get(url+'/hash/' + identifier)

print("POST hash request: ", password_response.text)

if hex_dig == password_response.text:
    print('SHA512 base64 hash matches the corresponding POST request')
else:
    print('SHA512 base64 hash does not match the corresponding POST request')

print('==================================================================')


def multiple_requests():
    texts = ['password', 'test', 'MYBIRTHDAY', 'hungryjack', '01/01/1970']
    for i in texts:
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{"password": "' + i + '"}'

        response = requests.post(url+'/hash', headers=headers, data=data)
        identifier = response.text
        passresponse = requests.get(url+'/hash/' + identifier)
        print(i, " ", identifier, " ", passresponse.text)


print("Test multiple requests before shutdown")

def post_url(args):
    return requests.post(args[0], data=args[1])


form_data = '{"password":"multipleconnections"}'

list_of_urls = [(url+'/hash', form_data)] * 10

with ThreadPoolExecutor(max_workers=10) as pool:
    response_list = list(pool.map(post_url, list_of_urls))

status = True
for res in response_list:
    if res.status_code >= 300 or res.status_code < 200:
        status = False
        break

if not status:
    print('simultaneous post not successful')
else:
    print('simultaneous post successful')

print('==================================================================')
stats_response = requests.get(url+'/stats')
if json.loads(stats_response.text):
    print('Response is in JSON format',stats_response.text)
else:
    print('Response is not in JSON format instead is ',stats_response.text)

stats_data_response = requests.get(url+'/stats/?newkey=datavalue')
if stats_data_response.status_code >=400:
    print('stats request does not accept parameters')
else:
    print('stats request accepts parameters ',stats_response.text)
print('==================================================================')
print('Shutdown in process...')
data = 'shutdown'
shutConnect = requests.post(url+'/hash', data=data)
assert shutConnect.status_code == 200
print(shutConnect.status_code)

try:
    multiple_requests()
except requests.exceptions.ConnectionError as e:
    print("Requests rejected as there is no Connection")
