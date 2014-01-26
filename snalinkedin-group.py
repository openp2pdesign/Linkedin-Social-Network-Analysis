# -*- encoding: utf-8 -*-
#
# Social Network Analysis of a Linkedin group
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# install oauth2 by downloading the package and launching python setup.py install
# From here: https://github.com/PrincessPolymath/python-oauth2
#
# Group API here: http://developer.linkedin.com/documents/groups-api
#

import oauth2 as oauth
import urlparse 
import networkx as nx
import json
import os

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

graph=nx.DiGraph()

# Get them from https://www.linkedin.com/secure/developer
OAUTH_TOKEN = "Insert here"
OAUTH_SECRET = "Insert here"
CONSUMER_KEY = "Insert here"
CONSUMER_SECRET = "Insert here"


# Code from: http://developer.linkedin.com/documents/getting-oauth-token-python
consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
resp, content = client.request(request_token_url, "POST")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
 
request_token = dict(urlparse.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print

authorize_url = 'https://api.linkedin.com/uas/oauth/authorize'
print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print 

# Try with commenting this section
'''
accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')

access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)
 
resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))
 
print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."
print
'''
# Here start my code

# Get info about the FabLab Interest Group group
request_url = 'http://api.linkedin.com/v1/groups/89815:(id,name,site-group-url,posts:(id,summary,creator))?format=json'
group = client.request(request_url, "GET")

#print json.dumps(group, sort_keys=True, indent=4)

# Get info about the FabLab Interest Group group
request_url = 'http://api.linkedin.com/v1/groups/89815/posts:(creation-timestamp,title,summary,creator:(first-name,last-name,picture-url,headline),likes,attachment:(image-url,content-domain,content-url,title,summary),relation-to-viewer)?format=json&category=discussion&order=recency&modified-since=1302727083000&count=5'
group = client.request(request_url, "GET")

#print json.dumps(group, sort_keys=True, indent=4)

# Convert the value from string to json to dict
a = group[1].rstrip('\n')
content = json.loads(a)

print content["_start"]
print content["_total"]
print content["values"]
