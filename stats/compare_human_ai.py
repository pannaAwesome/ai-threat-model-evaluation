from stats.files import read_csv_hallucinations, read_csv_threats
from stats.stat_measures import *

def _compare_pair(rater1, rater2, total):
    conf = count_based_confusion_matrix(rater1, rater2, total)
    kappa = cohens_kappa(conf, total)
    return kappa

def hallucinations_compare_human_ai(human_file, ai_file, total):
    # Example usage:
    df_human = read_csv_hallucinations(human_file)
    df_ai = read_csv_hallucinations(ai_file)
    
    category_kappas = []
    asset_kappas = []
    for row in df_ai.itertuples():
        category_kappa = _compare_pair(row.category, df_human["category"].iloc[0], total)
        asset_kappa = _compare_pair(row.asset, df_human["asset"].iloc[0], total)
        
        category_kappas.append(category_kappa)
        asset_kappas.append(asset_kappa)
    
    return {
        "model": df_ai["model"].iloc[0],
        "avg_category": sum(category_kappas) / len(category_kappas),
        "category_kappas": category_kappas,
        "avg_asset": sum(asset_kappas) / len(asset_kappas),
        "asset_kappas": asset_kappas
    }
    
def threat_compare_human_ai(human_file, ai_file, total):
    # Example usage:
    df_human = read_csv_threats(human_file)
    df_ai = read_csv_threats(ai_file)
    
    threats_kappas = []
    mitigations_kappas = []
    risk_same_kappas = []
    risk_more_kappas = []
    risk_less_kappas = []
    for row in df_ai.itertuples():
        kappa = _compare_pair(row.threats, df_human["threats"].iloc[0], total)
        threats_kappas.append(kappa)
        
        kappa = _compare_pair(row.mitigations, df_human["mitigations"].iloc[0], total)
        mitigations_kappas.append(kappa)
        
        kappa = _compare_pair(row.risks_same, df_human["risks_same"].iloc[0], total)
        risk_same_kappas.append(kappa)
        
        kappa = _compare_pair(row.risks_more, df_human["risks_more"].iloc[0], total)
        risk_more_kappas.append(kappa)
        
        kappa = _compare_pair(row.risks_less, df_human["risks_less"].iloc[0], total)
        risk_less_kappas.append(kappa)
    
    return {
        "model": df_ai["model"].iloc[0],
        "avg_threats": sum(threats_kappas) / len(threats_kappas),
        "threat_kappas": threats_kappas,
        "avg_mitigations": sum(mitigations_kappas) / len(mitigations_kappas),
        "mitigations_kappas": mitigations_kappas,
        "avg_risk_same": sum(risk_same_kappas) / len(risk_same_kappas),
        "risk_same_kappas": risk_same_kappas,
        "avg_risk_more": sum(risk_more_kappas) / len(risk_more_kappas),
        "risk_more_kappas": risk_more_kappas,
        "avg_risk_less": sum(risk_less_kappas) / len(risk_less_kappas),
        "risk_less_kappas": risk_less_kappas
    }