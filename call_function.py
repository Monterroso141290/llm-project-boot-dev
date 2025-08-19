import os
import subprocess
from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.get_files_info import schema_get_files_info, get_files_info
from config import WORKING_DIR  # Assuming we have a config.py with WORKING_DIR defined

def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content
    }

    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = WORKING_DIR  # Assuming the working directory is "calculator"

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if function_name in functions_dict:
        function_to_call = functions_dict[function_name]
        try:
            result = function_to_call(**function_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ]
            )
        except Exception as e:
            return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing {function_name}: {e}"},
                )
            ],
        )
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

