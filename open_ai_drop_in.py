 
import openai

messages = [{"role": "user", "content": "What's an astronomical unit?"}]


client = openai.OpenAI(
    api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # can be anything
    base_url = "http://0.0.0.0:8080/v1" # NOTE: Replace with IP address and port of your llama-cpp-python server
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    max_tokens=512,
    temperature=0
)



print(response)
response_message = response.choices[0].message

print(response_message)