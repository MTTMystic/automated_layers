import sys
import os
import shutil
from .globals import *
import random
import string

def generate_test_dir():
        random_char = random.choice(string.ascii_lowercase)
        test_dir_dst = ""
        tries = 0
        while test_dir_dst in os.listdir(test_dir_fp) or tries < len(string.ascii_lowercase):
            test_dir_dst = test_dir_fp_dst.format(random_char)
            tries+=1
        if (tries > len(string.ascii_lowercase)):
            for dirp in os.listdir(test_dir_fp):
                if (dirp not test_dir_fp_orig)
                    shutil.rmtree(dirp)
        os.makedirs(test_dir_dst, mode=0o755, exist_ok=True)
        #os.chmod(test_dir_dst, 0o755)
        for filepath in os.listdir(test_dir_fp_orig):
            src_fp = os.path.join(test_dir_fp_orig, filepath)
            os.chmod(src_fp, mode=0o755)
            shutil.copy2(src_fp, test_dir_dst)

        return test_dir_dst

def check_path_basic(fp, shouldBeDir = False):
    abspath = os.path.abspath(fp)
    as_should_be = "dir" if shouldBeDir else "file"
    not_as_should_be = "file" if shouldBeDir else "dir"

    if not os.path.exists(abspath):
        print(f"The specified item at path {fp} does not exist")
        return False

    invalid_type_should_be_file = os.path.isdir(abspath) and not shouldBeDir
    invalid_type_should_be_dir = not os.path.isdir(abspath) and shouldBeDir
    wrong_type = invalid_type_should_be_dir or invalid_type_should_be_file
    if wrong_type:
        print(f"The item at the specified path {fp} is a {not_as_should_be}, not a {as_should_be}")
        return False

    open_access = os.access(abspath, os.X_OK)
    if not open_access:
        print(f"The specified {as_should_be} at path {fp} cannot be opened, check its permissions")
        return False

    read_access = os.access(abspath, os.R_OK)
    if not read_access:
        print(f"The specified {as_should_be} at path {fp} cannot be read, check its permissions")
        return False

    write_access = os.access(abspath, os.W_OK)
    if not write_access:
        print("The specified {as_should_be} at path {fp} cannot be read, check its permissions")
        return False
    #congrats the type and permissions are correct and it literally exists at all!
    return True
    
def check_dir_path(fp):
        return check_path_basic(fp, shouldBeDir=True)

def check_filetype(fp):
    fn, ext = os.path.splitext(fp)
    return ext[1:] in valid_filetypes

