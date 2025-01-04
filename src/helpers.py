#!/bin/python3

import subprocess
import sys
import importlib

def install_missing_modules(modules):
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"Module '{module}' is already installed.")
        except ModuleNotFoundError:
            print(f"Module '{module}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
