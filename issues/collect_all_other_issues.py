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

def plot_graph(projects,count,desc):
  plt.bar(range(len(projects)),count,width=0.50, align='center', color = 'rgbymc')
  plt.xticks(range(len(projects)), projects)
  plt.ylabel(desc)
  plt.xlabel('Projects')
  locs, projects = plt.xticks()
  plt.setp(projects)
  plt.tick_params(axis='both', which='minor', labelsize=10)
  plt.tick_params(axis='both', which='major', labelsize=10)
  plt.savefig(desc+'.png')
  plt.clf()

def get_all_issues():
  i = 1
  not_closed = []
  not_labelled = []
  not_milestones = []
  not_in_time = []
  not_description = []
  while i <= 3:
  	  file_name = 'project'+str(i)+'.csv'
	  csvfile = file(file_name,'rb')
	  reader = csv.reader(csvfile)
	  f.write('\n')
	  txt = "=========== # "+ os.path.splitext(file_name)[0] + " ISSUES # ==========="
	  txt = str(txt)
	  print(txt)
	  f.write(txt)
	  f.write('\n')
	  t = []
	  labels = set([])
	  count_not_closed = 0
	  count_not_labelled = 0
	  count_not_milestones = 0
	  count_not_in_time = 0
	  count_not_description = 0
	  for line in reader:
	    [number,title,description,state,creator,create_at,labels,milestonedue,last_update] = line
	    if state != 'closed':
	      count_not_closed += 1
	    if labels == '[]':
	      count_not_labelled += 1
	    if milestonedue == '-1':
	      count_not_milestones += 1
	    if description == '':
	      count_not_description += 1
	    if int(float(milestonedue)) > 0 and int(float(last_update)) > int(float(milestonedue)):
	      if state == 'closed':
	        count_not_in_time += 1

	  txt = "ISSUES NOT CLOSED"
	  print(txt)
	  print(count_not_closed)
	  not_closed.append(count_not_closed)
	  f.write(txt + " : "+ str(count_not_closed))
	  f.write('\n')

	  txt = "ISSUES WITHOUT LABELS"
	  print(txt)
	  print(count_not_labelled)
	  not_labelled.append(count_not_labelled)
	  f.write(txt + " : "+ str(count_not_labelled))
	  f.write('\n')

	  txt = "ISSUES WITHOUT MILESTONES"
	  print(txt)
	  print(count_not_milestones)
	  not_milestones.append(count_not_milestones)
	  f.write(txt + " : "+ str(count_not_milestones))
	  f.write('\n')

	  txt = "OVERDUE ISSUES"
	  print(txt)
	  print(count_not_in_time)
	  not_in_time.append(count_not_in_time)
	  f.write(txt + " : "+ str(count_not_in_time))
	  f.write('\n')

	  txt = "ISSUES WITHOUT DESCRIPTION"
	  print(txt)
	  print(count_not_description)
	  not_description.append(count_not_description)
	  f.write(txt + " : "+ str(count_not_description))
	  f.write('\n')
	  
	  csvfile.close()
	  i += 1
  
  projects = ['project1', 'project2', 'project3']

  plot_graph(projects,not_closed,'issues_not_closed')
  plot_graph(projects,not_labelled,'issues_without_labels')
  plot_graph(projects,not_milestones,'issues_without_milestones')
  plot_graph(projects,not_in_time,'issues_overdue')
  plot_graph(projects,not_description,'issues_without_description')

f = open('issue_summary.txt','w')
f.truncate()

get_all_issues()

f.close()
