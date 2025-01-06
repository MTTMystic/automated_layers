import sys
from src.arg_handler import process_args

if __name__ == "__main__":
	user_args = sys.argv[1:]
	al_args = process_args(user_args)