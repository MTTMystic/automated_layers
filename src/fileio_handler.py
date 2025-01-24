import sys
import os
import shutil
from .globals import *
import random
import string
from enum import Enum

class err_msgs(Enum):
    does_not_exist = "That {} does not exist"
    invalid_shouldbe = "The {} should be a {}"
    wrong_permissions = "The {} has wrong permissions"
    missing_permissions = "The {} is missing {} permissions"

def get_audio_ext(audio_fn):
    return os.path.splitext(audio_fn)[1][1:]
    #todo check if fn is correct and valid
    #now functionality is priority

def get_basename(fp):
    if os.path.exists(fp):
        return os.path.basename(fp)
    else:
        print()

def generate_test_dir():
        random_char = random.choice(string.ascii_lowercase)
        test_dir_dst = ""
        tries = 0
        while test_dir_dst in os.listdir(test_dir_fp) or tries < len(string.ascii_lowercase):
            test_dir_dst = test_dir_fp_dst.format(random_char)
            tries+=1
        if (tries > len(string.ascii_lowercase)):
            for dirp in os.listdir(test_dir_fp):
                if (dirp != test_dir_fp_orig):
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
        print(err_msgs.does_not_exist.value.format(fp))
        return False

    invalid_should_be_file = os.path.isdir(abspath) and not shouldBeDir
    invalid_should_be_dir = not os.path.isdir(abspath) and shouldBeDir
    wrong_type = invalid_should_be_dir or invalid_should_be_file
    
    if wrong_type:
        correct = "dir" if invalid_should_be_dir else "file"
        print(err_msgs.invalid_shouldbe.value.format(fp, correct))
        return False

    read_access = os.access(abspath, os.R_OK)
    if (not read_access):
     print(err_msgs.missing_permissions.value.format(fp, "read"))
     return False
    #congrats the type and permissions are correct and it literally exists at all!
    return True
    
def check_dir(fp):
        return check_path_basic(fp, shouldBeDir=True)

def check_filetype(fp):
    fn, ext = os.path.splitext(fp)
    return ext[1:] in valid_filetypes

def validate_batch(batch_dirp):
        if (check_dir(batch_dirp)):
            invalid_files = []
            for fp in os.listdir(batch_dirp):
                if not check_path_basic(os.path.join(batch_dirp, fp)):
                    return False

                if not check_filetype(fp):
                    invalid_files.append(os.path.join(get_basename(batch_dirp), get_basename(fp)))
    
            if (len(invalid_files) > 0):
                invalid_files_string = "\n".join(invalid_files)
                print("The following files are invalid: \n" + invalid_files_string)
                print("Valid filetypes are" + " ".join(valid_filetypes))
                return False
            return True
        return False