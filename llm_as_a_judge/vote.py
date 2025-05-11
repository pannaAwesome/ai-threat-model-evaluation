import os
import json 

from copy import copy
from random import shuffle

from llm_as_a_judge.judge import LLMJudge
from llm_as_a_judge.prompts import HALLUCINATIONS_PROMPT, THREAT_PROMPT, MITIGATION_PROMPT, RISK_PROMPT

def vote_compare(tm1:list, tm2:list, assets, prompt:str, ai:str) -> list:
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = prompt.format(tm1=tm1, tm2=tm2)
    result = judge.judge(assets, prompt_tm)
        
    return result

def vote_single(tm:list, assets, prompt:str, ai:str) -> list:
    judge = LLMJudge(ai)
    
    # Judge threat in original order
    tm_shuffled = copy(tm)
    shuffle(tm_shuffled)
    prompt_tm = prompt.format(tm=tm_shuffled)
    result = judge.judge(assets, prompt_tm)
        
    return result

def get_threats_in_both(tm1:list, tm2:list, ids:list) -> list:
    """
    Get elements that are in both list
    """
    tm1_both = []
    tm2_both = []
    for (id1,id2) in ids:
        for th in tm1:
            if th["ID"] == id1:
                tm1_both.append(th)
                break
        for th in tm2:
            if th["ID"] == id2:
                tm2_both.append(th)
                break
    return tm1_both, tm2_both

def vote_hallucinations(tm, assets) -> list:
    ai_path = f"{os.getcwd()}/llm_as_a_judge/models_to_use.json"
    with open(ai_path, 'r') as ai_file:
        ai_models = json.load(ai_file)
    
    hallucinations = []
    for ai in ai_models:
        result = vote_single(tm, assets, HALLUCINATIONS_PROMPT, ai)
        
        categories = result["category_list"]
        assets = result["asset_list"]
    
        hallucinations.append({
            "model": ai,
            "no_cat": len(categories),
            "categories_ids": [id for (id,_) in categories],
            "categories": [category for (_,category) in categories],
            "no_assets": len(assets),
            "asset_ids": [id for (id,_) in assets],
            "assets": [asset for (_,asset) in assets]
        })
    
    return {"hallucinations" : hallucinations}

def vote_threats(tm1, tm2, assets, ai) -> list:
    result = vote_compare(tm1, tm2, assets, THREAT_PROMPT, ai)
    
    tm1_both, tm2_both = get_threats_in_both(tm1, tm2, result["similar_threats"])
    no_same = len(tm1_both)
    
    entry = {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": result["similar_threats"]
    }
    
    return entry, tm1_both, tm2_both

def vote_mitigations(tm1, tm2, assets, ai) -> list:
    result = vote_compare(tm1, tm2, assets, MITIGATION_PROMPT, ai)
    
    tm1_both, _ = get_threats_in_both(tm1, tm2, result["similar_threats"])
    no_same = len(tm1_both)
    
    return {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": result["similar_threats"]
    }

def vote_risks(tm1, tm2, assets, ai) -> list:
    result = vote_compare(tm1, tm2, assets, RISK_PROMPT, ai)
    
    tm1_both, _ = get_threats_in_both(tm1, tm2, result["similar_threats"])
    no_same = len(tm1_both)
    
    return {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": result["similar_threats"]
    }

def vote(human_tm, ai_tms, assets) -> dict:
    ai_path = f"{os.getcwd()}/llm_as_a_judge/models_to_use.json"
    with open(ai_path, 'r') as ai_file:
        ai_models = json.load(ai_file)
        
    tool_results = {}
    for tool, ai_tm in ai_tms.items():
        threats = []
        mitigations = []
        risks = []
        
        for ai in ai_models:
            threat, tm1_both, tm2_both = vote_threats(human_tm, ai_tm, assets, ai)
            threats.append(threat)
            
            mitigations.append(vote_mitigations(tm1_both, tm2_both, assets, ai))
            risks.append(vote_risks(tm1_both, tm2_both, assets, ai))
        
        tool_results[tool] = {
            "threats": threats,
            "mitigations": mitigations,
            "risks": risks
        }        
    
    return tool_results