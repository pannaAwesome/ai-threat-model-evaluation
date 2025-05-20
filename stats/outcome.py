from stats.files import *
from collections import Counter

def threats_count_outcome(ai_files):
    counts = []
    for file in ai_files:
        df_ai = read_csv_threats(file)
        
        threats = df_ai["threats"].apply(lambda x: len(set(x))).mean()
        threats_max = df_ai["threats"].apply(lambda x: len(set(x))).max()
        threats_min = df_ai["threats"].apply(lambda x: len(set(x))).min()

        duplicate_threats = df_ai['threats'].apply(lambda x: sum(count - 1 for count in Counter(x).values() if count > 1)).max()

        mitigations = df_ai["mitigations"].apply(lambda x: len(set(x))).mean()
        mitigations_max = df_ai["mitigations"].apply(lambda x: len(set(x))).max()
        mitigations_min = df_ai["mitigations"].apply(lambda x: len(set(x))).min()

        risk_same = df_ai["risks_same"].apply(lambda x: len(set(x))).mean()
        risk_same_max = df_ai["risks_same"].apply(lambda x: len(set(x))).max()
        risk_same_min = df_ai["risks_same"].apply(lambda x: len(set(x))).min()

        risk_more = df_ai["risks_more"].apply(lambda x: len(set(x))).mean()
        risk_more_max = df_ai["risks_more"].apply(lambda x: len(set(x))).max()
        risk_more_min = df_ai["risks_more"].apply(lambda x: len(set(x))).min()

        risk_less = df_ai["risks_less"].apply(lambda x: len(set(x))).mean()
        risk_less_max = df_ai["risks_less"].apply(lambda x: len(set(x))).max()
        risk_less_min = df_ai["risks_less"].apply(lambda x: len(set(x))).min()
        
        counts.append({
            "model": df_ai["model"].iloc[0],
            "duplicates": int(duplicate_threats),
            "threats": int(threats),
            "threats_max": int(threats_max),
            "threats_min": int(threats_min),
            "mitigations": int(mitigations),
            "mitigations_max": int(mitigations_max),
            "mitigations_min": int(mitigations_min),
            "risk_same": int(risk_same),
            "risk_same_max": int(risk_same_max),
            "risk_same_min": int(risk_same_min),
            "risk_more": int(risk_more),
            "risk_more_max": int(risk_more_max),
            "risk_more_min": int(risk_more_min),
            "risk_less": int(risk_less),
            "risk_less_max": int(risk_less_max),
            "risk_less_min": int(risk_less_min)
        })     
        
    return counts

def hallucinations_count_outcome(ai_files):
    counts = []
    for file in ai_files:
        df_ai = read_csv_hallucinations(file)
        
        category_max = df_ai["category"].apply(lambda x: len(x)).max()
        category_min = df_ai["category"].apply(lambda x: len(x)).min()
        category = df_ai["category"].apply(lambda x: len(x)).mean()
        asset_max = df_ai["asset"].apply(lambda x: len(x)).max()
        asset_min = df_ai["asset"].apply(lambda x: len(x)).min()
        asset = df_ai["asset"].apply(lambda x: len(x)).mean()
        
        counts.append({
            "model": df_ai["model"].iloc[0],
            "category": int(category),
            "category_max": int(category_max),
            "category_min": int(category_min),
            "asset": int(asset),
            "asset_max": int(asset_max),
            "asset_min": int(asset_min)
        })
    return counts