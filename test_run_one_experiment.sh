#!/bin/bash

tool=$1
application=$2
model=$3

# Set number of iterations for judging
if ! [[ "$4" =~ ^[0-9]+$ ]]; then
  echo "Third argument must be a valid number."
  exit 1
fi

iterations=$4
echo "[INFO] The judges will perform $iterations iterations"

> answer_errors_${tool}_${application}_${model}.txt
echo "[INFO] Running: App=$application, Tool=$tool, Model=$model"
source threat_env/bin/activate && python ./judge_threat_models.py -a $application -t $tool -ai $model -i $iterations
mv ./answer_errors_${tool}_${application}_${model}.txt ./results/$application
