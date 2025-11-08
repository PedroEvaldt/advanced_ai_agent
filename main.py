import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if (len(sys.argv) != 2):
        print("Usage: main.py 'prompt'")
        sys.exit(1)
    contents = sys.argv[1]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=contents)
    print(response.text)
    prompt_tokens_count = response.usage_metadata.prompt_token_count
    response_tokens_count = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens_count}")
    print(f"Response tokens: {response_tokens_count}")

if __name__ == "__main__":
    main()
