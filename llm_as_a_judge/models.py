from openai import OpenAI

models = [
    "microsoft/phi-4-reasoning-plus:free",
    "meta-llama/llama-4-maverick:free",
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-nemo:free",
    "deepseek/deepseek-chat-v3-0324:free"
]

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="microsoft/phi-4-reasoning-plus:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)