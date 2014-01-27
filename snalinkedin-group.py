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

# Here set the group id. You can get it from its url: http://www.linkedin.com/groups/FabLab-Interest-Group-89815?gid=89815
groupcode = "89815"

# Get info about the group
request_url = "http://api.linkedin.com/v1/groups/%s:(id,name,site-group-url)?format=json" % (groupcode)
group = client.request(request_url, "GET")

# Convert the value from string to json to dict
a = group[1].rstrip('\n')
content = json.loads(a)
groupname = content["name"]

# Get info about the posts in the group
request_url = 'http://api.linkedin.com/v1/groups/%s/posts:(id,creation-timestamp,title,summary,creator:(first-name,last-name,picture-url,headline),likes,attachment:(image-url,content-domain,content-url,title,summary),relation-to-viewer)?format=json&category=discussion&order=recency&start=0&count=5' % (groupcode)
group = client.request(request_url, "GET")

# Convert the value from string to json to dict
a = group[1].rstrip('\n')
content = json.loads(a)

print content["_total"]

# Debug
#print json.dumps(content["values"], sort_keys=True, indent=4)

# Read likes of each post
if content["_total"] != 0:
	for i in content["values"]:
		print ""
		print i["id"]
		name_author = i["creator"]["firstName"]+" "+i["creator"]["lastName"]
		print "Post by", name_author
		print "Likes..."
		if i["likes"]["_total"] != 0:
			for k in i["likes"]["values"]:
				print "-",k["person"]["firstName"], k["person"]["lastName"]
				name_like = k["person"]["firstName"]+" "+k["person"]["lastName"]
				graph.add_edge(name_like,name_author)
		
		# Read comments of each post
		request_url ="http://api.linkedin.com/v1/posts/%s/comments:(creator:(first-name,last-name,picture-url),creation-timestamp,text)?format=json" % (i["id"])
		# &count=5&start=0 For pagination
		# Convert the value from string to json to dict
		comments = client.request(request_url, "GET")
		b = comments[1].rstrip('\n')
		contentcomments = json.loads(b)
		if contentcomments["_total"] != 0:
			print "Comments..."
			for k in contentcomments["values"]:
				name_comment = k["creator"]["firstName"]+" "+k["creator"]["lastName"]
				print "-",name_comment
				graph.add_edge(name_comment,name_author)
				
				# TODO: an edge with previous commenters
				
				
# Save graph
print ""
print "The group discussion was analyzed succesfully."
print ""
print "Saving the file as "+groupcode+groupname+"-linkedin-group-discussion.gexf..."
#nx.write_gexf(graph, groupcode+groupname+"-linkedin-group-discussion.gexf")