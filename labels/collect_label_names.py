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
 

print("===========LABEL NAMES#===========")

def get_label_names(file_name):
  csvfile = file(file_name,'rb')
  reader = csv.reader(csvfile)
  f.write('\n')
  txt = "=========== # "+ os.path.splitext(file_name)[0] + " LABELS USED # ==========="
  txt = str(txt)
  print(txt)
  f.write(txt)
  f.write('\n')
  names = []
  for line in reader:
      [name,url,color] = line
      names.append(name)
  names.sort()
  print(names)    
  csvfile.close()

  f.write(str(names))
  f.write('\n')

f = open('label_summary.txt','w')
f.truncate()

get_label_names('project1.csv')
get_label_names('project2.csv')
get_label_names('project3.csv')

f.close()