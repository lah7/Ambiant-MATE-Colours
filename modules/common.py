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


def validate_colour_hex(value):
    if not value.startswith("#") or not len(value) == 7:
        return False

    try:
        int(value[1:7], 16)
    except ValueError:
        return False

    return True
