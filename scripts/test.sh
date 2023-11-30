#!/bin/bash
for i in $(ps aux | grep server-1.properties| awk '{print $2}')
do 
	kill $i || continue
done