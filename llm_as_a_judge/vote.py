
from llm_as_a_judge.judge import LLMJudge


def build_vote_prompt(tm1, tm2, prompt):
    function = {
        "type": "function",
        "function": {
            "name": prompt["name"],
            "description": prompt["description"],
            "parameters": {
                "type": "object",
                "properties": {arg: {"type": "list"} for arg in prompt["output_lists"]}
            },
            "required": prompt["output_lists"]
        }
    }
    
    return prompt["message"].format(tm1=tm1, tm2=tm2), function

def vote(tmss:dict, assets, prompt:dict, model) -> list:
    """
    Vote on the threat models using the judge.
    """
    # Create the judge
    judge = LLMJudge(model)
    
    # Judge threat models
    for tool, tms in tmss.items():
        # Get judging for tm1, tm2
        prompt, function = build_vote_prompt(tms[0], tms[1], prompt)
        # Get the completion from the judge
        result = judge.judge(assets, prompt, function)
        print(f"Found {len(result['similar_threats'])} similar threats")
        
        # Get judging for tm2, tm1
        # Build the prompt
        prompt, function = build_vote_prompt(tms[1], tms[0], prompt)
        # Get the completion from the judge
        result_reverse = judge.judge(assets, prompt, function)
        print(f"Found {len(result['similar_threats'])} similar threats")
        
    return result, result_reverse