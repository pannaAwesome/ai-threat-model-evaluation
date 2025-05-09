import csv
import json
import os
import sys

def threats_risk_to_json(csv_path):
    """
    Reads a CSV file and converts each row into a JSON object with the structure:
    
    {
      "Type": <Use case>,
      "Assets": <Component>,
      "Description": <Threat>,
      "Risk": <Projected Risk>
    }

    :param csv_path: full path to the CSV file
    :return: JSON string representation of the CSV file data
    """
    json_list = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                json_obj = {
                    "Type": row.get("Use case", "").strip(),
                    "Assets": row.get("Component", "").strip(),
                    "Description": row.get("Threat", "").strip(),
                    "Risk": row.get("Projected Risk", "").strip()
                }
                json_list.append(json_obj)
    except FileNotFoundError:
        print(f"Error: The file at {csv_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    return json_list

def mitigations_to_json(csv_path):
    """
    Reads a CSV file and converts each row into a JSON object with the structure:
    
    {
      "Type": <Use case>,
      "Assets": <Component>,
      "Description": <Threat>,
      "Risk": <Projected Risk>
    }

    :param csv_path: full path to the CSV file
    :return: JSON string representation of the CSV file data
    """
    json_list = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                json_obj = {
                    "Assets": row.get("Component", "").strip(),
                    "Mitigation": f"{row.get('Countermeasure', '').strip()}, {row.get('Description', '').strip()}"
                }
                json_list.append(json_obj)
    except FileNotFoundError:
        print(f"Error: The file at {csv_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    return json_list

def convert_iriusrisk(folder_path):
    """
    Converts IriusRisk CSV files to JSON format.
    
    :param folder_path: Path to the directory containing the CSV files.
    :return: A tuple containing two JSON strings: threats and mitigations.
    """
    threats_csv = os.path.join(folder_path, "threats.csv")
    mitigations_csv = os.path.join(folder_path, "mitigations.csv")
    
    threats_json = threats_risk_to_json(threats_csv)
    mitigations_json = mitigations_to_json(mitigations_csv)
    
    return threats_json, mitigations_json
