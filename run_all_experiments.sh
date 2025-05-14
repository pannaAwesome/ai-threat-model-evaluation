#!/bin/bash

applications=("message_queue_app" "iot" "web_app")
tools=("stridegpt" "iriusrisk" "threatcanvas")

light_models=("llama3.2:3b-instruct-q2_K" "phi:2.7b-chat-v2-q3_K_S" "qwen3:1.7b-q4_K_M" "gemma3:4b-it-q4_K_M" "mistral:7b-instruct-q2_K")
heavy_models=("mistral:7b-instruct-v0.3-q4_K_M" "llama3:8b-instruct-q4_K_M" "phi3:3.8b-mini-128k-instruct-q4_K_M" "qwen3:8b-q4_K_M" "gemma3:4b-it-q4_K_M")

# Set number of iterations for judging
# if [ -z "$1" ]; then
#     echo "Usage: $0 <int> <light|heavy>"
#   exit 1
# fi

# if ! [[ "$1" =~ ^[0-9]+$ ]]; then
#   echo "First argument must be a valid number."
#   exit 1
# fi

# iterations=$1
# echo "[INFO] The judges will perform $iterations iterations"


# # Select and pull the chosen models ("light" or "heavy")
# echo "[INFO] You chose to use $1 models"
# if [[ "$2" == "light" ]]; then
#     models=("${light_models[@]}") 
# elif [[ "$2" == "heavy" ]]; then
#     models=("${heavy_models[@]}")
# else
#     echo "Usage: $0 <int> <light|heavy>"
#     exit 1
# fi

for app in "${applications[@]}"; do
    python ./extract_threat_models.py --application $app
    # for tool in "${tools[@]}"; do
    #     TIMEOUT_MIN=30
    #     TIMEOUT_SEC=$((TIMEOUT_MIN * 60))

    #     if timeout "$TIMEOUT_SEC" ./ollama/pull_models.sh $models; then
    #         echo "[INFO] Finished pulling models for ollama"
    #     else
    #         status=$?
    #         if [ "$status" -eq 124 ]; then
    #             echo "[ERROR] Pulling models for ollama timed out"
    #         fi
    #     fi
    #     for model in "${models[@]}"; do
    #         > answer_errors.txt
    #         echo "[INFO] Running: App=$app, Tool=$tool, Model=$model"
    #         python ./judge_threat_models.py -a $app -t $tool -ai $model -i $iterations
    #         mv ./answer_errors.txt ./results/$app/$model/
    #     done
    # done
done
