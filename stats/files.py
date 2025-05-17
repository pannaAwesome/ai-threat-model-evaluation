import pandas as pd
import ast
import glob
import os
import shutil
import re

def read_csv_threats(filepath):
    """
    Reads the CSV and converts columns containing list strings into actual lists.
    
    Returns a pandas DataFrame with parsed list columns.
    """
    df = pd.read_csv(filepath)
    
    # Columns that contain list strings to parse
    list_columns = ['threats', 'mitigations', 'risks_same', 'risks_more', 'risks_less']
    
    for col in list_columns:
        # Use ast.literal_eval to convert string list to actual Python list safely
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
    
    return df

def read_threat_reverse_pairs(folder):
    """
    Finds and reads pairs of files:
    - {model}_{tool}_threats.csv
    - {model}_{tool}_reverse_threats.csv
    
    Returns a list of tuples: (prefix, threats_df, reverse_threats_df)
    """
    # Find all *_threats.csv and *_reverse_threats.csv files
    threat_files = glob.glob(os.path.join(folder, '*_threats.csv'))
    reverse_files = glob.glob(os.path.join(folder, '*_reverse_threats.csv'))

    # Build a dict from filename prefix (model_tool) to file path
    def extract_prefix(path, reverse=False):
        name = os.path.basename(path)
        pattern = r"(.+?)_threats.csv" if not reverse else r"(.+?)_reverse_threats.csv"
        match = re.match(pattern, name)
        return match.group(1) if match else None
    
    def make_lists(df):
        # Columns that contain list strings to parse
        list_columns = ['threats', 'mitigations', 'risks_same', 'risks_more', 'risks_less']
        
        for col in list_columns:
            # Use ast.literal_eval to convert string list to actual Python list safely
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
        return df

    threat_dict = {extract_prefix(f): f for f in threat_files}
    reverse_dict = {extract_prefix(f, reverse=True): f for f in reverse_files}

    pairs = []
    for key in threat_dict:
        if key in reverse_dict:
            threats_df = pd.read_csv(threat_dict[key])
            threats_df = make_lists(threats_df)
            reverse_df = pd.read_csv(reverse_dict[key])
            reverse_df = make_lists(reverse_df)
            pairs.append((key, threats_df, reverse_df))

    return pairs

def read_csv_hallucinations(filepath):
    """
    Reads the CSV and converts columns containing list strings into actual lists.
    
    Returns a pandas DataFrame with parsed list columns.
    """
    df = pd.read_csv(filepath)
    
    # Columns that contain list strings to parse
    list_columns = ['category', 'asset']
    
    for col in list_columns:
        # Use ast.literal_eval to convert string list to actual Python list safely
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
    
    return df

def get_threat_files(folder_path, tool):
    """
    Returns a list of file paths in `folder_path` matching the pattern *{tool}_threats.csv
    """
    pattern = os.path.join(folder_path, f"*{tool}_threats.csv")
    matching_files = glob.glob(pattern)
    return matching_files

def get_hallucination_files(folder_path, tool):
    """
    Returns a list of file paths in `folder_path` matching the pattern *{tool}_hallucinations.csv
    """
    pattern = os.path.join(folder_path, f"*{tool}_hallucinations.csv")
    matching_files = glob.glob(pattern)
    return matching_files

def reset_stats_folder(folder_path):
    # Delete the folder if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Recreate the folder
    os.makedirs(folder_path)