import os
from .get_files_info import is_valid_path
import subprocess


def run_python_file(
working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        valid_target_dir, target_file = is_valid_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if file_path[-3:] != ".py":
           return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command, text=True, timeout=30, capture_output=True, cwd=working_directory )

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}"

        return output

    except Exception as e:
        print(f"   Error: {e}")
