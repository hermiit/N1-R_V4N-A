# Testing for various roblox apis.

# Modules
import requests as reqs

# Functions
def checkrbx(msg):
    if msg[:10] != '**rbxinfo ':
        return False
    plrid = int(msg[10:])
    newreq = reqs.get(api + 'users/' + str(plrid))
    if newreq.status_code == 200:
        print('Sending info of id %d...' % plrid)
        reqjs = newreq.json()
        print(type(reqjs))
        return reqjs
    else:
        print('error' + str(newreq))
        return False

def getthumb(id):
    thumbapi = 'https://www.roblox.com/headshot-thumbnail/image'
    newthumb = reqs.get(thumbapi,params={'userId': [id],'width': 420,'height': 420,'format': 'png'})
    if newthumb.status_code < 400:
        return newthumb.url
    else:
        return False

def primgrp(id):
    groupapi = 'https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx'
    usrgrp = reqs.get(groupapi,params={'users': id['Username']})
    user = id['Username']
    print(usrgrp)
    if usrgrp.status_code < 400:
        usrjs = usrgrp.json()
        if usrjs == {}:
            print('User %s has no primary group!' % user)
            return 'N/A'
        else:
            return usrjs['Username']['GroupName']
    else:
        return False

# Main
testthumb = getthumb(2)
if testthumb:
    print(testthumb)
    print(primgrp({'Username': 'John Doe'}))
