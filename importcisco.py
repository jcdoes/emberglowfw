#!/usr/bin/python3
import requests
import json
import re
import redis
import urllib3  


urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
token = ""
domain_uuid = ""
ip = "10.23.1.103"    
pw_hash = ""

def getToken():

    url = "https://10.23.1.103/api/fdm/latest/fdm/token"

    payload = {
        "grant_type": "password",
        "username": "admin",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers, verify=False)

    return json.loads(response.text)['access_token']
    
def queryAPI(url, token):

    headers = {
        'Authorization' : 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    return json.loads(response.text)

def getJsonFile(filename):
    f = open(filename, "r")
    return json.loads(f.read()) 

def addPortObject(name, ttype, value, token):

    url = ""
    data = {}

    if re.search("tcp", ttype, re.IGNORECASE):
        url = "https://10.23.1.103/api/fdm/v6/object/tcpports"
        data = {
            "name": name,
            "port": value['value'],
            "type": "tcpportobject"
        }

    if re.search("udp", ttype, re.IGNORECASE):
        url = "https://10.23.1.103/api/fdm/v6/object/udpports"
        data = {
            "name": name,
            "port": value['value'],
            "type": "udpportobject"
        }

    if re.search("icmp", ttype, re.IGNORECASE):
        url = "https://10.23.1.103/api/fdm/v6/object/icmpv4ports"
        data = {
            "name": name,
            "icmpv4Type": value['value'].replace("[", "").replace("]", "").upper(),
            "type": "icmpv4portobject"
        }

    add2 = []

    for item in value:
        add = {'type': "tcpportobject", 'name': item}
        add2.append(add)
    
    if re.search("group", ttype, re.IGNORECASE):
        url = "https://10.23.1.103/api/fdm/v6/object/portgroups"
        data = {
            "name": name,
            "objects": add2,
            "type": "portobjectgroup"
        }

    headers = {
        'Authorization' : 'Bearer ' + token
    }

    response = requests.request("POST", url, json=data, headers=headers, verify=False)
    json_response = json.loads(response.text)

    if json_response.get('error') is not None:
        print("Error: " + str(json_response.get('error')))
    else:
        print("Imported Object!")

def addNetObject(name, type, value, token):

    if re.search("GROUP", type, re.IGNORECASE):
        url = "https://10.23.1.103/api/fdm/v6/object/networkgroups"

        add = {}
        add2 = []

        for item in value:
            add = {'type': "networkobject", 'name': item}
            add2.append(add)
        
        data = {
                "name": name,
                "objects": add2,
                "type": "networkobjectgroup"
            }

    else:
        url = "https://10.23.1.103/api/fdm/v6/object/networks"
        
        data = {
            "name": name,
            "subType": type,
            "value": value,
            "type": "networkobject"
        }

    headers = {
        'Authorization' : 'Bearer ' + token
    }

    response = requests.request("POST", url, json=data, headers=headers, verify=False)
    json_response = json.loads(response.text)

    if json_response.get('error') is not None:
        print("Error: " + str(json_response.get('error')))
    else:
        print("Imported Object!")

def importCiscoObjs():

    token = str(getToken())

    port_group = {}

    for partent in getJsonFile("fwobjects.json").items():
        if partent[0] == 'host_objs':
            for child in partent[1].items():
                # HOST, FQDN, NETWORK, RANGE
                addNetObject(child[0], 'HOST', child[1], token)
        if partent[0] == 'network_objs':
            for child in partent[1].items():
                # HOST, FQDN, NETWORK, RANGE
                addNetObject(child[0], 'NETWORK', child[1], token)
        if partent[0] == 'fqdn_objs':
            for child in partent[1].items():
                # HOST, FQDN, NETWORK, RANGE
                addNetObject(child[0], 'FQDN', child[1], token)
        if partent[0] == 'ports':
            for child in partent[1].items():
                if child[1]['type'] == "GROUP":
                    port_group[child[0]] = child[1]
                else:
                    addPortObject(child[0], child[1]['type'], child[1], token)
        if partent[0] == 'addr_groups':
            for child in partent[1].items():
                addNetObject(child[0], child[1]['type'], child[1]['value'], token)

        for child in port_group.items():
            addPortObject(child[0], child[1]['type'], child[1]['value'], token)

def parseFWObjs(data, ttype):

    objects_dict = {}

    for entry in data:
        entry['plugin'] = "Cisco"
        objects_dict["Cisco_" + ttype + "_" + str(entry['name'])] = entry

    return objects_dict

def removeFWObjs(data):

    objects_to_delete = []

    for objects in data:
        if not re.search("SS_", objects):
            objects_to_delete.append(objects)
            
    for delete in objects_to_delete:
        del data[delete]

    return data

def getCiscoObjs(kind):

    objects_query = {}
    token = str(getToken())

    r = redis.Redis(host='10.23.3.225', port=6379, decode_responses=True, username="default", password="o0WsuLfpl0")

    results_template = {
            "items": []
        }

    dict_to_parse = ""

    object_type = ""

    for template in results_template.items():
        dict_to_parse = template[0]

    ## Add the set of firewall objects
    if kind == "net_objects":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/networks", token)
        object_type = "Obj"

    if kind == "icmp_port_objects":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/icmpv4ports", token)
        object_type = "Ports"

    if kind == "tcp_port_objects":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/tcpports", token)
        object_type = "Ports"

    if kind == "udp_port_objects":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/udpports", token)
        object_type = "Ports"

    if kind == "port_groups":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/portgroups", token)
        object_type = "Ports"

    if kind == "net_groups":
        objects_query = queryAPI("https://10.23.1.103/api/fdm/v6/object/networkgroups", token)
        object_type = "Obj"

    if objects_query['paging'].get('next'):
        paging = objects_query['paging']['next'][0]
    else:
        paging = ""
    
    #Always add first one
    parsed_objects = parseFWObjs(objects_query[dict_to_parse], object_type)
    
    objects_dict = removeFWObjs(parsed_objects)

    if paging != "":

        while True:

            #Call for additional data
            objects_query = queryAPI(paging, token)  

            try:
                paging = objects_query.get('paging', {}).get('next', [])[0]
            except:
                # If we're at the last one, get out of loop
                objects_dict = objects_dict | removeFWObjs(parseFWObjs(objects_query[dict_to_parse], object_type))
                break

            objects_dict = objects_dict | removeFWObjs(parseFWObjs(objects_query[dict_to_parse], object_type))

    # Send the Redis data via our completed dict
    for entry in objects_dict.items():
        print(r.json().set(str(entry[0]), "$", entry[1]))

## Imports from file into Cisco
importCiscoObjs()

getCiscoObjs("net_groups")
getCiscoObjs("net_objects")
getCiscoObjs("tcp_port_objects")
getCiscoObjs("udp_port_objects")
getCiscoObjs("icmp_port_objects")
getCiscoObjs("port_groups")