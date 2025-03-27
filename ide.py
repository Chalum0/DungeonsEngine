import subprocess
import os
import sys

venv_python = os.path.join(sys.prefix, "Scripts", "python.exe")

subprocess.Popen([venv_python, "devinterface/fileExplorer.py"])