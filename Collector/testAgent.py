#!/usr/bin/python

import sys
from subprocess import *
import random
import time, sched, threading
import pymongo

mongoIp = '202.120.32.11'
mongoPort = 27017
connection = pymongo.Connection(mongoIp, mongoPort)
db = connection.sflow_test
data = db.agent_graph
interval = 1

nodes = ('172.16.60.2','172.16.60.4','172.16.60.5','172.16.60.6','172.16.60.7','172.16.60.8','172.16.60.9','172.16.60.10','172.16.60.11','172.16.60.15')

username = 'omni'

usage = []


def perform(s, inc, func, args):
    s.enter(inc,0,perform,(s, inc, func, args))
    func(**args)
   
def schedule(s, inc, func, args):
    s.enter(0,0,perform,(s, inc, func, args))
    s.run()

def getAgentUsage(ip, pName):
	utc = int(round(time.time()))
	sp = Popen(["ssh", "%s@%s"%(username,ip), "/home/omni/test.py %s"%pName], stdout=PIPE)
	results =  sp.stdout.readline().rstrip('\n').split()
	data.insert({'utc':utc, 'ip':ip, 'process':pName, 'pCount':int(results[0]), 'pCpu1':int(results[1]), 'pCpu2':int(results[2]), 'pMem':int(results[3])})

if __name__ == "__main__":
	scheduler = sched.scheduler(time.time,time.sleep)
	args = {'ip':'172.16.60.2', 'pName':'sflsp'}
	schedule(scheduler, interval, getAgentUsage, args)
