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

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def std_dev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def get_standard_deviation(file_name):
  csvfile = file(file_name,'rb')
  reader = csv.reader(csvfile)
  t = []
  for line in reader:
     [a,b,c] = line
     t.append(int(float(b)))
  t.sort()
  week = []
  total_week = (t[-1]-t[0])/(7*24*3600)
  end = []
  for i in range(total_week):
     end.append(t[0]+(i+1)*7*24*3600)

  c = 0
  for x in t:
     if  x < end[0]:
        c += 1
  week.append(c)

  for alpha in range(1,total_week):
     c = 0
     for x in t:
        if x >= end[alpha-1] and x < end[alpha]:
            c+= 1
     week.append(c)
  print(std_dev(week)/len(t))
  #plot_graph(week,file_name)
  #plt.show()
  csvfile.close()

get_standard_deviation('project1.csv')
get_standard_deviation('project2.csv')
get_standard_deviation('project3.csv')




