from os import path

arg_eq_sym = "="
input_dir_arg_prefix = f"input_dir{arg_eq_sym}"
batch_size_arg_prefix = f"batch_size{arg_eq_sym}"
auto_amp_arg_prefix = f"auto_amp{arg_eq_sym}"
batch_size_limit = 30
auto_amp_limit = 35

test_dir_fp = path.abspath("./test_dirs/")
test_dir_fp_orig = path.join(test_dir_fp, 'test_dir_orig')  
test_dir_fp_dst = path.join(test_dir_fp, "test_dir_{}") 
test_input_cml = "test"

valid_filetypes = ['m4a', 'mp3']


unsaved_progress_warning = "This will not save your progress in processing batches with the auto layer machine"
user_proceed_ready = "Are you ready for the next batch to be imported?"
user_proceed = "Please type y to continue or exit to terminate program execution."
user_prompt_exit = "If you prefer to exit the program, type exit"
user_prompt_invalid_response = "Your response was invalid, try again"

program_finished = "There are no more batches to process"