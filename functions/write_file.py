import os

def write_file(working_dir, file_path, content):
    full_path = os.path.abspath(os.path.join(working_dir, file_path))
    working_dir = os.path.abspath(working_dir)
    if not full_path.startswith(working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        dirs = os.path.dirname(file_path)
        os.makedirs(dirs)
    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Cannot create "{full_path}" -> {e}'
