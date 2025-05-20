from stats.files import read_csv_hallucinations, read_csv_threats
from stats.stat_measures import *

def threats_ai_ai(ai_files, total):
    found_threats = []
    found_mitigations = []
    found_risk_same = []
    found_risk_more = []
    found_risk_less = []
    for ai_file in ai_files:
        df_ai = read_csv_threats(ai_file)
        found = [item for sublist in df_ai['threats'] for item in sublist]
        found_threats.append(found)
        found = [item for sublist in df_ai['mitigations'] for item in sublist]
        found_mitigations.append(found)
        found = [item for sublist in df_ai['risks_same'] for item in sublist]
        found_risk_same.append(found)
        found = [item for sublist in df_ai['risks_more'] for item in sublist]
        found_risk_more.append(found)
        found = [item for sublist in df_ai['risks_less'] for item in sublist]
        found_risk_less.append(found)
    
    # Calculate for threats
    matrix = build_ratings_matrix(found_threats, total)
    threats_kappa = fleiss_kappa(matrix)
    
    # Calculate for mitigations
    matrix = build_ratings_matrix(found_mitigations, total)
    mitigations_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_same
    matrix = build_ratings_matrix(found_risk_same, total)
    risk_same_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_more
    matrix = build_ratings_matrix(found_risk_more, total)
    risk_more_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_less
    matrix = build_ratings_matrix(found_risk_less, total)
    risk_less_kappa = fleiss_kappa(matrix)
    
    return {
        "threats_kappas": threats_kappa,
        "mitigations_kappas": mitigations_kappa,
        "risk_same_kappas": risk_same_kappa,
        "risk_more_kappas": risk_more_kappa,
        "risk_less_kappas": risk_less_kappa
    }
    
def hallucinations_ai_ai(ai_files, total):
    found_category = []
    found_asset = []
    for ai_file in ai_files:
        df_ai = read_csv_hallucinations(ai_file)
        found = [item for sublist in df_ai['category'] for item in sublist]
        found_category.append(found)
        found = [item for sublist in df_ai['asset'] for item in sublist]
        found_asset.append(found)
    
    # Calculate for category
    matrix = build_ratings_matrix(found_category, total)
    category_kappa = fleiss_kappa(matrix)
    
    # Calculate for asset
    matrix = build_ratings_matrix(found_category, total)
    asset_kappa = fleiss_kappa(matrix)
    
    return {
        "category_kappa": category_kappa,
        "asset_kappa": asset_kappa
    }