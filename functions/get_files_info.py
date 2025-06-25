import os

def get_files_info(working_directory, directory=None):
    try:
        if directory == None:
            directory = "."
        
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
        
        if not target_dir.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'                                                                          
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for item in os.listdir(target_dir):
            lines.append(f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
        if not lines:
            return "Empty directory"
        return '\n'.join(lines)
    except Exception as e:
        return f"Error: {e}"