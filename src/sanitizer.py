from enum import Enum
import sys
import os
import shutil

default_sub_char = "_"

class SanitizeMode(Enum):
    SUB_CHAR = "sub" #replace special non-ascii characters with user-defined character
    NUMERIC = "num" #rename filses in dir or single file by a number, in order of its place in the dir

class Sanitizer():
    _mode = "" #which renaming scheme could sanitizer use?
    _in_place = False #should sanitizer rename in place (TRUE) or copy to target dir (FALSE)
    _target_dir = "" #where should renamed file be copied, if not inplace renaming?
    _sub_char = default_sub_char

    def new_fn_numeric(self, fp, num):
        #new dst = parent_dir/new_fn.orig_ext
        #new_fn = num
        pardir = os.path.dirname(fp)
        orig_ext = os.path.splitext(fp)[1]
        new_fn = str(num) + orig_ext
        return new_fn

    def new_fn_subchar(self, fp):
        #new dst = parent_dir/(fp with non-ascii replaced by '_')
        fn, orig_ext = os.path.splitext(os.path.basename(fp))
        pardir = os.path.dirname(fp)
        new_fn = ""
        for char in fn:
            next_char = char
            non_ascii = not char.isascii()
            inappropriate_point = char == "."
            if non_ascii or inappropriate_point:
                next_char = self._sub_char
        
            new_fn += next_char
        return new_fn + orig_ext

    def sanitize(self, fp, idx=0):
        new_fn = self.new_fn_subchar(fp) if self._mode == SanitizeMode.SUB_CHAR.value else self.new_fn_numeric(fp, idx)
        pardir = os.path.dirname(fp) if self._in_place else self._target_dir
        new_fp = os.path.join(pardir, new_fn)
        if not self._in_place:
            shutil.copyfile(fp, new_fp)
        else:
            os.rename(fp, new_fp)
        
    def sanitize_dir(self, dir):
        for idx, fn in enumerate(os.listdir(dir)):
            #print((idx, fn))
            self.sanitize(os.path.join(os.path.abspath(dir), fn), idx)
            #self.sanitize(fn, idx)
    
    def set_numeric(self):
        self._mode = SanitizeMode.NUMERIC.value
    
    def set_sub_char(self, sub_char=default_sub_char):
        self._mode = SanitizeMode.SUB_CHAR.value
        self._sub_char = sub_char
    
    def set_inplace(self, in_place, target_dir=""):
        self._in_place = in_place
        if (not in_place):
            self._target_dir = target_dir

    def __init__(self, mode=SanitizeMode.SUB_CHAR.value, given_sub_char=default_sub_char, in_place=False, target_dir=""):
        self._mode = SanitizeMode.SUB_CHAR.value if mode == SanitizeMode.SUB_CHAR.value else SanitizeMode.NUMERIC.value
        self._in_place = in_place
        self._target_dir = target_dir