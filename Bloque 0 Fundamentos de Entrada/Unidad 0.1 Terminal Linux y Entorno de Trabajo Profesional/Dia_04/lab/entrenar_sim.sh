#!/bin/bash
for i in $(seq 1 1 20); do
echo "Epoca $i/20 - loss=$(echo "scale=2; 1/$i" | bc)"
sleep 1
done
echo "Entrenamiento completo"
