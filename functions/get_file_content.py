from config import MAX_CHARS
from .get_files_info import is_valid_path
import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists the content file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to list content from, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        valid_target_dir, target_file = is_valid_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'


        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #print(f"\nPrinting: {file_path}\n-----------------------------------------------\n")
        with open(target_file, 'r') as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents

    except Exception as e:
        return f"Error: {e}"
