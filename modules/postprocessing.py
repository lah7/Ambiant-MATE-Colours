#
# Functions for performing optimisations after the build or patches.
#

import os
import glob
import hashlib


def optimise_icon_size(src_dir, new_dir):
    """
    Remove unmodified icons so they can inherited from the parent theme.
    """
    print("\nCleaning up: ", new_dir)

    # Deduplication
    checksums = []
    original_files = glob.glob(src_dir + "/**", recursive=True)
    new_files = glob.glob(new_dir + "/**", recursive=True)

    print("Deduplicating... (1/2)")
    for path in original_files:
        # Can't checksum directories or links
        if os.path.isdir(path) or os.path.islink(path):
            continue

        with open(path, "rb") as f:
            data = f.read()
            data_hash = hashlib.md5(data).hexdigest()
            checksums.append(data_hash)

    print("Deduplicating... (2/2)")
    for path in new_files:
        # Keep files that end with "-panel.svg"
        if path[-10:] == "-panel.svg":
            continue

        # Keep files that start with "bluetooth-" (#18)
        if os.path.basename(path)[:4] == "blue":
            continue

        # Keep files that start with "indicator-"
        if os.path.basename(path)[:9] == "indicator":
            continue

        # Keep files that end with "-panel.svg" (#11)
        if path[-10:] == "-close.svg":
            continue

        # Can't checksum directories or links
        if os.path.isdir(path) or os.path.islink(path):
            continue

        # Perhaps it was recently deleted?
        if not os.path.exists(path):
            continue

        # Perform checksum and delete file if it matches
        with open(path, "rb") as f:
            data = f.read()
            data_hash = hashlib.md5(data).hexdigest()

        if data_hash in checksums:
            os.remove(path)

    # Remove dead symlinks and empty directories.
    print("Cleaning up broken symlinks and empty directories...")
    for path in glob.glob(new_dir + "/**", recursive=True):
        if os.path.islink(path) and not os.path.exists(path):
            os.remove(path)

        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                os.rmdir(path)

    print("Finished cleaning up icons.\n")
