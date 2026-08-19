#!/bin/bash


PID=$1

for i in $(seq 0 1 10); do
ps -o pid,stat,cmd,%cpu,%mem -p $PID >> monitor_estados.txt
sleep 1
done
