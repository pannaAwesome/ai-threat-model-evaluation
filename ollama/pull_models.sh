#!/bin/bash

ollama list | tail -n +2 | awk '{print $1}' | xargs -n1 ollama rm

ollama list

models=$1

# Loop through each name
for model in "${models[@]}"; do
    echo "Pulling model: $model"
    ollama pull "$model"
    sleep 120
done

