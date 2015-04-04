#!/usr/bin/env python
import os
import sys
import time
import urllib
import urllib2
import xml.dom.minidom as XML

def sendLoginRequest(username, password):
    url = 'http://172.50.1.1:8090/login.xml'
    post_data = 'mode=191' + '&username=' + username + '&password=' + password
    try:
        req = urllib2.Request(url, post_data)
        response = urllib2.urlopen(req)
        print 'Logged In'
        #xml_dom = XML.parseString(response.read())
        #document = xml_dom.documentElement
        #response = document.getElementsByTagName('message')[0].childNodes[0].nodeValue
        #if 'successfully' in response:
        return True
    except:
        return False

def sendLogoutRequest(username):
    url = 'http://172.50.1.1:8090/logout.xml'
    post_data = 'mode=193' + '&username=' + username
    req = urllib2.Request(url, post_data)
    response = urllib2.urlopen(req)
    print 'Logged out.'

def checkLiveStatus(username):
    url = 'http://172.50.1.1:8090/live?mode=192'
    url = url + '&username=' + username
    response = urllib2.urlopen(url).read()
    xml_dom = XML.parseString(response)
    document = xml_dom.documentElement
    status = document.getElementsByTagName('ack')[0].childNodes[0].nodeValue
    if status == 'ack':
        return True
    else:
        return False

def init(username, password):
    try:
        while True:
            if not checkLiveStatus(username):
                sendLoginRequest(username, password)
            time.sleep(5)
    except KeyboardInterrupt:
            sendLogoutRequest(username)
            os.system('netsh wlan stop hostednetwork')

if __name__ == '__main__':
    cmd = sys.argv[1]
    #os.system('netsh wlan start hostednetwork')
    if cmd == 'login':
        init(sys.argv[2], sys.argv[3])
    elif cmd == 'logout':
        sendLogoutRequest(sys.argv[2])
    elif cmd == 'status':
        print checkLiveStatus(sys.argv[2])
