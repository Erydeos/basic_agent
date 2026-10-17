import os

def get_files_info(working_directory: str, directory: str=".") -> None:
    try:
        work_path = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
        valid_target_dir = os.path.commonpath([work_path, target_dir]) == work_path

        if not valid_target_dir:
            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return

        if not os.path.isdir(target_dir):
            print(f'Error: "{directory}" is not a directory')
            return

        print(f'Success: "{directory}" is within the working directory')
        print(f"Result for '{directory}' directory:")

        print_contents(target_dir)

    except Exception as e:
        print(f"   Error: {e}")


def print_contents(target_dir, depth=""):
    for item in os.listdir(target_dir):
        is_dir = os.path.isdir(f'{target_dir}/{item}')
        print(f"{depth}  - {item}: file_size={os.path.getsize(f"{target_dir}/{item}")}, is_dir={is_dir}")
        if is_dir:
            depth += "    "
            print_contents(f"{target_dir}/{item}", depth=depth)
