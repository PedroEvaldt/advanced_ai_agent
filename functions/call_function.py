from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


func_list = [get_files_info, get_file_content, write_file, run_python_file]
func_dict = {func.__name__: func for func in func_list}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    working_directory = "./calculator"
    function_name = function_call_part.name
    try:
        function = func_dict[function_name]
        function_call_part.args["working_dir"] = working_directory
        function_result = function(**function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name} : {e}"},
                )
            ],
        )