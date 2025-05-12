import os
import json
import random

from copy import copy
from random import shuffle

from llm_as_a_judge.judge import LLMJudge
from llm_as_a_judge.prompts import HALLUCINATIONS_PROMPT, THREAT_PROMPT, MITIGATION_PROMPT, RISK_PROMPT

ID_TM = "ID"
ASSET_TM = "Asset"
CATEGORY_TM = "Category"
THREAT_TM = "Threat"
MITIGATION_TM = "Mitigation"
RISK_TM = "Risk"

def vote_compare(tm1:list, tm2:list, assets, prompt:str, ai:str) -> list:
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = prompt.format(tm1=tm1, tm2=tm2)
    result = judge.judge(prompt_tm)
        
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

def vote_hallucinations(ai, tm, assets, seed) -> list:    
    
    hallucinations = []
    
    random.seed(seed)
    tm_shuffled = copy(tm)
    shuffle(tm_shuffled)
    
    judge = LLMJudge(ai)

    prompt = HALLUCINATIONS_PROMPT.format(tm=tm, assets=assets)
    result = judge.judge(prompt)
    
    categories = result["categories"]
    assets = result["assets"]

    hallucinations.append({
        "model": ai,
        "categories_ids": [id for (id,_) in categories],
        "categories": categories,
        "asset_ids": [id for (id,_) in assets],
        "assets": assets
    })
    
    return hallucinations

def vote_threats(tm1, tm2, assets, ai, reversed=False) -> list:
    tm1_copy = copy(tm1)
    tm2_copy = copy(tm2)
    
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = THREAT_PROMPT.format(tm1=tm1, tm2=tm2, assets=assets)
    result = judge.judge(prompt_tm)
    
    tm1_both, tm2_both = get_threats_in_both(tm1_copy, tm2_copy, result["same"])
    
    entry = [idx1 if not reversed else idx2 for idx1, idx2 in result["same"]]
    
    return entry, tm1_both, tm2_both

def vote_mitigations(tm1, tm2, ai, reversed=False) -> list:
    tm1_copy = copy(tm1)
    tm2_copy = copy(tm2)
    
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = MITIGATION_PROMPT.format(tm=zip(tm1_copy, tm2_copy))
    result = judge.judge(prompt_tm)
    
    return [idx1 if not reversed else idx2 for idx1, idx2 in result["same"]]

def vote_risks(tm1, tm2, ai, reversed=False) -> list:
    tm1_copy = copy(tm1)
    tm2_copy = copy(tm2)
    
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = RISK_PROMPT.format(tm=zip(tm1_copy,tm2_copy))
    result = judge.judge(prompt_tm)
    
    _, _ = get_threats_in_both(tm1, tm2, result["same"])
    
    return {
        "same": [idx1 if not reversed else idx2 for idx1, idx2 in result["same"]],
        "more": [idx1 if not reversed else idx2 for idx1, idx2 in result["more"]],
        "less": [idx1 if not reversed else idx2 for idx1, idx2 in result["less"]]
    }

def vote(ai, human_tm, ai_tm, assets, reversed=False) -> dict:
    ai_path = f"{os.getcwd()}/llm_as_a_judge/models_to_use.json"
    with open(ai_path, 'r') as ai_file:
        ai_models = json.load(ai_file)
    
    threats = []
    mitigations = []
    risks = []
    
    threat, tm1_both, tm2_both = vote_threats(human_tm, ai_tm, assets, ai, reversed)
    threats.append(threat)
    
    mitigations.append(vote_mitigations(tm1_both, tm2_both, ai, reversed))
    risks.append(vote_risks(tm1_both, tm2_both, ai, reversed))

    return {
        "threats": threats,
        "mitigations": mitigations,
        "risks": risks
    }