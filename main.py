import os
from functions.get_files_info import schema_get_files_info
from modules import *

available_functions = [
    schema_get_files_info
]

def main():
    api_key = get_api()
    client = get_client(api_key)
    messages, args = get_messages()
    response = generate_content(client, messages, available_functions)
    print_response(response, args)


if __name__ == "__main__":
    main()
