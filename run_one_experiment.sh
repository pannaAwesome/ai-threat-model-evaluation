#!/bin/bash

tool=$1
application=$2

models=("mistral:7b-instruct-v0.3-q4_K_M" "llama3:8b-instruct-q4_K_M" "phi3:3.8b-mini-128k-instruct-q4_K_M" "qwen3:8b-q4_K_M" "gemma3:4b-it-q4_K_M")

Set number of iterations for judging
if [ -z "$1" ]; then
    echo "Usage: $0 <int> <light|heavy>"
  exit 1
fi

if ! [[ "$1" =~ ^[0-9]+$ ]]; then
  echo "Third argument must be a valid number."
  exit 1
fi

iterations=$3
echo "[INFO] The judges will perform $iterations iterations"

python ./extract_threat_models.py --application $application

for model in "${models[@]}"; do
    > answer_errors_${tool}_${application}_${model}.txt
    echo "[INFO] Running: App=$application, Tool=$tool, Model=$model"
    python ./judge_threat_models.py -a $application -t $tool -ai $model -i $iterations
    mv ./answer_errors_${tool}_${application}_${model}.txt ./results/$application/$model/
done
