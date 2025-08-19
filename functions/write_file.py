import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)


        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'

        # Check if full_path is inside working_directory
        parent_dir = os.path.dirname(abs_full_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)


        with open(abs_full_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{abs_full_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory. It requires a file path relative to the working directory, and the content to write into the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. It is required to be given by the user.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. It is required to be given by the user.",
            ),
        },
        required=["file_path", "content"],  # <-- Place required here and include both!
    ),
)