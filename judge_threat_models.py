import random
import os

import numpy as np

from time import time
from argparse import ArgumentParser
from dotenv import load_dotenv, find_dotenv

from llm_as_a_judge.vote import vote_threats_threaded, vote_hallucinations_threaded
from utils.files import load_assets, load_threat_models, append_threat_results, append_hallucination_results
from utils.run_stats import result_time

random.seed(42)
np.random.seed(42)

# Load environment variables from .env file
env_file = find_dotenv()
load_dotenv(env_file)

def perform_judging(ai, ai_model, tms, tms_reversed, assets, seeds, iterations, prefix_result):
    start_time = time()
    for idx in range(iterations):
        hallucinations = vote_hallucinations_threaded(ai, ai_model, assets, seeds[idx])
        append_hallucination_results(hallucinations, ai, idx, seeds[idx], f"{prefix_result}_hallucinations.csv")                    
        hallucination_time = result_time(time() - start_time)
        print(f"[INFO] Hallucinations saved for {idx+1} out of {iterations} after {hallucination_time}")
        
        vote_results = vote_threats_threaded(tms, assets, ai)
        if vote_results:
            append_threat_results(vote_results, ai, idx, False, f"{prefix_result}_threats.csv")                    
        threat_time = result_time(time() - start_time)
        print(f"[INFO] Threats saved for {idx+1} out of {iterations} after {threat_time}")
        
        #vote_results_reversed = vote_threats_threaded(tms_reversed, assets, ai, True)
        #if vote_results_reversed:
        #    append_threat_results(vote_results_reversed, ai, idx, True, f"{prefix_result}_reverse_threats.csv")                    
        #threat_reversed_time = result_time(time() - start_time)
        #print(f"[INFO] Reversed Threats saved for {idx+1} out of {iterations} after {threat_reversed_time}")
        
        total_time = result_time(time() - start_time)
        print(f"[RESULT] Finished iteration {idx} out of {iterations}, it took {total_time}")

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script that obtains judging on the provided threat model"
    )
    parser.add_argument("-a", "--application", required=True, type=str)
    parser.add_argument("-t", "--tool", required=True, type=str)
    parser.add_argument("-ai", "--aimodel", required=True, type=str)
    parser.add_argument("-i", "--iterations", required=True, type=int)
    args = parser.parse_args()
    
    application = args.application
    tool = args.tool
    ai = args.aimodel
    iterations = args.iterations
    
    # For easy debugging
    # application = "message_queue_app"
    # tool = "stridegpt"
    # ai = "gemma3:4b-it-q4_K_M"
    # iterations = 2
    
    random.seed(21)
    seeds = [random.randint(1, 1000) for _ in range(iterations)]
    
    tool_folder = f"results/{application}"
    human_folder = f"threat_templates/{application}"
    current_results = os.listdir(tool_folder)

    assets = load_assets(f"{human_folder}/assets.json")
    print(f"[INFO] System has assets: {assets}")
    
    # Load threat models
    human_model, ai_model = load_threat_models(tool_folder, human_folder, tool)
    
    tms = np.array(np.meshgrid(human_model, ai_model)).T.reshape(-1,2)
    tms_reversed = np.array(np.meshgrid(ai_model, human_model)).T.reshape(-1,2)
    print("[INFO] Threat models are ready for judging")
    
    result_path = f"{tool_folder}/{ai}_{tool}"
    
    # For easy debugging
    # ai_model = random.sample(ai_model, 10)
    # tms = random.sample(list(tms), 10)
    # tms_reversed = random.sample(list(tms_reversed), 10)
    
    perform_judging(ai, ai_model, tms, tms_reversed, assets, seeds, iterations, result_path)
    print(f"[SUCCESS] Finished judging threat model for {application} with {tool}")
