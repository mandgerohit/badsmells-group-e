from __future__ import print_function
from itertools import groupby
import urllib2
import json
import re,datetime
import sys
import csv, os
import matplotlib.pyplot as plt
 
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

def plot_graph(week,file_name):
  plt.bar(range(len(week)),week,width=0.50, align='center')
  plt.ylabel('No. of Issues')
  plt.xlabel('Weeks')
  plt.savefig(os.path.splitext(file_name)[0]+'_weekly_issue_distribution'+'.png')
  plt.clf()

print("START FORM FEB 1, 15(1422748800000)=====")

def get_issue_distribution(file_name):
  csvfile = file(file_name,'rb')
  reader = csv.reader(csvfile)
  t = []
  for line in reader:
     [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
     t.append(int(float(create_at)))
  t.sort()
  week = []
  total_week = (t[-1]-t[0])/(7*24*3600)
  end = []
  for i in range(total_week):
     end.append(t[0]+(i+1)*7*24*3600)

  w = 0
  for x in t:
     if  x < end[0]:
        w += 1
  week.append(w)

  for alpha in range(1,total_week):
     w = 0
     for x in t:
        if x >= end[alpha-1] and x < end[alpha]:
            w+= 1
     week.append(w)
  print(week)
  plot_graph(week,file_name)
  csvfile.close()

get_issue_distribution('project1.csv')
get_issue_distribution('project2.csv')
get_issue_distribution('project3.csv')