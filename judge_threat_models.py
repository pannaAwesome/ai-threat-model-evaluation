import csv
import random
import numpy as np
import json

from dotenv import load_dotenv, find_dotenv

from llm_as_a_judge.vote import vote, vote_hallucinations

random.seed(42)
np.random.seed(42)

# Load environment variables from .env file
env_file = find_dotenv()
load_dotenv(env_file)

def load_threat_models(tool_folder:str, human_folder:str, tools:list) -> tuple:
    """Load the threat models created by the tools from the result folder, and the human threat model
    from the template folder. The threat models are stored in a JSON format and loaded as list of dictionaries.

    Args:
        tool_folder (str): path to the tool's threat model
        human_folder (str): path to the template threat model
        tools (list): list of tools to load the threat models for

    Returns:
        tuple: human threat model, ai threat models dictionary
    """
    with open(f"{human_folder}/threat_model.json", "r") as file:
        human_threat_model = json.load(file)
        
    ai_threat_models = {}
    for tool in tools:    
        ai_threat_model_path = f"{tool_folder}/{tool}_model.json"
        with open(ai_threat_model_path, "r") as ai_file:
            ai_threat_model = json.load(ai_file)
        ai_threat_models[tool] = ai_threat_model
        
    return human_threat_model, ai_threat_models

def save_results(result_folder, results, prefix=""):
    for metric,result in results.items():
        with open(f"{result_folder}/{prefix}_{metric}.csv", "w", newline='', encoding='utf-8') as csvfile:
            fieldnames = result[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(result)

if __name__ == "__main__":
    
    applications = ["message_queue_app"]
    tools = ["stridegpt", "iriusrisk", "threatcanvas"]
    
    for application in applications:
        print(f"Processing threat models for application: {application}")
        
        tool_folder = f"results/{application}"
        human_folder = f"threat_templates/{application}"

        # Collect assets for the application
        assets_path = f"{human_folder}/assets.json"
        with open(assets_path, "r") as assets_file:
            assets = json.load(assets_file)
        
        # Load threat models
        human_model, ai_models = load_threat_models(tool_folder, human_folder, tools)
        
        for idx in range(2):
            hallucinations = vote_hallucinations(ai_models, assets)
            save_results(tool_folder, hallucinations, idx+1)
        
        vote_results = vote(human_model, ai_models, assets)
        save_results(tool_folder, vote_results)
        
        vote_results_reversed = vote(ai_models, human_model, assets)
        save_results(tool_folder, vote_results, f"reverse")