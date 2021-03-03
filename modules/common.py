#
# Contains essential and pretty print functions
#

import subprocess
import shutil


def check_for_tool(exec_name):
    if not shutil.which(exec_name):
        print("'{0}' not found. Please install this tool.".format(exec_name))
        exit(1)


def get_output(command):
    return subprocess.check_output(command.split(" ")).decode("UTF-8").strip()

