#!/usr/bin/python

import sys
import time
from subprocess import *

cmd = sys.argv[1]

def getCpuUsage(pName):
	cat = Popen(["cat", "/proc/cpuinfo"], stdout=PIPE)
	grep = Popen(["grep", "processor"], stdin=cat.stdout, stdout=PIPE)
	wc = Popen(["wc", "-l"], stdin=grep.stdout, stdout=PIPE)
	cores = int(wc.stdout.readline())

	cat1 = Popen(["cat", "/proc/stat"], stdout=PIPE)
	stat1 = cat1.stdout.readline().rstrip('\n').split()[1:]
	totalCpuTime1 = 0
	for i in range(len(stat1)):
	        totalCpuTime1 += int(stat1[i])
	#print "totalCpuTime1: %d"%totalCpuTime1
	ps = Popen(["ps", "axo", "pid,comm"], stdout=PIPE)
	grep = Popen(["grep", cmd], stdin=ps.stdout, stdout=PIPE)
	processTime1 = 0
	procCount = 0
	for line in grep.stdout:
		procCount += 1
		pid = line.strip(' \n').split()[0]
		cat2 = Popen(["cat", "/proc/%s/stat"%pid], stdout=PIPE)
		stat2 = cat2.stdout.readline().rstrip('\n').split()[13:17]
		for i in range(len(stat2)):
	        	processTime1 += int(stat2[i])
	#print "processTime1: %d"%processTime1
	'''
	time.sleep(1)

	cat1 = Popen(["cat", "/proc/stat"], stdout=PIPE)
	stat1 = cat1.stdout.readline().rstrip('\n').split()[1:]
	totalCpuTime2 = 0
	for i in range(len(stat1)):
	        totalCpuTime2 += int(stat1[i])
	#print "totalCpuTime2: %d"%totalCpuTime2
	ps = Popen(["ps", "axo", "pid,comm"], stdout=PIPE)
	grep = Popen(["grep", cmd], stdin=ps.stdout, stdout=PIPE)
	processTime2 = 0
	procCount = 0
	for line in grep.stdout:
		procCount += 1
	        pid = line.strip(' \n').split()[0]
	        cat2 = Popen(["cat", "/proc/%s/stat"%pid], stdout=PIPE)
	        stat2 = cat2.stdout.readline().rstrip('\n').split()[13:17]
	        for i in range(len(stat2)):
	                processTime2 += int(stat2[i])
	#print "processTime2: %d"%processTime2
	'''
	return (procCount,cores*processTime1,totalCpuTime1)

def getMemUsage(pName):
	ps = Popen(["ps", "axo", "pid,comm,rss"], stdout=PIPE)
	grep = Popen(["grep", pName], stdin=ps.stdout, stdout=PIPE)
	#lines = grep.stdout.readlines()
	memUsage = 0
	for line in grep.stdout:
		memUsage += int(line.rstrip('\n').split()[2])
	return memUsage


if __name__ == '__main__':
	pName = sys.argv[1]
	cpu = getCpuUsage(pName)
	print cpu[0], cpu[1], cpu[2], getMemUsage(pName)

