#!/bin/bash
for i in $(seq 1 100); do
echo "registro $i" >> salida_datos.txt
sleep 0.1
done
