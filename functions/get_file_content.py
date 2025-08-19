import os
from google.genai import types

def get_file_content(working_directory, file_path):

    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)


        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if full_path is inside working_directory
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        # Read the file content, limiting to MAX_CHARS characters
        # If the file is larger, truncate it and indicate truncation in the content
        MAX_CHARS = 10000

        with open(abs_full_path, "r") as file:
            content = file.read(MAX_CHARS)
            leftover = file.read(1)
            if (len(leftover) > 0):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
        required=["file_path"],  # <-- Place it here, with a comma after properties!
    ),
)