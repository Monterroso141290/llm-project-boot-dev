import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.get_files_info import schema_get_files_info, get_files_info
# Load environment variables from .env file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of files
- Write to files
- Run Python files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



def main():

    print("DEBUG: main() started")
    print(f"DEBUG: sys.argv = {sys.argv}")

    # We check if the user initialized the project with a prompt of if its empty
    if len(sys.argv) < 2:
        print("Error: No prompt provided!")
        print("Usage: python main.py \"Your prompt here\"")
        sys.exit(1) 

    prompt = sys.argv[1]  # Move this inside main()
    verbose = "--verbose" in sys.argv
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    print("Hello from llm-project-boot-dev!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    print(f"API key loaded: {api_key is not None}")
    print(f"API key length: {len(api_key) if api_key else 0}")
    
    if not api_key:
        print("Error: API key not found!")
        return

    client = genai.Client(api_key=api_key)

    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        except Exception as e:
            print(f"Error during API call: {e}")
            continue

        for candidates in response.candidates:
            messages.append(candidates.content)

        if "--verbose" in sys.argv:
            print(f"User prompt: {prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        print("Response:")

        if response.function_calls:
            verbose = "--verbose" in sys.argv
            function_responses = []
            
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                function_responses.append(function_call_result.parts[0])

            #We check if the result is valid
                if not function_call_result.parts or not function_call_result.parts[0].function_response:
                    raise Exception(f"empty function call result")

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_responses))            

        else:
            print(f"Final response: {response.text}")
            break
        

if __name__ == "__main__":
    main()

