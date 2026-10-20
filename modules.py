import argparse
import json
from operator import call
import os
from tabnanny import verbose

from dotenv import load_dotenv
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_to_file import write_file
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

    response = response.choices[0].message

    if response.tool_calls:
        for tool_call in response.tool_calls:


            if verbose:
                result_msg = call_function(tool_call, verbose=True)
                print(f"-> {result_msg['content']}")
            else:
               result_msg = call_function(tool_call)
               print(result_msg)


    else:
        print(f"\nResponse: {response.content}")


def generate_content(client, messages, tools=[]):

    response = client.chat.completions.create(
        model="gpt-oss:20b",
        messages=messages,
        #temperature=0,
        tools=tools,
    )
    return response


def get_messages(old=None):
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
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    return client


def call_function(tool_call, verbose: bool = False) -> dict:
    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments or "{}")
        id = tool_call.id

        if verbose:
            print(f" - Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")

        function_map = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "write_file": write_file,
            "run_python_file": run_python_file
        }

        if function_name not in function_map:
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown function: {function_name}",
            }

        function_args["working_directory"] = "./calculator"

        result = function_map[function_name](**function_args)

        return {
            "role":"tool",
            "tool_call_id": id,
            "content": result,
        }
    except Exception as e:
        print(f"   Error: {e}")
