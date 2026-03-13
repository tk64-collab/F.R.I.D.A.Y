from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(question, conversation_history, model="gpt-4o"):
    conversation = [{"role": "system", "content": "You are a dependable secretary. You are basically serious, but sometimes you joke."}]
    for i, text in enumerate(conversation_history):
        role = "user" if i % 2 == 0 else "assistant"
        conversation.append({"role": role, "content": text})

    conversation.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=model,
        messages=conversation,
        max_tokens=150
    )

    return response.choices[0].message.content