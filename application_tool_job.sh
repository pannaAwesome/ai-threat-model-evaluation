#!/bin/bash
#SBATCH --job-name=ollama_tool_job
#SBATCH --output=ollama_output_%x_%j.txt
#SBATCH --error=ollama_error_%x_%j.txt
#SBATCH --cpus-per-task=15
#SBATCH --gpus=1
#SBATCH --mem=24G

# Input parameter: tool name, application name
TOOL_NAME="$1"
APPLICATION="$2"

DEBUG=0
if [ -n "$3" ]; then
    DEBUG=1
fi


# Path to Ollama container
CONTAINER_PATH=/ceph/container/ollama_latest.sif

# Unique model cache directory for this job
export OLLAMA_MODELS="/.ollama/ollama_models_${TOOL_NAME}_${APPLICATION}"

mkdir -p "$OLLAMA_MODELS"

# Set specific ollama server host

$PORT=$((11434 + SLURM_ARRAY_TASK_ID))
export OLLAMA_HOST="http://localhost:$PORT"

# Start Ollama container instance with GPU support
INSTANCE_NAME="ollama-${TOOL_NAME}-${APPLICATION}"
singularity instance start --nv $CONTAINER_PATH "$INSTANCE_NAME"

# Start Ollama server with isolated model path
singularity exec instance://"$INSTANCE_NAME" \
  env OLLAMA_MODELS="$OLLAMA_MODELS" ollama serve > ollama_server.log 2>&1 &

# Allow server to initialize
sleep 10

# Pull required models (repeat across tools for now)
MODELS=(
    "mistral:7b-instruct-v0.3-q4_K_M"
    "llama3:8b-instruct-q4_K_M"
    "phi3:3.8b-mini-128k-instruct-q4_K_M"
    "qwen3:8b-q4_K_M"
    "gemma3:4b-it-q4_K_M"
)

MAX_RETRIES=3

for model in "${MODELS[@]}"; do
    retries=0
    until singularity exec instance://"$INSTANCE_NAME" env OLLAMA_MODELS="$OLLAMA_MODELS" ollama pull "$model"; do
        ((retries++))
        if [ $retries -ge $MAX_RETRIES ]; then
            echo "Failed to pull model: $model after $MAX_RETRIES attempts."
            exit 1
        fi
        echo "Retrying pull for $model (attempt $retries)..."
        sleep 10
    done
    sleep 20
done

# Activate Python virtual environment
source ./threat_env/bin/activate

# Set up OpenAI-compatible access
export OPENAI_API_ENDPOINT="http://localhost:$POST/v1"
export OPENAI_API_KEY="ollama"

# Run your tool-specific experiment
if [ DEBUG -eq 0]; then
  bash run_one_experiments.sh "$TOOL_NAME" "$APPLICATION" 10
else
  bash test_run_one_experiment.sh "$TOOL_NAME" "$APPLICATION" 1
fi

# Clean up
singularity instance stop "$INSTANCE_NAME"
rm -rf "$OLLAMA_MODELS"
