import os
import json
from openai import OpenAI
from llm_as_a_judge.prompts import SYSTEM_PROMPT

class LLMJudge:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def _get_completion(self, assets, prompt, function):
        # Call the OpenAI API to get the completion
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(assets=assets)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            seed=42,
            tools=[function],
            tool_choice={"type": "function", "function": {"name": function["function"]["name"]}},
        )
        
        return completion
        
    def judge(self, assets, prompt, function):
        for try_idx in range(3):
            try:
                # Call the OpenAI API to get the completion
                completion = self._get_completion(assets, prompt, function)
                return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
            except Exception as e:
                print(f"Attempt {try_idx + 1} failed")
                if try_idx == 2:
                    raise