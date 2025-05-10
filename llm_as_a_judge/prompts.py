
def build_threat_prompt(assets: list, candidate1: dict, candidate2: dict) -> str:
    """
    Build a prompt for the LLM to evaluate if two threats are the same.
    
    Args:
        candidate1 (dict): The first candidate's information.
        candidate2 (dict): The second candidate's information.
        Structure of dicts:
            {
                "ID": int,
                "Category": <str>,
                "Asset": <str>,
                "Threat": <str>
            }
    
    Returns:
        str: The formatted prompt for the LLM.
    """
    prompt = f"""
        Please act as an impartial judge and evaluate the similarity of two threats provided from
        two different threat models. Two threats are considered the same if they apply to the same asset(s),
        have the same threat category, and their description describes the same malicious objective and
        impact.
        
        For this task, you will be provided with two candidates, each representing a potential threat.
        Each candidate will include the following information:
        - Category: The category of the threat.
        - Asset: The asset that the threat targets. 
        - Threat: A description of the threat itself.
        For some of the candidates, the asset may be empty. In this case, you should defer the asset from
        the threat description.
        
        The Category can be either of: Spoofing, Tampering, Repudiation, Information Disclosure, 
        Denial of Service, Elevation of Privilege.
        The Asset can be either of: {assets}.
        
        [First Candidate]
        Category: {candidate1["Category"]}
        Asset: {candidate1["Asset"]}
        Threat: {candidate1["Threat"]}
        
        [Second Candidate]
        Category: {candidate2["Category"]}
        Asset: {candidate2["Asset"]}
        Threat: {candidate2["Threat"]}
        
        Please answer with 'yes' if the two threats are the same, and 'no' if they are not.
        If you are not sure, please answer with 'NA'.
        Please provide a brief explanation of your answer.
        Your answer should be in the following format:
        {
            'Answer': <yes/no/NA>,
            'Threat1': {candidate1['ID']},
            'Threat2': {candidate2['ID']},
            'Explanation': <your explanation here>
        }
        Please do not include any other information in your answer.
    """
    
    return prompt