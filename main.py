import sys
from src.arg_handler import process_args
from src.auto_layering import AutoLayer
from src.globals import *

if __name__ == "__main__":
	user_args = sys.argv[1:]
	al_args = process_args(user_args)
	auto_layer_machine = AutoLayer(*al_args)
	auto_layer_machine.run()