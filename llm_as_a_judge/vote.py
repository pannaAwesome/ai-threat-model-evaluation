import os
import json 

from copy import copy
from random import shuffle

from llm_as_a_judge.judge import LLMJudge
from llm_as_a_judge.prompts import HALLUCINATIONS_PROMPT, THREAT_PROMPT, MITIGATION_PROMPT, RISK_PROMPT

def vote_compare(tm1:list, tm2:list, assets, prompt:str, ai:str) -> list:
    judge = LLMJudge(ai)
    
    # Get judging for tm1, tm2
    prompt_tm = prompt_tm.format(tm1=tm1, tm2=tm2)
    result = judge.judge(assets, prompt_tm)
    
    # Get judging for tm2, tm1
    prompt_tm_reverse = prompt_tm_reverse.format(tm1=tm1, tm2=tm2)
    result_reverse = judge.judge(assets, prompt_tm_reverse)
        
    return result, result_reverse

def vote_single(tm:list, assets, prompt:str, ai:str) -> list:
    judge = LLMJudge(ai)
    
    # Judge threat in original order
    prompt_tm = prompt_tm.format(tm=tm)
    result = judge.judge(assets, prompt_tm)
    
    # Judge in randomised order
    tm_shuffled = copy(tm)
    shuffle(tm_shuffled)
    prompt_tm_shuffled = prompt_tm_shuffled.format(tm_shuffled)
    result_shuffled = judge.judge(assets, prompt_tm_shuffled)
        
    return result, result_shuffled

def get_threats_in_both(tm1:list, tm2:list, ids:list, ids_reverse:list) -> list:
    """
    Get elements that are in both list
    """
    tm1_both = []
    tm2_both = []
    ids_both = []
    for (id1,id2) in ids:
        if (id2, id1) in ids_reverse:
            for th in tm1:
                if th["ID"] == id1:
                    threat1 = th
                    break
            for th in tm2:
                if th["ID"] == id2:
                    threat2 = th
                    break
            
            tm1_both.append(threat1)
            tm2_both.append(threat2)
            ids_both.append((id1,id2))
    return tm1_both, tm2_both, ids_both

def vote_hallucinations(tm, assets, ai) -> list:
    # result, result_shuffled = vote_single(tm, assets, HALLUCINATIONS_PROMPT, ai)
    
    result = {"category_list": [(1,"Spoofing"), (2, "Tampering")], "asset_list": [(2,["Server"]), (5,["Server"])]}
    result_shuffled = {"category_list": [(2, "Tampering"), (1,"Spoofing")], "asset_list": [(2,["Server"]), (4,["Hejsa"]), (5,["Server","Hejsa"])]}
    
    categories = list(filter(lambda c: c in result_shuffled["category_list"], result["category_list"]))
    assets = list(filter(lambda a: a in result_shuffled["asset_list"], result["asset_list"]))
    
    return {
        "model": ai,
        "no_cat": len(categories),
        "categories_ids": [id for (id,_) in categories],
        "categories": [category for (_,category) in categories],
        "no_assets": len(assets),
        "asset_ids": [id for (id,_) in assets],
        "assets": [asset for (_,asset) in assets]
    }

def vote_threats(tm1, tm2, assets, ai) -> list:
    #result, result_reverse = vote_compare(tm1, tm2, assets, THREAT_PROMPT, ai)
    result = {"similar_threats": [(1,2), (4,4), (1,1), (3,4), (20,20), (5,10)]}
    result_reverse = {"similar_threats": [(2,1), (4,4), (1,1), (4,3), (10,10)]}
    
    tm1_both, tm2_both, tm_ids = get_threats_in_both(tm1, tm2, result["similar_threats"], result_reverse["similar_threats"])
    no_same = len(tm1_both)
    
    entry = {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": tm_ids
    }
    
    return entry, tm1_both, tm2_both

def vote_mitigations(tm1, tm2, assets, ai) -> list:
    #result, result_reverse = vote_compare(tm1, tm2, assets, MITIGATION_PROMPT, ai)
    result = {"similar_threats": [(1,2), (4,4), (1,1),]}
    result_reverse = {"similar_threats": [(2,1), (4,4), (1,1), (4,3)]}
    
    tm1_both, _, tm_ids = get_threats_in_both(tm1, tm2, result["similar_threats"], result_reverse["similar_threats"])
    no_same = len(tm1_both)
    
    return {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": tm_ids
    }

def vote_risks(tm1, tm2, assets, ai) -> list:
    #result, result_reverse = vote_compare(tm1, tm2, assets, RISK_PROMPT, ai)
    result = {"similar_threats": [(1,2), (4,4), (3,4), (20,20)]}
    result_reverse = {"similar_threats": [(2,1), (4,4), (4,3)]}
    
    tm1_both, _, tm_ids = get_threats_in_both(tm1, tm2, result["similar_threats"], result_reverse["similar_threats"])
    no_same = len(tm1_both)
    
    return {
        "model": ai,
        "no_same": no_same,
        "no_human": len(tm1)- no_same,
        "no_all_human": len(tm1),
        "no_ai": len(tm2)- no_same,
        "no_all_ai": len(tm2),
        "same": tm_ids
    }

def vote(human_tm, ai_tms, assets) -> dict:
    ai_path = f"{os.getcwd()}/llm_as_a_judge/models_to_use.json"
    with open(ai_path, 'r') as ai_file:
        ai_models = json.load(ai_file)
        
    tool_results = {}
    for tool, ai_tm in ai_tms.items():
        hallucinations = []
        threats = []
        mitigations = []
        risks = []
        
        for ai in ai_models:
            hallucinations.append(vote_hallucinations(ai_tm, assets, ai))
            threat, tm1_both, tm2_both = vote_threats(human_tm, ai_tm, assets, ai)
            threats.append(threat)
            
            mitigations.append(vote_mitigations(tm1_both, tm2_both, assets, ai))
            risks.append(vote_risks(tm1_both, tm2_both, assets, ai))
        
        tool_results[tool] = {
            "hallucinations": hallucinations,
            "threats": threats,
            "mitigations": mitigations,
            "risks": risks
        }        
    
    return tool_results