import json
import os
import csvimport ast

import pandas as pd

def load_judging(file_path):
    return pd.read_csv(file_path)

def load_judgings(files, column_to_lists):
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        for column in column_to_lists:
            df[column] = df[column].apply(ast.literal_eval)
        dfs.append(df)
    return dfs

def save_stats(result_folder, tool, stats_name, all_ai_stats, all_ai_itself_stats, all_human_model_stats):
    stats_folder = f"{result_folder}/stats"
    os.makedirs(stats_folder, exist_ok=True)
    
    if all_human_model_stats:
        with open(f"{stats_folder}/human_{tool}_{stats_name}.json", "w") as json_file:
            json.dump(all_human_model_stats, json_file, indent=4)
            
    with open(f"{stats_folder}/self_{tool}_{stats_name}.json", "w") as json_file:
        json.dump(all_ai_itself_stats, json_file, indent=4)
            
    with open(f"{stats_folder}/ais_{tool}_{stats_name}.json", "w") as json_file:
        json.dump(all_ai_stats, json_file, indent=4)


def load_assets(assets_path):
    with open(assets_path, "r") as assets_file:
        assets = json.load(assets_file)
    return assets

def load_threat_models(result_folder:str, human_folder:str, tool:list) -> tuple:
    with open(f"{human_folder}/threat_model.json", "r") as file:
        human_threat_model = json.load(file)

    ai_threat_model_path = f"{result_folder}/{tool}_model.json"
    with open(ai_threat_model_path, "r") as ai_file:
        ai_threat_model = json.load(ai_file)
        
    return human_threat_model, ai_threat_model

def append_hallucination_results(results, ai, id, seed, csv_file):
    # Check if file exists to decide whether to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["result_id", "model", "seed", "category", "asset"])

        if not file_exists:
            writer.writeheader()

        for idx in range(len(results)):
            writer.writerow({
                "result_id": id,
                "model": ai,
                "seed": seed,
                "category": results["category"],
                "asset": results["asset"]
            })

def append_threat_results(results, ai, id, reversed_val, csv_file):
    # Check if file exists to decide whether to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["result_id", "model", "reversed", "threats", "mitigations", "risks_same", "risks_more", "risks_less"])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "result_id": id,
            "model": ai,
            "reversed": reversed_val,
            "threats": results["threats"],
            "mitigations": results["mitigations"],
            "risks_same": results["risks"]["same"],
            "risks_more": results["risks"]["more"],
            "risks_less": results["risks"]["less"],
        })