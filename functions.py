import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def get_api() -> str:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("api key not found")
    return api_key


def print_response(response, prompt) -> None:
    print("Hello from agent-py!")

    if response.usage is None:
        raise RuntimeError("no usage stuff")
    else:
        print(
            f"\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}"
        )

    print(f"\nPrompt: {prompt}")
    print(f"\nResponse: {response.choices[0].message.content}")


def generate_content(client, messages):

    response = client.chat.completions.create(
        model="openrouter/free", messages=messages
    )
    return response


def get_messages():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    return messages, args.user_prompt


def get_client(api_key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    return client
