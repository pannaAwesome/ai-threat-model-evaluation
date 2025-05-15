import random

from copy import copy
from random import shuffle
from openai import OpenAIError
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from itertools import repeat

from llm_as_a_judge.judge import LLMJudge
from llm_as_a_judge.prompts import CATEGORY_PROMPT, ASSET_PROMPT, THREAT_PROMPT, MITIGATION_PROMPT, RISK_PROMPT
from utils.run_stats import concurrent_progress_monitor

ID_TM = "ID"
ASSET_TM = "Asset"
CATEGORY_TM = "Category"
THREAT_TM = "Threat"
MITIGATION_TM = "Mitigation"
RISK_TM = "Risk"
        
def vote_hallucinations(th, ai, assets):    
    try:
        judge = LLMJudge(ai)
        prompt = CATEGORY_PROMPT.format(tm=th)
        cat = judge.judge(prompt)

        prompt = ASSET_PROMPT.format(tm=th, assets=assets)
        ass = judge.judge(prompt)
        return cat["answer"], th[ID_TM], ass["answer"], th[ID_TM]
    except OpenAIError as e:
        pass
    except Exception as e:
        with open('answer_errors.txt', 'a', encoding='utf-8') as f:
            f.write(f"[HALLUCINATION] AI: {ai}, ID: {th[ID_TM]}, ANSWER: {e}\n")

    return -1, -1, -1, -1

def vote_hallucinations_threaded(ai, tm, assets, seed):
    random.seed(seed)
    tm_shuffled = copy(tm)
    shuffle(tm_shuffled)
    
    category_id = []
    asset_ids = []
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        for category, cat_id, asset, ass_id in executor.map(vote_hallucinations, tm_shuffled, repeat(ai), repeat(assets)):
            if category == 0:
                category_id.append(cat_id)            
            if asset == 0:
                asset_ids.append(ass_id)
    
    return {
        "category": category_id,
        "asset": asset_ids
    }


def vote_threats(th1, th2, ai, assets, reversed):
    try:
        judge = LLMJudge(ai)
        th1_copy = {CATEGORY_TM: th1[CATEGORY_TM], THREAT_TM: th1[THREAT_TM]}
        if ASSET_TM in th1:
            th1_copy[ASSET_TM] = th1[ASSET_TM]
        th2_copy = {CATEGORY_TM: th2[CATEGORY_TM], THREAT_TM: th2[THREAT_TM]}
        if ASSET_TM in th2:
            th2_copy[ASSET_TM] = th2[ASSET_TM]
            
        prompt_tm = THREAT_PROMPT.format(tm1=th1_copy, tm2=th2_copy, assets=assets)
        result = judge.judge(prompt_tm)
        if result["answer"] == 1:
            return th1[ID_TM] if not reversed else th2[ID_TM]
    except OpenAIError as e:
        pass
    except Exception as e:
        with open('answer_errors.txt', 'a', encoding='utf-8') as f:
            f.write(f"[THREAT] AI: {ai}, ID1: {th1[ID_TM]}, ID2: {th2[ID_TM]}, ANSWER: {e}\n")
    return -1

def vote_mitigations(th1, th2, ai, reversed):
    try:
        judge = LLMJudge(ai)
        th1_copy = {MITIGATION_TM: th1[MITIGATION_TM]}
        th2_copy = {MITIGATION_TM: th2[MITIGATION_TM]}
        prompt_tm = MITIGATION_PROMPT.format(tm1=th1_copy, tm2=th2_copy)
        result = judge.judge(prompt_tm)
        
        if result["answer"] == 1:
            return th1[ID_TM] if not reversed else th2[ID_TM]
    except OpenAIError as e:
        pass
    except Exception as e:
        with open('answer_errors.txt', 'a', encoding='utf-8') as f:
            f.write(f"[MITIGATION] AI: {ai}, ID1: {th1[ID_TM]}, ID2: {th2[ID_TM]}, ANSWER: {e}\n")
    return -1
            
def vote_risks(th1, th2, ai, reversed):
    try:
        judge = LLMJudge(ai)
        th1_copy = {RISK_TM: th1[RISK_TM]}
        th2_copy = {RISK_TM: th2[RISK_TM]}
        prompt_tm = RISK_PROMPT.format(tm1=th1_copy, tm2=th2_copy)
        result = judge.judge(prompt_tm)
        
        return result["answer"], th1[ID_TM] if not reversed else th2[ID_TM]
    except OpenAIError as e:
        pass
    except Exception as e:
        with open('answer_errors.txt', 'a', encoding='utf-8') as f:
            f.write(f"[RISK] AI: {ai}, ID1: {th1[ID_TM]}, ID2: {th2[ID_TM]}, ANSWER: {e}\n")
    return -2, -1

def vote_all(ths, assets, ai, reversed=False):    
    result = {
        "threats": -1,
        "mitigations": -1,
        "risks": {
            "same": -1,
            "more": -1,
            "less": -1
        }
    }
    th1 = ths[0]
    th2 = ths[1]
    
    threat_result = vote_threats(th1, th2, ai, assets, reversed)
    result["threats"] = threat_result
    if threat_result != -1:
        mitigation_result = vote_mitigations(th1, th2, ai, reversed)
        result["mitigations"] = mitigation_result
        risk_result, risk_id = vote_risks(th1, th2, ai, reversed)
        if risk_result == 0:
            result["risks"]["same"] = risk_id
        elif risk_result == 1:
            result["risks"]["more"] = risk_id
        elif risk_result == -1:
            result["risks"]["less"] = risk_id
    
    return result

def vote_threats_threaded(tms, assets, ai, reversed=False) -> list:    
    results = {
        "threats": [],
        "mitigations": [],
        "risks": {
            "same": [],
            "more": [],
            "less": []
        }
    }
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        for result in executor.map(vote_all, tms, repeat(assets), repeat(ai), repeat(reversed)):
            if result["threats"] != -1:
                results["threats"].append(result["threats"])
            if result["mitigations"] != -1:
                results["mitigations"].append(result["mitigations"])
            if result["risks"]["same"] != -1:
                results["risks"]["same"].append(result["risks"]["same"])
            if result["risks"]["more"] != -1:
                results["risks"]["more"].append(result["risks"]["more"])
            if result["risks"]["less"] != -1:
                results["risks"]["less"].append(result["risks"]["less"])
                
    return results

