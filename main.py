import os
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_to_file import schema_write_to_file
from modules import *

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_to_file,
]

def main():
    #api_key = get_api()
    #client = get_client(api_key)
    #messages, args = get_messages()
    #response = generate_content(client, messages, available_functions)
    #print_response(response, args)

    api_key = get_api()
    client = get_client(api_key)
    messages, args = get_messages()
    response = generate_content(client, messages, available_functions)


    for _ in range(20):
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                if verbose:
                    result_msg = call_function(tool_call, verbose=True)
                else:
                    result_msg = call_function(tool_call)

            if  response.choices[0].message.reasoning:
                messages.append({"role": "Assistant", "content": response.choices[0].message.reasoning})
            messages.append(result_msg)


            response = generate_content(client, messages, available_functions)

        else:
            break

    print_response(response, args)


if __name__ == "__main__":
    main()
