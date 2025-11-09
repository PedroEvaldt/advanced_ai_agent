import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function
from config import MAX_STEPS

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if (len(sys.argv) < 2):
        print("Usage: main.py 'prompt' '--verbose (optional)' ")
        sys.exit(1)

    user_prompt = sys.argv[1]
    
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    
    available_tools = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    
    messages = []
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
    
    for step in range(MAX_STEPS):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_tools],
                system_instruction=system_prompt))
        
        if response.candidates:
            for cand in response.candidates:
                if cand.content:
                    messages.append(cand.content)
                    
        if response.function_calls:
            for func_call in response.function_calls:
                func_response = call_function(func_call, verbose="--verbose" in sys.argv)
                 
                data = func_response.parts[0].function_response.response or {}
                messages.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=func_call.name,
                                response=data
                            )
                        ]
                    )
                )
            continue
            
        elif response.text:
            print(f"-> {response.text}")
            break
    else:
        print("[Agent stopped: max steps reached]")
                        
        
    prompt_tokens_count = response.usage_metadata.prompt_token_count
    response_tokens_count = response.usage_metadata.candidates_token_count
    
    if ("--verbose" in sys.argv):
        print("=======================================\n")
        print(f"Prompt tokens: {prompt_tokens_count}")
        print(f"Response tokens: {response_tokens_count}")
        print("=======================================\n")


if __name__ == "__main__":
    main()
