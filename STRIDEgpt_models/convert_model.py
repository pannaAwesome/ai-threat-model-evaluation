import pandas as pd
import re
import os

def extract_markdown_table(filepath: str) -> pd.DataFrame:
    """
    Extracts the first markdown table found in a file and returns it as a pandas DataFrame.

    Parameters:
        filepath (str): Path to the markdown file containing the table.

    Returns:
        pd.DataFrame: DataFrame representation of the first markdown table found.

    Raises:
        ValueError: If no markdown table is found in the file.
    """
    with open(filepath, 'r') as file:
        content = file.read()
    table_match = re.search(r'(\|.*?\|\n(?:\|.*?\|\n)+)', content, re.DOTALL)
    if table_match:
        table = table_match.group(1)
        temp_path = filepath + '.tmp'
        with open(temp_path, 'w') as temp_file:
            temp_file.write(table)
        df = pd.read_csv(temp_path, sep='|', skipinitialspace=True, engine='python')[1:-1].dropna(axis=1, how='all')
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    else:
        raise ValueError(f"No markdown table found in {filepath}")

def merge_dataframes(threat_path: str, mitigation_path: str, dread_path: str) -> pd.DataFrame:
    """
    Merges threat, mitigation, and dread assessment tables into a single DataFrame.
    Assumes the dread table has the same row order as the other two tables.

    Parameters:
        threat_path (str): Path to the threat_model.md file.
        mitigation_path (str): Path to the mitigations.md file.
        dread_path (str): Path to the dread_assessment.md file.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all three sources.

    Raises:
        ValueError: If the number of rows does not match across all files.
    """
    threat_df = extract_markdown_table(threat_path)
    mitigation_df = extract_markdown_table(mitigation_path)
    dread_df = extract_markdown_table(dread_path)

    if not (len(threat_df) == len(mitigation_df) == len(dread_df)):
        raise ValueError("Mismatch in number of rows across threat, mitigation, and dread dataframes.")

    merged_df = pd.merge(threat_df, mitigation_df, on=["Threat Type", "Scenario"])

    dread_df = dread_df.reset_index(drop=True)
    merged_df = merged_df.reset_index(drop=True)
    dread_columns = [col for col in dread_df.columns if col not in ["Threat Type", "Scenario"]]
    for col in dread_columns:
        merged_df[col] = dread_df[col]

    return merged_df

import re

def find_assets_in_threat(threat, assets):
    """finds assets in a description of a threat

    Args:
        threat (str): the threat to read
        assets (list): assets in the system

    Returns:
        list: list of assets found in the threat description
    """
    threat_lower = threat.lower()

    # Build a regex to find all known entities in the sentence
    asset_patterns = [re.escape(e.lower()) for e in assets]
    asset_regex = r'\b(?:' + '|'.join(asset_patterns) + r')\b'

    # Find all matches and their positions
    matches = [(m.group(0), m.start()) for m in re.finditer(asset_regex, threat_lower)]

    if not matches:
        return []

    # Find the earliest match position
    earliest_pos = min(pos for _, pos in matches)
    
    # Calculate max distance between assets in a list based on the assets starting position
    max_distance = max_distance = len(max(assets, key=len) + " and the ") + 1


    # Find all contiguous asset matches starting at the first one
    found = []
    for asset, pos in matches:
        if pos == earliest_pos or (found and pos - matches[matches.index((asset, pos)) - 1][1] <= max_distance):
            # Add the properly cased version from the original list
            for original in assets:
                if asset == original.lower():
                    found.append(original)
                    break
        elif found:
            break  # stop after first group of contiguous matches

    return found

def create_threat_model_json(merged_df: pd.DataFrame, assets: list[str]) -> list[dict]:
    """
    Converts a merged DataFrame into a list of JSON objects representing the threat model.

    Parameters:
        merged_df (pd.DataFrame): Merged DataFrame with threat, mitigation, and dread data.
        assets (list[str]): List of asset strings to match within the Scenario field.

    Returns:
        list[dict]: List of threat model entries in dictionary format.
    """
    result = []
    for _, row in merged_df.iterrows():
        assets_in_threat = find_assets_in_threat(row["Scenario"], assets)
        
        if len(assets_in_threat) == 0:
            entry = {
                "Category": row["Threat Type"],
                "Asset": assets_in_threat[0],
                "Threat": f'{row["Scenario"]} {row["Potential Impact"]}',
                "Mitigation": row["Suggested Mitigation(s)"],
                "Risk": f'{row["Risk Score"]} out of 10'
            }
            result.append(entry)
        else:
            for asset in assets_in_threat:
                entry = {
                    "Category": row["Threat Type"],
                    "Asset": assets_in_threat[0],
                    "Threat": f'{row["Scenario"]} {row["Potential Impact"]}',
                    "Mitigation": row["Suggested Mitigation(s)"],
                    "Risk": row["Risk Score"]
                }
                result.append(entry)
    return result

def convert_STRIDEgpt(folder_path: str, assets: list[str]) -> None:
    """
    Function to merge data from markdown files and export it to a JSON file.

    Parameters:
        folder_path (str): Path to the directory containing the markdown files.
        assets (list[str]): List of assets to match within threat scenarios.
    """
    threat_path = os.path.join(folder_path, "threat_model.md")
    mitigation_path = os.path.join(folder_path, "mitigations.md")
    dread_path = os.path.join(folder_path, "dread_assessment.md")

    merged_df = merge_dataframes(threat_path, mitigation_path, dread_path)
    threat_model_json = create_threat_model_json(merged_df, assets)
    
    return threat_model_json