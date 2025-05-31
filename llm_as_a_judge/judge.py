from openai import OpenAI, OpenAIError
import ast
import re
import os

class LLMJudge:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(
            base_url=os.getenv("OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_API_KEY")
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
        completion_message_lower = completion_message.lower()
        
        # Check for JSON
        answer = re.findall(r'\{(?:[^{}]|(?<=\\)\}|(?<=\\)\{)*\}', completion_message_lower)
        if answer:
            answer = answer[-1].replace("'", '"')
            answer = ast.literal_eval(answer)
            if type(answer["answer"]) is int:
                return answer

        # Check for 0 or 1 (standalone, not part of a bigger number)
        answer = re.findall(r'\b[01]\b', completion_message_lower)
        if answer:
            return {"answer": int(answer[-1])}

        # Check for same or similar
        if any(word in completion_message_lower for word in ["same", "similar"]):
            return {"answer": 1}
        
        # Check for yes or no
        if any(word in completion_message_lower for word in ["yes"]):
            return {"answer": 1}

        raise ValueError(completion_message)
        
    def judge(self, prompt):
        for try_idx in range(3):
            try:
                completion = self._get_completion(prompt)
                answer = self._extract_answer(completion.choices[0].message.content)
                return answer
            except OpenAIError as e:
                print(f"[WARN] Attempt {try_idx + 1} failed: {e}")
                if try_idx == 2:
                    print(f"[ERROR] Failed to retrieve answer from {self.model}")
                    raise
