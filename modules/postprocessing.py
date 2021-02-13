#
# Functions for performing optimisations after the build or patches.
#

from modules.common import status_print
from modules.common import status_clear

import os
import glob
import hashlib


def optimise_icon_size(prop):
    """
    Remove unmodified icons so they can inherited from the parent theme.
    """
    dest_icon_files = glob.glob(prop.target_dir_icons + "/**", recursive=True)

    print("Removing unmodified icons...")

    def __delete_if_same_file(dest, dest_prefix, new_dest_prefix):
        src = dest.replace(dest_prefix, new_dest_prefix)

        if not os.path.exists(src) or not os.path.exists(dest):
            return False

        if os.path.isdir(src) or os.path.isdir(dest):
            return False

        # Keep files that end with "-panel.svg"
        if dest[-10:] == "-panel.svg":
            return False

        # Keep files that start with "bluetooth-" (#18)
        if os.path.basename(dest)[:4] == "blue":
            return False

        # Keep files that start with "indicator-"
        if os.path.basename(dest)[:9] == "indicator":
            return False

        # Keep files that end with "-panel.svg" (#11)
        if dest[-10:] == "-close.svg":
            return False

        with open(src, "rb") as f:
            src_bin = f.read()
            src_hash = hashlib.md5(src_bin).hexdigest()

        with open(dest, "rb") as f:
            dest_bin = f.read()
            dest_hash = hashlib.md5(dest_bin).hexdigest()

        if src_hash == dest_hash:
            status_print(prop, dest_hash, "." + dest.replace(dest_prefix, ""))
            os.remove(dest)

        return src_hash == dest_hash

    for dest in dest_icon_files:
        __delete_if_same_file(dest, prop.target_dir_icons, os.path.join(prop.src_path, "usr", "share", "icons", prop.base_icon_theme))
    status_clear(prop)

    # Remove dead symlinks and empty directories.
    print("\nCleaning up broken symlinks and empty directories...")
    for path in glob.glob(prop.target_dir_icons + "/**", recursive=True):
        if os.path.islink(path) and not os.path.exists(path):
            status_print(prop, "Removing broken symlink:", "." + path.replace(prop.target_dir_icons, ""))
            os.remove(path)

        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                status_print(prop, "Removing empty directory:", ".{0}/".format(path.replace(prop.target_dir_icons, "")))
                os.rmdir(path)

    status_clear(prop)
    print("Finished cleaning up icons.\n")
