from stats.files import read_csv_hallucinations, read_csv_threats
from stats.confusion_matrix import *

def _compare_pair(rater1, rater2, total):
    conf = count_based_confusion_matrix(rater1, rater2, total)
    kappa = cohens_kappa(conf, total)
    return kappa

def threats_ai_position_bias(model, df1, df2, total):
    # Calculate for threats
    reverse_found = sum(df2["threats"], [])
    found = sum(df1["threats"], [])
    threats_kappa = _compare_pair(reverse_found, found, total)
    # Calculate for mitigations
    reverse_found = sum(df2["mitigations"], [])
    found = sum(df1["mitigations"], [])
    mitigations_kappa = _compare_pair(reverse_found, found, total)
    # Calculate for risk same
    reverse_found = sum(df2["risk_same"], [])
    found = sum(df1["risk_same"], [])
    risk_same_kappa = _compare_pair(reverse_found, found, total)
    # Calculate for risk_more
    reverse_found = sum(df2["risk_more"], [])
    found = sum(df1["risk_more"], [])
    risk_more_kappa = _compare_pair(reverse_found, found, total)
    # Calculate for risk less
    reverse_found = sum(df2["risk_less"], [])
    found = sum(df1["risk_less"], [])
    risk_less_kappa = _compare_pair(reverse_found, found, total)
    
    return {
        "model": model,
        "threats_kappas": threats_kappa,
        "mitigations_kappas": mitigations_kappa,
        "risk_same_kappas": risk_same_kappa,
        "risk_more_kappas": risk_more_kappa,
        "risk_less_kappas": risk_less_kappa
    }

def threats_ai_repetition(ai_file, total):
    df_ai = read_csv_threats(ai_file)
    
    # Calculate for threats
    found = list(df_ai["threats"])
    matrix = build_ratings_matrix(found, total)
    threats_kappa = fleiss_kappa(matrix)
    
    # Calculate for mitigations
    found = list(df_ai["mitigations"])
    matrix = build_ratings_matrix(found, total)
    mitigations_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_same
    found = list(df_ai["risk_same"])
    matrix = build_ratings_matrix(found, total)
    risk_same_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_more
    found = list(df_ai["risk_more"])
    matrix = build_ratings_matrix(found, total)
    risk_more_kappa = fleiss_kappa(matrix)
    
    # Calculate for risk_less
    found = list(df_ai["risk_less"])
    matrix = build_ratings_matrix(found, total)
    risk_less_kappa = fleiss_kappa(matrix)
    
    return {
        "model": df_ai["model"].iloc[0],
        "threats_kappas": threats_kappa,
        "mitigations_kappas": mitigations_kappa,
        "risk_same_kappas": risk_same_kappa,
        "risk_more_kappas": risk_more_kappa,
        "risk_less_kappas": risk_less_kappa
    }