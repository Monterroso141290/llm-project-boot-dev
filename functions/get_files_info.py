import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        # Check if full_path is inside working_directory
        if not os.path.isdir(full_path):
            raise ValueError(f'Error: "{directory}" is not a directory')

        if not full_path.startswith(working_directory):
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        directory_content = os.listdir(full_path)

        joined_string_details = ""

        for file in directory_content:
            file_string = f"{file}: file_size = {os.path.getsize(os.path.join(full_path, file))} bytes, is_dir={os.path.isdir(os.path.join(full_path, file))}\n"
            joined_string_details += file_string

        return joined_string_details

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        # No 'required' needed here, since it's optional!
    ),
)