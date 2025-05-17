import pandas as pd
import ast

def read_csv_threats(filepath):
    """
    Reads the CSV and converts columns containing list strings into actual lists.
    
    Returns a pandas DataFrame with parsed list columns.
    """
    df = pd.read_csv(filepath)
    
    # Columns that contain list strings to parse
    list_columns = ['threats', 'mitigations', 'risk_same', 'risk_more', 'risk_less']
    
    for col in list_columns:
        # Use ast.literal_eval to convert string list to actual Python list safely
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
    
    return df

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

