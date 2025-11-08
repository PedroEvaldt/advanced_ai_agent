import os
from functions.config import MAX_CHARS_FILE_CONTENT

def get_file_content(working_dir, file_path):
    full_path = os.path.abspath(os.path.join(working_dir, file_path))
    working_dir = os.path.abspath(working_dir)
    if not full_path.startswith(working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS_FILE_CONTENT)
    overflow_msg = f'[...File "{file_path}" truncated at 10000 characters]'
    final_msg = f"{file_content_string} {overflow_msg if len(file_content_string) >= MAX_CHARS_FILE_CONTENT else ''}"
    return final_msg