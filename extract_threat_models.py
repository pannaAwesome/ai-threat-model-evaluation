import os
import json

from argparse import ArgumentParser

from STRIDEgpt_models.convert_model import convert_STRIDEgpt
from IriusRisk.convert_model import convert_iriusrisk
from ThreatCanvas.convert_model import convert_threatcanvas
from utils.files import load_assets


def extract_STRIDEgpt_models(assets: list[str], application: list[str], result_folder: str) -> None:
    """
    Extracts threat models from markdown files in the STRIDEgpt_models directory,
    and saves them as a JSON file in the result directory.
    Parameters:
        applications (list[str]): List of application names to process.
        result_folder (str): Path to the directory where the JSON files will be saved.
    """
    folder_path = "STRIDEgpt_models"
    
    application_path = f"{folder_path}/{application}"
    
    threat_model = convert_STRIDEgpt(application_path, assets)
    
    print(f"Threat model for {application} has {len(threat_model)} threats.")
    
    threat_path = f"{result_folder}/{application}/stridegpt_model.json"
    with open(threat_path, "w") as json_file:
        json.dump(threat_model, json_file, indent=4)
        
def extract_IriusRisk_models(application: list[str], result_folder: str) -> None:
    """
    Extracts threat models from csv files in the IriusRisk directory,
    and saves them as a JSON file in the result directory.
    Parameters:
        applications (list[str]): List of application names to process.
        result_folder (str): Path to the directory where the JSON files will be saved.
    """
    folder_path = "IriusRisk"
    
    application_path = f"{folder_path}/{application}"
    
    threat_model = convert_iriusrisk(application_path)
    
    print(f"Threat model for {application} has {len(threat_model)} threats.")
    
    # Save the threat model to a file
    threat_path = f"{result_folder}/{application}/iriusrisk_model.json"
    with open(threat_path, "w") as json_file:
        json.dump(threat_model, json_file, indent=4)
        
def extract_ThreatCanvas_models(application: list[str], result_folder: str) -> None:
    """
    Extracts threat models from csv files in the ThreatCanvas directory,
    and saves them as a JSON file in the result directory.
    Parameters:
        applications (list[str]): List of application names to process.
        result_folder (str): Path to the directory where the JSON files will be saved.
    """
    folder_path = "ThreatCanvas"
    
    threat_model = convert_threatcanvas(folder_path, application)
    
    print(f"Threat model for {application} has {len(threat_model)} threats.")
    
    # Save the threat model to a file
    threat_path = f"{result_folder}/{application}/threatcanvas_model.json"
    with open(threat_path, "w") as json_file:
        json.dump(threat_model, json_file, indent=4)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script that extracts threat models for a specific application"
    )
    parser.add_argument("-a", "--application", required=True, type=str)
    args = parser.parse_args()
    
    application = args.application
    
    result_folder = "results"
    
    print(f"[INFO] Processing threat models for application: {application}")
    
    if not os.path.exists(f"{result_folder}/{application}"):
        os.makedirs(f"{result_folder}/{application}")

    assets = load_assets(f"threat_templates/{application}/assets.json")
    print(f"[INFO] System has assets: {assets}")
    
    extract_STRIDEgpt_models(assets, application, result_folder)
    print(f"[INFO] Extracted threat model for STRIDEgpt...")
    
    extract_IriusRisk_models(application, result_folder)
    print(f"[INFO] Extracted threat model for IriusRisk...")
    
    extract_ThreatCanvas_models(application, result_folder)
    print(f"[INFO] Extracted threat model for ThreatCanvas...")