#!/bin/bash

tool=$1
application=$2
models_str=$3

IFS="," read -ra models <<< "$models_str"

# Set number of iterations for judging
if ! [[ "$4" =~ ^[0-9]+$ ]]; then
  echo "Third argument must be a valid number."
  exit 1
fi

iterations=$4
echo "[INFO] The judges will perform $iterations iterations"

source threat_env/bin/activate && python ./extract_threat_models.py --application $application

for model in "${models[@]}"; do
    > answer_errors_${tool}_${application}_${model}.txt
    echo "[INFO] Running: App=$application, Tool=$tool, Model=$model"
    source threat_env/bin/activate && python ./judge_threat_models.py -a $application -t $tool -ai $model -i $iterations
    mv ./answer_errors_${tool}_${application}_${model}.txt ./results/$application
done
