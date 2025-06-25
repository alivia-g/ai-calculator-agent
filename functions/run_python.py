import os, subprocess

def run_python_file(working_directory, file_path):
    real_workin_dir = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(real_workin_dir, file_path))
    if not full_path.startswith(real_workin_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(["python3", file_path], timeout=30, capture_output=True, text=True, cwd="calculator")
        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        if not result.stderr and not result.stdout:
            return "No output produced."
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"