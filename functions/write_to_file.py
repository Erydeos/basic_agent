import os
from .get_files_info import is_valid_path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        valid_target_dir, target_file = is_valid_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"   Error: {e}")
