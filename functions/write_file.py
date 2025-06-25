import os

def write_file(file_name, content, directory="", working_directory="./calculator", **kwargs):
    try:
        # Compute the full path
        if directory:
            path = os.path.join(working_directory, directory, file_name)
        else:
            path = os.path.join(working_directory, file_name)
        # Prevent writing outside the calculator directory
        if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_name}" as it is outside the permitted working directory'
        # Ensure the directory exists
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to \"{file_name}\" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"