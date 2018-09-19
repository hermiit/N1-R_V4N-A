# Modules
import requests as reqs
import json


# Vars
newstr = '**rbxinfo 1000'
api = 'https://api.roblox.com/'
print(newstr[:2])

# Functions
def checkrbx(msg):
    if newstr[:10] != '**rbxinfo ':
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
# Main

rbxreq = checkrbx("**getinfo 2")
if rbxreq:
    print(rbxreq['Username'])
