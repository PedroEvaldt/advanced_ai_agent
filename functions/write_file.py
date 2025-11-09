import os
from google.genai import types

def write_file(working_dir, file_path, content):
    full_path = os.path.abspath(os.path.join(working_dir, file_path))
    working_dir = os.path.abspath(working_dir)
    if not full_path.startswith(working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        dirs = os.path.dirname(file_path)
        if dirs:
            os.makedirs(dirs)
    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Cannot create "{full_path}" -> {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file inside the given working directory with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)