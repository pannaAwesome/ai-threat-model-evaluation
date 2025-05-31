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

# Path to Ollama files
OLLAMA_MODELS_HOST="$HOME/.singularity/ollama_models_${SLURM_JOB_ID}"
OLLAMA_MODELS="/scratch/singularity/ollama_models_${SLURM_JOB_ID}"
mkdir -p "$OLLAMA_MODELS_HOST"


# Start Ollama container instance with GPU support
INSTANCE_NAME="ollama-${TOOL_NAME}-${APPLICATION}"
singularity instance start --nv -B $HOME/.singularity:/scratch/singularity \
	-B $OLLAMA_MODELS_HOST:$OLLAMA_MODELS \
	 $CONTAINER_PATH "$INSTANCE_NAME"

# Start Ollama server with isolated model path
singularity exec instance://"$INSTANCE_NAME" \
  env OLLAMA_NUM_PARALLEL=15 \
	OLLAMA_MODELS=$OLLAMA_MODELS \
	OLLAMA_MAX_QUEUE=64 \
	 ollama serve > ollama_server.log 2>&1 &

# Allow server to initialize
sleep 10

if ! curl --fail --silent --head http://localhost:11434; then
	echo "Failed to find Ollama API"
	exit 1
fi

singularity exec instance://"$INSTANCE_NAME" ollama --version

# Pull required models (repeat across tools for now)
MODELS=(
    "mistral:7b-instruct-v0.3-q4_K_M"
    "llama3:8b-instruct-q4_K_M"
    "phi3:3.8b-mini-128k-instruct-q4_K_M"
    "qwen:7b-chat"
    "gemma3:4b-it-q4_K_M"
)

MAX_RETRIES=3

for model in "${MODELS[@]}"; do
    retries=0
    until singularity exec instance://"$INSTANCE_NAME" env OLLAMA_MODELS=$OLLAMA_MODELS ollama pull "$model"; do
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

# Set up OpenAI-compatible access
export OPENAI_ENDPOINT="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"

# Run your tool-specific experiment
if [ $DEBUG -eq 0 ]; then
    chmod +x run_one_experiment.sh
    bash run_one_experiment.sh "$TOOL_NAME" "$APPLICATION" 10
else
    bash test_run_one_experiment.sh "$TOOL_NAME" "$APPLICATION" 1
fi

# Clean up
for model in "${MODELS[@]}"; do
    singularity exec instance://"$INSTANCE_NAME" env OLLAMA_MODELS=$OLLAMA_MODELS  ollama rm "$model"
done
singularity instance stop "$INSTANCE_NAME"
rm -rf "$OLLAMA_MODELS"
