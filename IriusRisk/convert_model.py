import pandas as pd
import os
import sys    

def csv_to_dataframe(threat_path: str, mitigation_path: str) -> pd.DataFrame:
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
    threat_df = pd.read_csv(threat_path, sep=',', skipinitialspace=True, engine='python')
    threat_df = threat_df.rename(columns={"Name": "Threat", "Description": "Scenario"})
    threat_df = threat_df[["Component", "Use Case", "Threat", "Scenario", "Current Risk"]]
    
    mitigation_df = pd.read_csv(mitigation_path, sep=',', skipinitialspace=True, engine='python')
    mitigation_df = mitigation_df.rename(columns={"Name": "Mitigation", "Description": "Fix"})
    mitigation_df = mitigation_df[["Component", "Use Case", "Threat", "Mitigation", "Fix"]]

    merged_df = pd.merge(threat_df, mitigation_df, how='left', on=["Component", "Use Case", "Threat"])

    return merged_df

def convert_df_to_json(df: pd.DataFrame) -> str:
    """
    Converts a DataFrame to a JSON string.
    
    :param df: DataFrame to convert.
    :return: JSON string representation of the DataFrame.
    """
    result = []
    idx = 1
    for _, row in df.iterrows():
        entry = {
            "ID": idx,
            "Category": row['Use Case'],
            "Asset": row['Component'],
            "Threat": f"{row['Threat']}. {row['Scenario']}",
            "Mitigation": f"{row['Mitigation']}. {row['Fix']}",
            "Risk": f"{row['Current Risk']} out of 100"
        }
        result.append(entry)
        idx = idx + 1
    return result

def convert_iriusrisk(folder_path):
    """
    Converts IriusRisk CSV files to JSON format.
    
    :param folder_path: Path to the directory containing the CSV files.
    :return: A tuple containing two JSON strings: threats and mitigations.
    """
    threats_csv = os.path.join(folder_path, "threats.csv")
    mitigations_csv = os.path.join(folder_path, "mitigations.csv")
    
    df = csv_to_dataframe(threats_csv, mitigations_csv)
    threat_json = convert_df_to_json(df)
    
    return threat_json
