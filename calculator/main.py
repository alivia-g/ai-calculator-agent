# main.py

from pkg.calculator import Calculator
from pkg.render import render
import argparse
import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
sys.path.append('.')
from functions.call_function import call_function

def is_math_exp(text):
    # a simple heuristic: if it contains mostly math operators and numbers, vs. natural language words
    math_chars = set("0123456789+-*/().")
    words = ["explain", "how", "does", "fix", "bug", "what", "why", "show"]

    # check if it contains natural language words, then it won't be math
    for word in words:
        if word.lower() in text.lower():
            return False
    
    math_char_count = sum(1 for c in text if c in math_chars or c.isspace())
    return math_char_count / len(text) > 0.7

def main():
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    
    if is_math_exp(expression):
        calculator = Calculator()
        try:
            result = calculator.evaluate(expression)
            to_print = render(expression, result)
            print(to_print)
        except Exception as e:
            print(f"Error: {e}")
    else:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        system_prompt = """
        You are a helpful AI coding agent that MUST use the available functions to complete tasks.

        You have access to these functions:
        - get_files_info: List files and directories 
        - get_file_content: Read file contents
        - run_python_file: Execute Python files
        - write_file: Create or modify files

        When a user asks about code, files, or wants you to analyze something:
        1. ALWAYS start by calling get_files_info to see what files are available
        2. Use get_file_content to read relevant files
        3. Only provide your final answer after you have gathered the necessary information

        Do NOT provide answers without first exploring the available files using your functions.
        """

        if len(sys.argv) < 2:
            print("Error: Prompt required")
            exit(1)

        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

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
            ),
        )
        schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Reads and returns the content of a specified file.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the file to read, relative to the working directory.",
                    ),
                },
                required=["directory"]
            ),
        )
        schema_run_python_file = types.FunctionDeclaration(
            name="run_python_file",
            description="Runs any Python file given its path relative to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the Python file to run, e.g., 'main.py' or 'tests.py'",
                    ),
                },
                required=["file_path"]
            ),
        )
        schema_write_file = types.FunctionDeclaration(
            name="write_file",
            description="Creates or overwrites a file in the given directory with the specified string contents.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(type=types.Type.STRING, description="Where to write the file."),
                    "file_name": types.Schema(type=types.Type.STRING, description="Name of the file to create or overwrite."),
                    "content": types.Schema(type=types.Type.STRING, description="The string contents to write to the file."),
                },
                required=["file_name", "content"]
            ),
        )

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_run_python_file,
                schema_write_file,
            ]
        )

        # create verbose locally
        #parser = argparse.ArgumentParser()
        #parser.add_argument("user_prompt", type=str, help="The prompt or command to process")
        #parser.add_argument('--verbose', action='store_true')
        #args = parser.parse_args()
        #verbose = args.verbose
        verbose = "--verbose" in sys.argv
        user_prompt = " ".join([arg for arg in sys.argv[1:] if arg != "--verbose"])

        #print("available_functions", available_functions)

        # loop 20 times max
        for i in range(0, 20):
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )

            messages.append(response.candidates[0].content)
            
            func_calls_found = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    func_calls_found.append(part.function_call)
            
            if func_calls_found:
                # execute first function call
                func_call = func_calls_found[0]
                result = call_function(func_call, verbose=verbose)
                messages.append(result)

                if verbose:
                    print(f"-> Function result: {result.parts[0].function_response.response}")
            else:
                break  # no function calls found

            if not result.parts[0].function_response.response:
                raise Exception("Fatal error: function call did not return a valid response.")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
                
            if len(sys.argv) == 3:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            if response.function_calls:
                for function_call in response.function_calls:
                    print(f"Calling function: {function_call.name}({function_call.args})")
        print("Final response:")
        print(response.text)

if __name__ == "__main__":
    main()