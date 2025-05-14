import json
import os
import csv

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