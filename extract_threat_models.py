import os
import json
import shutil
from STRIDEgpt_models.convert_model import convert_STRIDEgpt
from IriusRisk.convert_model import convert_iriusrisk
from ThreatCanvas.convert_model import convert_threatcanvas


def extract_STRIDEgpt_models(assets: list[str], application: list[str], result_folder: str) -> None:
    """
    Extracts threat models from markdown files in the STRIDEgpt_models directory,
    and saves them as a JSON file in the result directory.
    Parameters:
        applications (list[str]): List of application names to process.
        result_folder (str): Path to the directory where the JSON files will be saved.
    """
    folder_path = "STRIDEgpt_models"
    
    #for application in applications:
    application_path = f"{folder_path}/{application}"
    
    # Convert the STRIDEgpt threat model files into JSON
    threat_model = convert_STRIDEgpt(application_path, assets)
    
    print(f"Threat model for {application} has {len(threat_model)} threats.")
    
    # Save the threats to a file
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
    
    #for application in applications:
    application_path = f"{folder_path}/{application}"
    
    # Convert the IriusRisk threat model files into JSON
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
    
    # Convert the ThreatCanvas threat model files into JSON
    threat_model = convert_threatcanvas(folder_path, application)
    
    print(f"Threat model for {application} has {len(threat_model)} threats.")
    
    # Save the threat model to a file
    threat_path = f"{result_folder}/{application}/threatcanvas_model.json"
    with open(threat_path, "w") as json_file:
        json.dump(threat_model, json_file, indent=4)

if __name__ == "__main__":
    applications = ["message_queue_app"]
    result_folder = "results"
    
    # Delete results folder if exists
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)
        
    # Create the results directory and subdirectories for each application
    os.makedirs(result_folder)
    for application in applications:
        print(f"Processing threat model for application: {application}")
        os.makedirs(f"{result_folder}/{application}")

        # Collect assets for the application
        assets_path = f"threat_templates/{application}/assets.json"
        with open(assets_path, "r") as assets_file:
            assets = json.load(assets_file)
        
        # Extract threat models from the STRIDEgpt_models directory
        print(f"Extracting threat model for STRIDEgpt...")
        extract_STRIDEgpt_models(assets, application, result_folder)
        
        # Extract threat models from the IriusRisk directory
        print(f"Extracting threat model for IriusRisk...")
        extract_IriusRisk_models(application, result_folder)
        
        # Extract threat models from the ThreatCanvas directory
        print(f"Extracting threat model for ThreatCanvas...")
        extract_ThreatCanvas_models(application, result_folder)