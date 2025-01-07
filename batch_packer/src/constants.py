test_dir = "batcher_test"
gen_step = "step"
gen_all = "all"
gen_modes = [gen_step, gen_all]
arg_eq_sym = "="
input_dir_arg_prefix = f"input_dir{arg_eq_sym}"
gen_mode_arg_prefix = f"gen_mode{arg_eq_sym}"
batch_size_arg_prefix = f"batch_size{arg_eq_sym}"
batch_size_limit = 30
gen_mode_default = "all"
placeholder = "$"
batch_dir_base = "batch"
batch_dir_name_prefix = batch_dir_base + "_"
batch_dir_path_base = batch_dir_base + placeholder
default_batch_size = 15
wildcard_sym = "*"