import _thread
import http.client
import json
import time
import urllib.request
from urllib.parse import urlparse

import babase
import bascenev1
from efro.terminal import Clr
from playersdata import pdata

VERSION = 81

def check():
    _thread.start_new_thread(updateProfilesJson, ())

    bascenev1.apptimer(15, postStatus)


#def updateProfilesJson():
#    profiles = pdata.get_profiles()
#
#    for id in profiles:
#        if "spamCount" not in profiles[id]:
#            profiles[id]["spamCount"] = 0
#            profiles[id]["lastSpam"] = time.time()
#
#    pdata.commit_profiles(profiles)

def updateProfilesJson():
    profiles = pdata.get_profiles() or {}

    for id in profiles:
        if "spamCount" not in profiles[id]:
            profiles[id]["spamCount"] = 0
            profiles[id]["lastSpam"] = time.time()

    pdata.commit_profiles(profiles)

def postStatus():
    link = 'https://bcsservers.ballistica.workers.dev/ping'
    data = {'name': babase.app.classic.server._config.party_name,
            'port': str(bascenev1.get_game_port()),
            'build': babase.app.env.engine_build_number,
            'bcsversion': VERSION}
    _thread.start_new_thread(postRequest, (link, data,))


def postRequest(link, data):
    try:
        url = urlparse(link)
        conn = http.client.HTTPSConnection(url.netloc)
        json_payload = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }
        conn.request("POST", url.path, body=json_payload, headers=headers)
        response = conn.getresponse()
        response_data = response.read()
    except:
        pass


def checkSpammer(data):
    def checkMaster(data):
        try:
            url = urlparse(
                'https://bcsservers.ballistica.workers.dev/checkspammer')
            conn = http.client.HTTPSConnection(url.netloc)
            json_payload = json.dumps(data)
            headers = {
                "Content-Type": "application/json"
            }
            conn.request("POST", url.path, body=json_payload, headers=headers)
            response = conn.getresponse()
            response_data = response.read()
        except:
            pass
        # TODO handle response and kick player based on status

    _thread.start_new_thread(checkMaster, (data,))
    return