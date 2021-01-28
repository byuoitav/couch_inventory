#!/usr/bin/env python
import json
import socket
import re
from collections import defaultdict
import os 

lists = []
CP = []
SP = []
STB = []
MSD = []
DS = []
TC = []
production = []
stage = []
no_designation = []
buildings = defaultdict(list)

def device_Designation(str):
    hostname = str
    print(hostname)
    host_name_split=hostname.split("-")
    building_name = host_name_split[0]
    room_number = host_name_split[1]
    room = host_name_split[0] + '-' + host_name_split[1]
    if buildings[building_name]:
        buildings[building_name].append(hostname) 
    else:
        buildings[building_name] = [hostname]

    try:
        room_response = urlopen(couch_url+'/rooms/'+room)
        rr=room_response.read()
        rr_json = json.loads(rr)
        desig = rr_json['designation']
    except urllib.error.HTTPError:
        print("Cannot Get designation")
        desig = 'no_designation'
    
    if desig=='production':
        print(desig)
        production.append(hostname)
    elif desig=='stage':
        stage.append(hostname)
        print(desig)
    else:
        no_designation.append(hostname)
        print(desig)

# Get hostname and parse it for the building, room name, and room number
try:
  from urllib.request import urlopen
  import urllib.error
except ImportError:
  from urllib2 import urlopen
# Pull from couchdb the room designation
couch_url = os.environ['COUCH_ADDR']
response = urlopen(couch_url + '/devices/_all_docs')
resp = response.read()
resp_json = json.loads(resp)
test = json.dumps(resp_json, indent=2)
for row in resp_json["rows"]:
    lists.append(row['id'])

for l in lists:
    if re.search(r'-CP[0-9]+\b', l):
        CP.append(l)
        device_Designation(l)
    elif re.search(r'-SP[0-9]+\b', l):
        SP.append(l)
        device_Designation(l)
    elif re.search(r'-STB[0-9]+\b', l):
        STB.append(l)
        device_Designation(l)
    elif re.search(r'-MSD[0-9]+\b', l):
        MSD.append(l)
        device_Designation(l)
    elif re.search(r'-DS[0-9]+\b', l):
        DS.append(l)
        device_Designation(l)
    elif re.search(r'-TC[0-9]+\b', l):
        TC.append(l)
        device_Designation(l)

d = {"all": [{"Control Processors":CP},{"Scheduling Panels":SP},{"Set-top Boxes":STB},{"Portable Set-top Boxes":MSD},{"Divider Sensors":DS},{"Time Clocks":TC},{"Production":production},{"Stage":stage},{"No Designation":no_designation},{"Buildings":buildings}]}
with open('couch_inventory.txt', 'w') as outfile:
    json.dump(d, outfile)
print("File has been dropped in the local directory at couch_inventory.txt")
#print( json.dumps(d, indent=4))
