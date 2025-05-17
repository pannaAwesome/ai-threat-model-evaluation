from stats.compare_human_ai import *

import os
import glob
import json
import shutil

def get_threat_files(folder_path, tool):
    """
    Returns a list of file paths in `folder_path` matching the pattern *{tool}_threats.csv
    """
    pattern = os.path.join(folder_path, f"*{tool}_threats.csv")
    matching_files = glob.glob(pattern)
    return matching_files

def get_hallucination_files(folder_path, tool):
    """
    Returns a list of file paths in `folder_path` matching the pattern *{tool}_hallucinations.csv
    """
    pattern = os.path.join(folder_path, f"*{tool}_hallucinations.csv")
    matching_files = glob.glob(pattern)
    return matching_files

def reset_stats_folder(folder_path):
    # Delete the folder if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Recreate the folder
    os.makedirs(folder_path)

application = "message_queue_app"
tool = "stridegpt"
actual_threats = 13
tool_threats = 17
stats_folder = f"stats/{tool}"
reset_stats_folder(stats_folder)

threat_files = get_threat_files(f"results/{application}", tool)
hallucination_files = get_hallucination_files(f"results/{application}", tool)

hallucinations = []
for file in hallucination_files:
    kappa = hallucinations_compare_human_ai("human_evaluation/iriusrisk/hallucinations.csv", file, actual_threats*tool_threats)
    hallucinations.append(kappa)

with open(f"{stats_folder}/human_ai_hallucinations.json", "w") as f:
    json.dump(hallucinations, f, indent=4)

threats = []
for file in threat_files:
    kappa = threat_compare_human_ai("human_evaluation/iriusrisk/threats.csv", "results/message_queue_app/gemma3_stridegpt_threats.csv", 57*13)
    threats.append(kappa)

with open(f"{stats_folder}/human_ai_threats.json", "w") as f:
    json.dump(threats, f, indent=4)