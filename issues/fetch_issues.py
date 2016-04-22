#  gitabel
#  the world's smallest project management tool
#  reports relabelling times in github (time in seconds since epoch)
#  thanks to dr parnin
#  todo:
#    - ensure events sorted by time
#    - add issue id
#    - add person handle

"""
You will need to add your authorization token in the code.
Here is how you do it.

1) In terminal run the following command

curl -i -u <your_username> -d '{"scopes": ["repo", "user"], "note": "OpenSciences"}' https://api.github.com/authorizations

2) Enter ur password on prompt. You will get a JSON response. 
In that response there will be a key called "token" . 
Copy the value for that key and paste it on line marked "token" in the attached source code. 

3) Run the python file. 

     python gitable.py

"""
 
from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
import csv
 
class L():
  "Anonymous container"
  def __init__(i,**fields) : 
    i.override(fields)
  def override(i,d): i.__dict__.update(d); return i
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
                     for k in i.show()])+ '}'
  def show(i):
    lst = [str(k)+" : "+str(v) for k,v in i.__dict__.iteritems() if v != None]
    return ',\t'.join(map(str,lst))

  
def secs(d0):
  d     = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = d - epoch
  return delta.total_seconds()
 


def dump1(u, csvwriter):
  f = open("../token.info","r")
  token = f.readline().strip('\n')
  f.close()
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for event in w:
    number    = event['number']
    state     = event['state']
    creator   = event['user']['login']
    create_at = secs(event['created_at'])
    labels = []
    for la in event['labels']:
       labels.append(la['name'].encode("ascii"))
    if event['milestone'] :
         milestonedue = secs(event['milestone']['due_on'])
    else:
         milestonedue = -1
    last_update=secs(event['updated_at'])
    if state == 'closed':
         closed_at = secs(event['closed_at'])
    else:
         closed_at = -1
    csvwriter.writerows([[number,state,creator,create_at,labels,milestonedue,last_update]])
  return True

def dump(u,csvwriter):
  try:
    return dump1(u, csvwriter)
  except Exception as e: 
    print(e)
    print("Contact TA")
    return False

def launchDump(pro_name,csvwriter):
   page = 1
   while(True):
       print(page)
       doNext = dump('https://api.github.com/repos/' + pro_name + '/issues?state=all&page=' + str(page), csvwriter)
       page += 1
       if not doNext : break

    
pf = open("../projects.info","r")

b = open('project1.csv','wb')
b.truncate()
a = csv.writer(b)
launchDump(pf.readline().strip('\n'),a)
print("===============END OF THE PROJECT1========================")
b.close()

b = open('project2.csv','wb')
b.truncate()
a = csv.writer(b)
launchDump(pf.readline().strip('\n'),a)
print("===============END OF THE PROJECT2========================")
b.close()

b = open('project3.csv','wb')
b.truncate()
a = csv.writer(b)
launchDump(pf.readline().strip('\n'),a)
print("===============END OF THE PROJECT3========================")
b.close()
   

pf.close()
 

