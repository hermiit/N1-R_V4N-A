# Testing for various roblox apis.

# Modules
import requests as reqs

# Functions
def checkrbx(msg):
    presapi = 'https://www.roblox.com/presence/user'
    usrapi  = 'https://api.roblox.com/users/'
    if msg[:10] != '**rbxinfo ':
        return False

    plrid = int(msg[10:])
    usrreq = reqs.get(usrapi + str(plrid))
    presreq = reqs.get(presapi,params={'userId': plrid})

    if usrreq.status_code == 200 and presreq.status_code == 200:
        print('Sending info of id %d...' % plrid)
        reqjs = usrreq.json()
        reqjs['Last Seen On'] = presreq
        print(type(reqjs))
        return reqjs
    else:
        print('error' + str(newreq))
        return False

# getting the user's presence: https://presence.roblox.com/docs#!/Presence/post_v1_presence_users
# request example: params={'userId': plrid}

# api for username and id: https://api.roblox.com/docs/#Users/
# request example: https://api.roblox.com/users/{userid}

# api for a user's thumbnail: https://www.roblox.com/headshot-thumbnail/image
# request example: params={'userId': [array of ids],'width': 420,'height': 420,'format': 'png'} returns: url(string)

# api for a user's primary group: https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx
# request example: https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx

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
