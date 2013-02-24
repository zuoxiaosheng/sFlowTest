#!/bin/bash


username=omni
for agent in `cat agents`
do
	scp test.py $username@$agent:/home/$username/
done
