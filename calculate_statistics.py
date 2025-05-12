import json
import os

import pandas as pd

from results.hallucinations import hallucinations

def load_threat_models(tool_folder:str, human_folder:str, tools:list) -> tuple:
    with open(f"{human_folder}/threat_model.json", "r") as file:
        human_threat_model = json.load(file)
        
    ai_threat_models = {}
    for tool in tools:    
        ai_threat_model_path = f"{tool_folder}/{tool}_model.json"
        with open(ai_threat_model_path, "r") as ai_file:
            ai_threat_model = json.load(ai_file)
        ai_threat_models[tool] = ai_threat_model
        
    return human_threat_model, ai_threat_models

if __name__ == "__main__":
    applications = ["message_queue_app"]
    tools = ["stridegpt", "iriusrisk", "threatcanvas"]
    
    for application in applications:
        print(f"Processing threat models for application: {application}")
        
        tool_folder = f"results/{application}"
        human_folder = f"threat_templates/{application}"
        current_results = os.listdir(tool_folder)

        # Collect assets for the application
        assets_path = f"{human_folder}/assets.json"
        with open(assets_path, "r") as assets_file:
            assets = json.load(assets_file)
        
        # Load threat models
        human_model, ai_models = load_threat_models(tool_folder, human_folder, tools)
        
        hallucinations("results/message_queue_app", "stridegpt", ai_models, )