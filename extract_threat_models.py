import os
import json
import shutil
from STRIDEgpt_models.convert_model import extract_threat_model


def extract_STRIDEgpt_models(assets: list[str], applications: list[str], result_folder: str) -> None:
    """
    Extracts threat models from markdown files in the STRIDEgpt_models directory,
    and saves them as a JSON file in the result directory.
    Parameters:
        applications (list[str]): List of application names to process.
        result_folder (str): Path to the directory where the JSON files will be saved.
    """
    folder_path = "STRIDEgpt_models"
    
    application_path = f"{folder_path}/{application}"
    
    # Convert the STRIDEgpt threat model files into JSON
    threat_model = extract_threat_model(application_path, assets=assets)
    
    # Save the JSON to a file
    json_path = f"{result_folder}/{application}/STRIDEgpt_threat_model.json"
    with open(json_path, "w") as json_file:
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