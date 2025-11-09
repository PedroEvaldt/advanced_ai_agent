import os
from google.genai import types

def get_files_info(working_dir, directory="."):
    directory = os.path.join(working_dir, directory)
    directory = os.path.abspath(directory)
    working_dir = os.path.abspath(working_dir)
    print_msg = f"Result for {directory if directory.endswith(".") else "current"} directory:\n"
    if not directory.startswith(working_dir):
        print_msg += f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        return print_msg
    if not os.path.isdir(directory):
        print_msg += f'Error: "{directory}" is not a directory\n'
        return print_msg
    for f in os.listdir(directory):
        file_path = os.path.join(directory, f)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        file_msg = f"- {f}: file_size={file_size} bytes, is_dir={is_dir}\n"
        print_msg += file_msg
    return print_msg

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)