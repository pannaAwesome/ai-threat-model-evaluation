import pandas as pd
import json
import os

def get_assets_with_threats(application: str):
    assets_path = f"{application}/assets_to_threats.json"
    with open(assets_path, "r") as assets_file:
        assets = json.load(assets_file)
    
    return assets

def get_threat_info_for_assets(assets: pd.DataFrame, folder_path) -> pd.DataFrame:
    threats_info_path = os.path.join(folder_path, "threat_descriptions.json")
    threat_info_df = pd.read_json(threats_info_path, orient="records")
    
    mitigations_info_path = os.path.join(folder_path, "mitigation_descriptions.json")
    mitigation_df = pd.read_json(mitigations_info_path, orient="records")
    
    output = []

    for asset, threats in assets.items():
        for threat in threats:
            # Get the row corresponding to the threat category
            threat_info_row = threat_info_df[threat_info_df["Category"] == threat]
            if threat_info_row.empty:
                continue  # Skip if the threat category isn't found

            # Extract values from the single-row DataFrame
            threat_info = threat_info_row.iloc[0]
            threat_description = threat_info["Description"]
            risk = threat_info["Risk"]
            mitigation_names = threat_info["Mitigations"]

            # Filter mitigation descriptions
            mitigation_rows = mitigation_df[mitigation_df["Mitigation"].isin(mitigation_names)]
            mitigation_descriptions = [
                f"{row['Mitigation']}: {row['Description']}"
                for _, row in mitigation_rows.iterrows()
            ]
            mitigations_text = " ".join(mitigation_descriptions)

            # Build the output entry
            entry = {
                "Category": threat,
                "Asset": asset,
                "Threat": threat_description,
                "Mitigation": mitigations_text,
                "Risk": f"{risk} out of 3"
            }
            output.append(entry)

    return output
    
def convert_threatcanvas(folder_path: str, application: str) -> list:
    """
    Converts ThreatCanvas files to JSON format.
    
    :param 
        folder_path: Path to the directory containing the threat model files.
        application: Name of the application for the threat model.
    :return: A list containing the json formatted threat model.
    """
    
    app_path = os.path.join(folder_path, application)   
    assets = get_assets_with_threats(app_path)
    threat_json = get_threat_info_for_assets(assets, folder_path)
    
    return threat_json