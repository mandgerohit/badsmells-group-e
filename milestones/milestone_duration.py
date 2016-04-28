from __future__ import print_function
import urllib2
import json
import re,datetime
import sys, os
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
 

print("===========MILESTONE DURATION #===========")

def get_milestone_duration(file_name):
  csvfile = file(file_name,'rb')
  reader = csv.reader(csvfile)
  f.write('\n')
  txt = "=========== # "+ os.path.splitext(file_name)[0] + " MILESTONE DETAILS # ==========="
  txt = str(txt)
  print(txt)
  f.write(txt)
  f.write('\n')
  for line in reader:
      [number,title,createat,due] = line
      days = (long(float(due))-long(float(createat)))/(24*3600)
      print(title+":"+str(int(days)))
      txt = title+":"+str(int(days))
      f.write(txt)
      f.write('\n')
  csvfile.close()

f = open('milestone_summary.txt','w')
f.truncate()

get_milestone_duration('project1.csv')
get_milestone_duration('project2.csv')
get_milestone_duration('project3.csv')

f.close()