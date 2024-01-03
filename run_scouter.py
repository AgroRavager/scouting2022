#! /usr/bin/env python
"""
This script starts the Flask server.

The IP address of the Flask server can be passed as an optional
command line. If no IP address is passed, the script assumes you are
doing development work and runs the server on 127.0.0.1.

Example:
python run_scouter.py 192.168.1.1
"""
import os
import sys


def main():
    address = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    cwd=os.path.realpath(os.getcwd())
    servpath=cwd+"/scouter"
    os.environ["PYTHONPATH"] = servpath 
    os.system(f"python scouter/main.py {address}")

if __name__ == "__main__":
	main()
