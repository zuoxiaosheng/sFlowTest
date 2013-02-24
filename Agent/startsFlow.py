#!/usr/bin/python

import sys
import subprocess
import random
import time, sched, threading

agent_count = int(sys.argv[1])
interval = sys.argv[2]
collector = sys.argv[3]

def send(agent, start):
	print 'new process'
	time.sleep(start)
	print 'start process'
	sp = subprocess.Popen(['./sflsp', '-d', 'eth0', '-P', '-s', '-1', '-t', interval, '-A', agent, '-C', collector, '-c', '6343'])


if __name__ == '__main__':
	thread_pool = []
	for i in range(agent_count):
		th = threading.Thread(target=send, args=('1.12.'+str(i/255)+'.'+str(i%255),random.uniform(0, float(interval))))
        	thread_pool.append(th)
	for i in range(len(thread_pool)):
		thread_pool[i].start()
	
