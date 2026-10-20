import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from prompts import *


def get_api() -> str:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("api key not found")
    return api_key


def print_response(response, args) -> None:
    print("Hello from agent-py!")

    if args.verbose:
        print(f"\nUser prompt: {args.user_prompt}")
        if response.usage is None:
            raise RuntimeError("no usage stuff")
        else:
            print(
                f"\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}"
            )


    print(f"\nResponse: {response.choices[0].message.content}")


def generate_content(client, messages):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0
    )
    return response


def get_messages():
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help= "Enable verbose output")

    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },

        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    return messages, args


def get_client(api_key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    return client
