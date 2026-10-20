import os
from .get_files_info import is_valid_path
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run/execute a python file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to the file to run, relative to the working directory",
                },
                "args": {
                    "type": "list",
                    "description": "list of the arguments that the file will run with, (default is None)",
                },
            },
        },
    },
}


def run_python_file(
working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        valid_target_dir, target_file = is_valid_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
           return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command, text=True, timeout=30, capture_output=True, cwd=working_directory )

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if result.stdout:
            output += f"STDOUT: {result.stdout}"
        if result.stderr:
            output += f"STDERR: {result.stderr}"

        return output

    except Exception as e:
        print(f"   Error: {e}")
