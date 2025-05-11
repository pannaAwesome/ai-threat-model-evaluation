import os
import ast
import re
from openai import OpenAI
from llm_as_a_judge.prompts import SYSTEM_PROMPT

class LLMJudge:
    def __init__(self, model):
        self.model = model
        api_key=os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def _get_completion(self, assets, prompt):
        # Call the OpenAI API to get the completion
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(assets=assets)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            seed=42
        )
        
        return completion
    
    def _extract_answer(self, completion_message):
        # Extract the JSON object as a dict from the completion message
        # Find actual answer in message starting from { and ending with }
        pattern = r'\{(?:[^{}]*|(?R))*\}'
        answer = re.findall(pattern, completion_message)

        if not answer:
            return None
        
        # Parse the JSON object
        answer = answer[-1]
        answer = answer.replace("'", '"')
        answer = ast.literal_eval(answer)
        return answer
        
    def judge(self, assets, prompt):
        for try_idx in range(3):
            try:
                # Call the OpenAI API to get the completion
                completion = self._get_completion(assets, prompt)
                answer = self._extract_answer(completion.choices[0].message.content)
                return answer
            except Exception as e:
                print(f"Attempt {try_idx + 1} failed")
                if try_idx == 2:
                    raise