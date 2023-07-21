from pathlib import Path
import subprocess

# Python program creating a
# context manager

""" class ContextManager():
	def __init__(self, name, age):
		print('init method called')
		self.name = name
		self.age = age
		
	def __enter__(self):
		print('enter method called')
		print(f'name: {self.name}, age: {self.age}')
		return self
	
	def __exit__(self, exc_type, exc_value, exc_traceback):
		print('exit method called')

with ContextManager("asda", 10) as manager:
	print('with statement block') """


class Test:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

    def _is_string(self) -> bool:
        """Returns True if the name is a string."""
        return isinstance(self.name, str)


""" test = Test("asda")
print(test.name)
print(test._is_string()) """

import subprocess

asda = Path("tests/filea.jpg")


def test():
    return subprocess.run(["taskkill", "/f", "/im", "DB Browser for SQLite.exe"], check=False, capture_output=True).returncode


cmd = ["taskkill", "/f", "/im", "DB Browser for SQLite.exe"]
print(test())
""" if test() == 0:
    print("yes")
else:
    print("no") """

import re

# asda = "dd"
""" if not re.match("^[D-Zd-z]$", asda):
    print(f'"{asda}" is not a valid drive letter (D-Z).')
else:
    print("yes") """
# print(bool(re.match("^[D-Zd-z]$", asda)))

import os


def kill_process_by_name(process_name):
    os.system(f"taskkill /f /im {process_name}.exe")


# kill_process_by_name("Notion")
