from __future__ import print_function
import urllib2
import json
import re,datetime
import sys, os
import csv
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

def plot_graph(creators,count,file_name):
  plt.bar(range(len(creators)),count,width=0.50, align='center', color = 'rgbymc')
  plt.xticks(range(len(creators)), creators)
  plt.ylabel('Issues created')
  plt.xlabel('Users')
  locs, creators = plt.xticks()
  plt.setp(creators)
  plt.tick_params(axis='both', which='minor', labelsize=6)
  plt.tick_params(axis='both', which='major', labelsize=6)
  plt.savefig(os.path.splitext(file_name)[0]+'_issue_creator_distribution'+'.png')
  plt.clf()

def get_issue_distribution(file_name):
  csvfile = file(file_name,'rb')
  reader = csv.reader(csvfile)
  t = []
  creator_set = set([])
  for line in reader:
     [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
     creator_set.add(creator)

  dis = []
  for mm in creator_set:
     count = 0
     csvfile.seek(0)
     for line in reader:
        [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
        if creator == mm:
          count += 1
     dis.append(count)
  print(list(creator_set))
  print(dis)
  plot_graph(list(creator_set), dis, file_name)
  csvfile.close()

get_issue_distribution('project1.csv')
get_issue_distribution('project2.csv')
get_issue_distribution('project3.csv')
