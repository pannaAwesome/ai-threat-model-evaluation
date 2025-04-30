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
        scenario_text = row["Scenario"].lower()
        matched_assets = [asset for asset in assets if asset.lower() in scenario_text]

        entry = {
            "Type": row["Threat Type"],
            "Threat": "",
            "Assets": matched_assets,
            "Description": row["Scenario"],
            "Impact": row["Potential Impact"],
            "Mitigation": row["Suggested Mitigation(s)"],
            "Risk": row["Risk Score"]
        }
        result.append(entry)
    return result

def extract_threat_model(folder_path: str, assets: list[str]) -> None:
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