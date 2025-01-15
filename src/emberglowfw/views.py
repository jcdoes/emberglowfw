from __future__ import unicode_literals

import re

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from . tables import rule_table

from .forms import source_destination_dropdowns
from .db import redisdb
from .ruledb import rulecompile


class firewall_ports_data(View):

    def get(self, request):

        # Get what term we have in the search box.
        term = request.GET['term']

        redis_client = redisdb.open_redis_con()

        # Search in Redis
        redis_prefix = "Cisco_Ports*"

        results = []
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor=cursor, match=redis_prefix, count=1000)

            for key in keys:
                decoded_key = key.decode("utf-8")
                value = redis_client.json().get(decoded_key)  # Fetch the value for each key

                if value:
                    decoded_value = value.get("type")
                    group_sub_members = ""

                    if re.search("icmp", decoded_value):
                        decoded_value = value["icmpv4Type"]

                    if None != value.get('objects'):

                        for group in value['objects']:
                            group_sub_members += group['name'] + ", "

                        decoded_value = group_sub_members

                    # Filter based on the search term
                    if term.lower() in decoded_key.lower() or term.lower() in decoded_value.lower():
                        results.append({"id": decoded_key, "text": decoded_key + " - " + decoded_value})

            if cursor == 0:
                break

        return JsonResponse({"results": results})

class firewall_objs_data(View):
    def get(self, request):

        # Get what term we have in the search box.
        term = request.GET['term']

        redis_client = redisdb.open_redis_con()
        
        # Search in Redis
        redis_prefix = "Cisco_Obj*"

        results = []
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor=cursor, match=redis_prefix, count=1000)

            for key in keys:
                decoded_key = key.decode("utf-8")
                value = redis_client.json().get(decoded_key)  # Fetch the value for each key
                
                if value:
                    decoded_value = value.get("value")
                    group_sub_members = ""

                    # This if for groups that don't have the values field.
                    if None == decoded_value:

                        for group in value['objects']:
                            group_sub_members += group['name'] + ", "
                        
                        decoded_value = group_sub_members

                    # Filter based on the search term
                    if term.lower() in decoded_key.lower() or term.lower() in decoded_value.lower():
                        results.append({"id": decoded_key, "text": decoded_key + " - " + decoded_value})
            
            if cursor == 0:
                break

        return JsonResponse({"results": results})

def request_start(request):
    
    if request.method == 'POST':
        form = source_destination_dropdowns(request.POST)
        if form.is_valid():
            rulecompile.create_rule_request(form.cleaned_data['Source'], form.cleaned_data['Destination'], form.cleaned_data['Port'])
            print(form.cleaned_data['Source'])
            print(form.cleaned_data['Destination'])
            print(form.cleaned_data['Port'])
    else: 
        form = source_destination_dropdowns()
    return render(request, "rule_request.html", {"form": form})

def view_rules(request):

    redis_client = redisdb.open_redis_con()

    # Search in Redis
    redis_prefix = "Rule_*"

    results = []
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match=redis_prefix)

        for key in keys:
            decoded_key = key.decode("utf-8")

            value = redis_client.json().get(decoded_key)  # Fetch the value for each key

            name = str(value.get('name'))
            if str(value.get('name')) == '':
                name = "To_Be_Entered"

            results.append({
                "Name": name,
                "Source": str(value.get('source')),
                "Destination": str(value.get('dest')),
                "Port": str(value.get('port')),
                "Reviewed": str(value.get('reviewed')),
                "Reviewed_by": str(value.get('reviewed_by')),
                "Approved": str(value.get('approved'))
            })

        if cursor == 0:
            break

    table = rule_table(results)

    # print(apps.loaded_plugins)
    #  if request.method == 'POST':a
    #       form = ClassificationForm(request.POST)
    #       subnet = "No subnet found, please check your selections or make sure we have a CASE zone built for your selected operating system, environment, access level, region and/or datacenter (If in America). Please contact network security for any questions."
    #       vlan = "n/a"

    #       if form.is_valid():
    #            print("Form is valid!")
    #            if (form.cleaned_data['yesNo_auth']):
    #                 return render(request, 'project.html', {'slug': 'authentication'})
    #            else:
    #                 foundZone = calculateZone(form.cleaned_data)
    #                 for subnetItem in foundZone.items():
    #                      if (subnetItem[0] == 'subnet'):
    #                           subnet = subnetItem[1]
    #                      if (subnetItem[0] == 'vlan'):
    #                           vlan = subnetItem[1]

    #                 return render(request, 'results.html', {'subnets': subnet, 'vlan': vlan})
    #       else:
    #            print("Form is not valid!")
    #            return render(request, 'options2.html', {'form': form})
    #  else:
    #       form = ClassificationForm()
    return render(request, 'rule_view.html', {'table': table})
