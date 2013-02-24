#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import time
from subprocess import *

procs = []
for i in range(len(sys.argv)-1):
	procs.append(sys.argv[i+1])
proc_str = ''
for i in range(len(procs)):
	proc_str += procs[i]
	if i != len(procs)-1:
		proc_str += '\|'

#获取一个或或多个进程的CPU占用率
def getCpuUsage():

	cpuUsage = {}

	#获取CPU核心数
	cat = Popen(["cat", "/proc/cpuinfo"], stdout=PIPE)
	grep = Popen(["grep", "processor"], stdin=cat.stdout, stdout=PIPE)
	wc = Popen(["wc", "-l"], stdin=grep.stdout, stdout=PIPE)
	cores = int(wc.stdout.readline())

	#获取开始时间的CPU总时间
	cat1 = Popen(["cat", "/proc/stat"], stdout=PIPE)
	stat1 = cat1.stdout.readline().rstrip('\n').split()[1:]
	totalCpuTime1 = 0
	for i in range(len(stat1)):
	        totalCpuTime1 += int(stat1[i])
	#print "totalCpuTime1: %d"%totalCpuTime1

	#获取开始时间的进程CPU时间
	ps = Popen(["ps", "axo", "pid,comm"], stdout=PIPE)
	grep = Popen(["grep", proc_str], stdin=ps.stdout, stdout=PIPE)
	processTime1 = {}
	procCount = {}
	for line in grep.stdout:
		pinfo = line.strip(' \n').split()
		pid = pinfo[0]
		pname = pinfo[1]
		if processTime1.has_key(pname):
			procCount[pname] += 1
		else:
			procCount[pname] = 1
			processTime1[pname] = 0
		cat2 = Popen(["cat", "/proc/%s/stat"%pid], stdout=PIPE)
		stat2 = cat2.stdout.readline().rstrip('\n').split()[13:17]
		for i in range(len(stat2)):
	        	processTime1[pname] += int(stat2[i])
	#print "processTime1: %d"%processTime1

	'''
	#1秒的间隔时间
	time.sleep(1)

	#获取结束时间的CPU总时间
	cat1 = Popen(["cat", "/proc/stat"], stdout=PIPE)
	stat1 = cat1.stdout.readline().rstrip('\n').split()[1:]
	totalCpuTime2 = 0
	for i in range(len(stat1)):
	        totalCpuTime2 += int(stat1[i])
	#print "totalCpuTime2: %d"%totalCpuTime2

	#获取结束时间的进程CPU时间
	ps = Popen(["ps", "axo", "pid,comm"], stdout=PIPE)
	grep = Popen(["grep", proc_str], stdin=ps.stdout, stdout=PIPE)
	processTime2 = {}
        for line in grep.stdout:
	        pinfo = line.strip(' \n').split()
		pid = pinfo[0]
		pname = pinfo[1]
		if not processTime2.has_key(pname):
                        processTime2[pname] = 0
		processTime2[pname] = 0
	        cat2 = Popen(["cat", "/proc/%s/stat"%pid], stdout=PIPE)
	        stat2 = cat2.stdout.readline().rstrip('\n').split()[13:17]
	        for i in range(len(stat2)):
	                processTime2[pname] += int(stat2[i])
	#print "processTime2: %d"%processTime2
	'''
	for proc in processTime1:
		cpuUsage[proc] = (procCount[proc], cores*processTime1[proc], totalCpuTime1)
	return cpuUsage

def getMemUsage():
	ps = Popen(["ps", "axo", "pid,comm,rss"], stdout=PIPE)
	grep = Popen(["grep", proc_str], stdin=ps.stdout, stdout=PIPE)
	memUsage = {}
	for line in grep.stdout:
		pinfo = line.strip(' \n').split()
		pid = pinfo[0]
                pname = pinfo[1]
		pdata = pinfo[2]
		memUsage[pname] = int(pdata)
	return memUsage


if __name__ == '__main__':
	usage = {}
	cpu = getCpuUsage()
	mem = getMemUsage()
	for proc in cpu:
		print proc,cpu[proc][0],cpu[proc][1],cpu[proc][2],mem[proc]
	#print usage

