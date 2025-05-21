from stats.files import *
from collections import Counter

def _compute_risk_proportions(row):
    total_threats = len(row['threats'])
    if total_threats == 0:
        return pd.Series({'same_pct': 0, 'more_pct': 0, 'less_pct': 0})
    
    same_pct = (total_threats - len(row['risks_more']) - len(row["risks_less"])) / total_threats
    more_pct = len(row['risks_more']) / total_threats
    less_pct = len(row['risks_less']) / total_threats
    
    return pd.Series({'same_pct': same_pct, 'more_pct': more_pct, 'less_pct': less_pct})

def _compute_mitigation_proportion(row):
    total_threats = len(row['threats'])
    if total_threats == 0:
        return 0
    return len(row['mitigations']) / total_threats

def _normalized_duplicate_count(row, actual_threats):
    threats_list = row['threats']
    if actual_threats == 0:
        return 0
    counts = Counter(threats_list)
    # Count how many unique elements appear more than once
    unique_duplicate_count = sum(1 for count in counts.values() if count > 1)
    return unique_duplicate_count / actual_threats

def threats_count_outcome(ai_files, comparisons, actual_threats):
    counts = []
    for file in ai_files:
        df_ai = read_csv_threats(file)
        
        threats = df_ai["threats"].apply(lambda x: len(set(x))).mean()/actual_threats

        duplicate_threats = df_ai.apply(_normalized_duplicate_count, axis=1, args=(actual_threats,)).mean()

        mitigations = df_ai.apply(_compute_mitigation_proportion, axis=1)
        mitigations = mitigations.mean()
        
        risk = df_ai.apply(_compute_risk_proportions, axis=1)
        risk = {
            "mean": risk.mean()
        }
        risk = {key: value.round(4).to_dict() for key, value in risk.items()}
        
        counts.append({
            "model": df_ai["model"].iloc[0],
            "total": comparisons,
            "actual": actual_threats,
            "duplicates": duplicate_threats,
            "threats": threats,
            "mitigations": mitigations,
            "risk_same": risk,
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