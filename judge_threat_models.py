import csv
import random
import json
import os

import numpy as np

from dotenv import load_dotenv, find_dotenv
from time import time

from llm_as_a_judge.vote import vote, vote_hallucinations

random.seed(42)
np.random.seed(42)

# Load environment variables from .env file
env_file = find_dotenv()
load_dotenv(env_file)

def load_threat_models(result_folder:str, human_folder:str, tools:list) -> tuple:
    with open(f"{human_folder}/threat_model.json", "r") as file:
        human_threat_model = json.load(file)
        
    ai_threat_models = {}
    for tool in tools:    
        ai_threat_model_path = f"{result_folder}/{tool}_model.json"
        with open(ai_threat_model_path, "r") as ai_file:
            ai_threat_model = json.load(ai_file)
        ai_threat_models[tool] = ai_threat_model
        
    return human_threat_model, ai_threat_models

def get_last_run_id(csv_file):
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file))
            last_row = reader[-1] if reader else None
        return int(last_row[0])
    return 0

def append_hallucination_results(results, ai, id, seed, csv_file):
    # Check if file exists to decide whether to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["result_id", "model", "seed", "categories_id", "categories", "assets_id", "assets"])

        if not file_exists:
            writer.writeheader()

        for idx in range(len(results)):
            writer.writerow({
                "result_id": id,
                "model": ai,
                "seed": seed,
                "categories_id": results[idx]["categories_id"],
                "categories": results[idx]["categories"],
                "assets_id": results[idx]["assets_id"],
                "assets": results[idx]["assets"]
            })

def append_threat_results(results, ai, id, reversed_val, csv_file):
    # Check if file exists to decide whether to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["result_id", "model", "reversed", "threats", "mitigations", "risks_same", "risks_more", "risks_less"])

        if not file_exists:
            writer.writeheader()

        for idx in range(len(results["threats"])):
            writer.writerow({
                "result_id": id,
                "model": ai,
                "reversed": reversed_val,
                "threats": results["threats"][idx],
                "mitigations": results["mitigations"][idx],
                "risks_same": results["risks"][idx]["same"],
                "risks_more": results["risks"][idx]["more"],
                "risks_less": results["risks"][idx]["less"],
            })
            
def result_time(seconds):
    time_pretty = ""
    if seconds > 3600:
        time_pretty += f"{seconds // 3600} hours "
        seconds = seconds % 3600
    if seconds > 60:
        time_pretty += f"{seconds // 60} min "
        seconds = seconds % 60
    time_pretty += f"{seconds} sec"
    return time_pretty

if __name__ == "__main__":
    
    applications = ["message_queue_app"]
    tools = ["stridegpt"]#, "iriusrisk", "threatcanvas"]
    ais = [
        "gemma:2b",
        "mistral:7b-instruct-v0.2-q4_K_M",
        "llama2:7b-chat-q4_K_M",
        "gemma3:4b-it-qat",
        "phi3:3.8b-mini-128k-instruct-q4_K_M",
        "qwen3:4b-q4_K_M"
    ]
    iterations = 10
    
    random.seed(21)
    seeds = [random.randint(1, 1000) for _ in range(iterations)]
    
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
        
        for tool in tools:
            print(f"Judging threat model for {tool}")
            ai_model = ai_models[tool]
            
            for ai in ais:
                result_folder = f"{tool_folder}/{ai}"
                if not os.path.exists(f"{result_folder}"):
                    os.makedirs(f"{result_folder}")
                    last_id = 0
                else:
                    last_id = get_last_run_id(f"{result_folder}/{tool}_hallucinations.csv")
                
                start_time = time()
                for idx in range(last_id, iterations):
                    hallucinations = vote_hallucinations(ai, ai_model, assets, seeds[idx])
                    # print("Hallucinations finished")
                    # vote_results = vote(ai, human_model, ai_model, assets)
                    # print("Threats finished")
                    # vote_results_reversed = vote(ai, ai_model, human_model, assets, True)
                    # print("Reverse threats finished")
                    
                    append_hallucination_results(hallucinations, ai, idx, seeds[idx], f"{result_folder}/{tool}_hallucinations.csv")
                    # append_threat_results(vote_results, ai, idx, False, f"{result_folder}/{tool}_threats.csv")
                    # append_threat_results(vote_results_reversed, ai, idx, True, f"{result_folder}/{tool}_reverse_threats.csv")
                    
                    pretty_time = result_time(time() - start_time)
                    print(f"Finished iteration {idx} out of {iterations}, it took {pretty_time}")
            