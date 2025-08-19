import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)


        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if full_path is inside working_directory
        parent_dir = os.path.dirname(abs_full_path)
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found'


        if not abs_full_path.endswith('.py'):
            return f'Error: "{full_path}" is not a Python file'

        command = ["python", abs_full_path] + args
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                cwd=abs_working_dir, timeout=30, check=False, encoding=None, errors=None, text=True, env=None)

        stdout = result.stdout
        stderr = result.stderr       

        if not result.stdout and not result.stderr:
            print("No output produced.")
        else:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

        output = f"STDOUT: {stdout}\nSTDERR: {stderr}"

        if result.returncode != 0:
            print("Process exited with code", result.returncode)
        else:
            print("Process succeeded")

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrained to the working directory. It requires a file path relative to the working directory. It can also accept command line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of command line arguments to pass to the Python file during execution. This is an optional parameter.",
            ),
        },
        required=["file_path"],  # <-- Place it here!
    ),
)