import os

def get_file_content(working_directory, directory):
    file_path = directory
    try:
        path = os.path.join(working_directory, file_path)
        print(working_directory)
        if not path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        has_ending = False
        ending = f'[...File "{file_path}" truncated at 10000 characters]'
        file_content_string = ""
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) > MAX_CHARS:
                has_ending = True
        if has_ending:
            file_content_string += ending
        return file_content_string
    except Exception as e:
        return f"Error: {e}"