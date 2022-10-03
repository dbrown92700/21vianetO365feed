#!/usr/bin/python3
"""
Copyright (c) 2012 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
__author__ = "David Brown <davibrow@cisco.com>"
__contributors__ = []
__copyright__ = "Copyright (c) 2012 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from vmanage_api import rest_api_lib
from vmanage_credentials import *
import requests, uuid, json

if __name__ == '__main__':

    # Starting JSON definition for application in vManage

    ms21vianet_urls = {
      "appName": "O365-21V-URL",
      "serverNames": []
    }
    ms21vianet_ips = {
      "appName": "O365-21V-IP",
      "L3L4": [
        {
          "ipAddresses": [],
          "ports": "443",
          "l4Protocol": "TCP"
        }
      ]
    }

    # Read Microsoft JSON definition. Add URLs and IP's to appropriate app definition

    my_uuid = str(uuid.uuid4())
    vianet = json.loads(requests.get(f'https://endpoints.office.com/endpoints/China?clientrequestid={my_uuid}').text)
    for net in vianet:
        if 'urls' in net.keys():
            for url in net['urls']:
                if url not in ms21vianet_urls['serverNames']:
                    ms21vianet_urls['serverNames'].append(url)
        else:
            for ip_address in net['ips']:
                if ':' in ip_address:
                    # print(f'IPv6 Address Ignored: {ip_address}')
                    continue
                else:
                    if ip_address not in ms21vianet_ips:
                        ms21vianet_ips['L3L4'][0]['ipAddresses'].append(ip_address)

    # Log into vManage, pull current app list, and either update existing apps or create new ones

    ms21vianet_urls_id = ms21vianet_ips_id = None
    vmanage = rest_api_lib(vmanage_ip, vmanage_user, vmanage_password)
    current_apps = vmanage.get_request('/template/policy/customapp')
    for app in current_apps['data']:
        if app['appName'] == 'O365-21V-IP':
            ms21vianet_ips_id = app['appId']
        if app['appName'] == 'O365-21V-URL':
            ms21vianet_urls_id = app['appId']
    if ms21vianet_urls_id:
        app_id = ms21vianet_urls_id
        vmanage.put_request(f'/template/policy/customapp/{app_id}', ms21vianet_urls)
    else:
        app_id = vmanage.post_request('/template/policy/customapp', ms21vianet_urls)
    print(f'{app_id}:\n{ms21vianet_urls}')
    if ms21vianet_urls_id:
        app_id = ms21vianet_urls_id
        vmanage.put_request(f'/template/policy/customapp/{app_id}', ms21vianet_ips)
    else:
        app_id = vmanage.post_request('/template/policy/customapp', ms21vianet_ips)
    print(f'{app_id}:\n{ms21vianet_ips}')
    vmanage.logout()
# [END gae_python3_app]
