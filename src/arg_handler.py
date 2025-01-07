from .globals import *
import sys
import shutil
import os
sys.path.append('./batch_packer/src/')
from constants import input_dir_arg_prefix

def get_arg_prefix(arg_cml):
    return arg_cml.split(arg_eq_sym)[0]

def typo_in_arg(user_input, arg_prefix):
    missing_eq_sym = arg_eq_sym not in user_input
    prefix_end_before_eq_sym = -(len(arg_eq_sym))
    arg_name = arg_prefix[0:prefix_end_before_eq_sym]
    incorrect_prefix = get_arg_prefix(user_input) != arg_name
    if (missing_eq_sym or incorrect_prefix):
        print("missing eq or incorrect prefix for ", user_input)
        print("correct arg name is ", arg_name)
        print("actual prefix was", get_arg_prefix(user_input))
    return missing_eq_sym or incorrect_prefix

def get_arg_val(arg_cml):
    return arg_cml.split(arg_eq_sym)[1]

def process_args(user_args):
	input_dir_cml = None if len(user_args) < 1 else user_args[0]
	batch_size_cml = None if len(user_args) < 2 else user_args[1]
	auto_amp_cml = None if len(user_args) < 3 else user_args[2]


	typo_input_dir = typo_in_arg(input_dir_cml, input_dir_arg_prefix) if input_dir_cml else False
	typo_batch_size = typo_in_arg(batch_size_cml, batch_size_arg_prefix) if batch_size_cml else False
	typo_auto_amp = typo_in_arg(auto_amp_cml, auto_amp_arg_prefix) if auto_amp_cml else False

	invalid_auto_amp = int(get_arg_val(auto_amp_cml)) > auto_amp_limit if auto_amp_cml else False
	invalid_batch_size = int(get_arg_val(batch_size_cml)) > batch_size_limit if batch_size_cml else False
	args_invalid = (not input_dir_cml) or typo_input_dir or typo_auto_amp or typo_batch_size\
	                or invalid_auto_amp or invalid_batch_size
	if args_invalid:
	    args = [f"\"{input_dir_arg_prefix}\"[folder path]", f"\"{batch_size_arg_prefix}\"[int <= {batch_size_limit}](optional)", f"\"{auto_amp_arg_prefix}\"[int <= {auto_amp_limit}](optional)"]
	    args_list_str = " ".join(args)
	    cml_format = f"(python3) main.py {args_list_str}"
	    print(f"Please call the program as \n {cml_format}")
	    exit()
	#args contains all arguments that were given, including input_dir (mandatory) and non-None (False) args
	args = [get_arg_val(x) for x in [input_dir_cml, batch_size_cml, auto_amp_cml] if x]
	return args
