from openai import OpenAI
import ast
import re

class LLMJudge:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="not needed"
        )
        
    def _get_completion(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            seed=42
        )
        return completion
    
    def _extract_answer(self, completion_message):
        pattern = r'\{(?:[^{}]|(?<=\\)\}|(?<=\\)\{)*\}'
        answer = re.findall(pattern, completion_message)

        if not answer:
            return None
        
        answer = answer[-1].replace("'", '"')
        answer = ast.literal_eval(answer)
        return answer
        
    def judge(self, prompt):
        for try_idx in range(3):
            try:
                completion = self._get_completion(prompt)
                answer = self._extract_answer(completion.choices[0].message.content)
                return answer
            except Exception as e:
                print(f"Attempt {try_idx + 1} failed: {e}")
                if try_idx == 2:
                    raise
