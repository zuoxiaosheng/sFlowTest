#!/usr/bin/python

import sys
from subprocess import *
import random
import time, sched, threading
import pymongo

mongoIp = '202.120.32.11'
mongoPort = 27017
connection = pymongo.Connection(mongoIp, mongoPort)
db = connection.test
col = sys.argv[1]
data = db[col]
interval = 1

username = 'omni'

usage = []


def perform(s, inc, func, args):
    s.enter(inc,0,perform,(s, inc, func, args))
    func(**args)
   
def schedule(s, inc, func, args):
    s.enter(0,0,perform,(s, inc, func, args))
    s.run()

def getCollectorUsage(ip):
    utc = int(round(time.time()))
    sp = Popen(["Collector/collectorUsage.py", "python", "sflowtool"], stdout=PIPE)
    for line in  sp.stdout:
	    proc = line.rstrip('\n').split()
	    data.insert({'utc':utc, 'ip':ip, 'process':proc[0], 'pCount':proc[1], 'pCpu1':int(proc[2]), 'pCpu2':int(proc[3]), 'pMem':int(proc[4])})


if __name__ == "__main__":
    thread_pool = []

    scheduler = sched.scheduler(time.time,time.sleep)
    args = {'ip':'172.16.60.26'}
    th = threading.Thread(target=schedule, args=(scheduler, interval, getCollectorUsage, args))
    thread_pool.append(th)

    for i in range(len(thread_pool)):
	thread_pool[i].start()

