from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


#print(get_files_info({'directory': '.'}))
#print(get_files_info({'directory': 'pkg'}))
print(get_file_content({'file_path': 'main.py'}))  # read the contents of main.py
print(write_file({'file_path': 'main.txt', 'content': 'hello'}))  # write 'hello' to main.txt
print(run_python_file({'file_path': 'main.py'}))  # run main.py
print(get_files_info({'directory': 'pkg'}))  # list the contents of the pkg directory
