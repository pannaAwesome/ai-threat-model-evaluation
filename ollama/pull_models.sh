#!/bin/bash

ollama list | tail -n +2 | awk '{print $1}' | xargs -n1 ollama rm

ollama list

models=("llama3.2:3b-instruct-q2_K" "phi:2.7b-chat-v2-q3_K_S" "qwen3:1.7b-q4_K_M" "gemma3:4b-it-q4_K_M" "mistral:7b-instruct-q2_K")

# Loop through each name
for model in "${models[@]}"; do
    echo "Pulling model: $model"
    ollama pull "$model"
    sleep 120
done

