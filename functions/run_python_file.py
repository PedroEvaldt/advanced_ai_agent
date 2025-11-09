import os
import subprocess
from google.genai import types

def run_python_file(working_dir, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_dir, file_path))
    working_dir = os.path.abspath(working_dir)
    if not full_path.startswith(working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    if args is None:
        args = []
    elif isinstance(args, str):
        args = [args]
    try:
        completed_process = subprocess.run(["python3", full_path] + args, timeout=30, cwd=working_dir, capture_output = True, text=True)
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT: {stdout}")
        if stderr:
            output_parts.append(f"STDERR: {stderr}")
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        if not output_parts:
            return "No output produced."
        final_msg = "\n".join(output_parts)
        return final_msg
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Runs a Python script inside the given working directory with optional arguments. "
        "Captures STDOUT and STDERR, includes exit code if non-zero, and limits execution to 30 seconds."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)