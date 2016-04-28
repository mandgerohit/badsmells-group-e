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

def plot_graph(labels,count,file_name):
  plt.bar(range(len(labels)),count,width=0.50, align='center')
  plt.xticks(range(len(labels)), labels)
  plt.ylabel('Labels')
  plt.xlabel('Count')
  locs, labels = plt.xticks()
  plt.setp(labels, rotation=45)
  plt.tick_params(axis='both', which='minor', labelsize=7)
  plt.tick_params(axis='both', which='major', labelsize=7)
  plt.savefig(os.path.splitext(file_name)[0]+'_label_distribution'+'.png')
  plt.clf()

def splits(e):
  result = []
  strs = ''
  for c in e:
     if c != ',' and c != '[' and c != ']' and c != '\'':
	strs += c
     else:
        if len(strs) >0 and strs != ' ':
           result.append(strs)
	strs = ''	
  return result

def get_label_distribution(file_name):
  csvfile = file(file_name,'rb')
  csvfile2 = file(os.path.splitext(file_name)[0] + '_label_distribution.csv','w')
  reader = csv.reader(csvfile)
  writer = csv.writer(csvfile2)
  t = []
  label_set = set([])
  for line in reader:
    [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
    for label in splits(labels):
        label_set.add(label)

  new_labels = []
  label_count = []
  for la in label_set:
     count = 0
     csvfile.seek(0)
     for line in reader:
        [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
        for ll in splits(labels):
             if ll == la:
                 count += 1
     writer.writerows([[la,count]])
     new_labels.append(la)
     label_count.append(count)
  plot_graph(new_labels, label_count, file_name)
  csvfile.close()
  csvfile2.close()

get_label_distribution('project1.csv')
get_label_distribution('project2.csv')
get_label_distribution('project3.csv')