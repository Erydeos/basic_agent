import os

from functions import *


def main():
    api_key = get_api()
    client = get_client(api_key)
    messages, args = get_messages()
    response = generate_content(client, messages)
    print_response(response, args)


if __name__ == "__main__":
    main()
