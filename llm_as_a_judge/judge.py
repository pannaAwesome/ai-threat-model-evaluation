from llm_as_a_judge.prompts import build_threat_prompt

def judge_pair(assets: list, candidate1:dict, candidate2:dict, llm, prompt_builder) -> list:
    """
    Judge if two candidates are the same using a language model.

    Args:
        assets (list): List of asset names.
        candidate1 (dict): The first candidate's information.
        candidate2 (dict): The second candidate's information.
        llm: The language model to use for evaluation.

    Returns:
        dict: The result of the evaluation.
    """
    prompt = prompt_builder(assets, candidate1, candidate2)
    response = llm(prompt)
    
    return response

def judge_model(assets:list, ai_threat_model:list, human_threat_model:list, llm) -> list:
    """
    Judge if two threat models are the same using a language model.

    Args:
        assets (list): List of asset names.
        ai_threat_model (list): The AI-generated threat model.
        human_threat_model (list): The human-generated threat model.
        llm: The language model to use for evaluation.

    Returns:
        dict: The result of the evaluation.
    """
    threats = []
    
    for ai_candidate, human_candidate in zip(ai_threat_model, human_threat_model):
        result = judge_pair(assets, ai_candidate, human_candidate, llm, build_threat_prompt)
        threats.append(result)
    
    return threats