import sys
import shutil
import os
from .globals import *
from .fileio_handler import  *
from .audio_handler import *
from .sanitizer import *
sys.path.append("./batch_packer/src")
from batch_packer import BatchPacker
from constants import *
from enum import Enum
import pyaudacity as pa
class AutoLayer:
	class UserInput(Enum):
		CONTINUE_NEXT_BATCH = 'y'
		EXIT = 'exit'
	
	_batch_dirs = []
	_batch_idx = 0
	
	def _current_batch(self):
		if (self._batch_idx < len(self._batch_dirs)):
			return self._batch_dirs[self._batch_idx]
		else:
			return ""
	
	#TODO filehandler io chain join
	#TODO if not that then see if os has builtin chain path join
	def _current_batch_path(self):
		batch_basep = self._current_batch()
		print(batch_basep)
		return os.path.join(self._active_dir, batch_basep)
		
	def _user_prompt_ready_check(self):
		user_prompt ="\n".join([user_proceed_ready, user_proceed,  user_prompt_exit, unsaved_progress_warning, " : "])
		user_answer = input(user_prompt).lower()
		while not user_answer in self.UserInput:
			user_answer = input(user_prompt_invalid_response).lower()
		if (user_answer is self.UserInput.EXIT):
			#TODO allow user to select which batch to start at and tell them which batch was next
			print("Exit chosen. Your progress will not be saved, and next program execution will start over with first batch")
			return False
		else:
			if not self._finished():
				print("Proceeding to next batch")
			return True
	
	def _finished(self):
		if self._batch_idx > (len(self._batch_dirs) - 1):
			print("There are no more batches to process")
			return True
		return False

	def process_batch(self):
		if validate_batch(self._current_batch()):
			batch_handler = AudioHandler(self._current_batch_path())
		else:
			return False
		self._batch_idx += 1
		return True

	def run(self):
		continue_running = not self._finished()
		while continue_running:
			batch_succeed = self.process_batch()
			if (batch_succeed):
				print("batch processed")
			if (not batch_succeed):
				continue_running = False
			else:
				continue_running = not self._finished() and self._user_prompt_ready_check()
	def _init_sanitizer(self):


	def _init_batcher(self, batch_size):
		self._batcher = BatchPacker(self._active_dir, batch_size)
		self._batcher.gen_batch_all()
		self._batch_dirs = [os.path.join(self._active_dir, x) for x in os.listdir(self._active_dir)]
		print(self._batch_dirs)

	def __init__(self, given_input_dir, given_batch_size=None, given_auto_amp = 0):	
			to_gen_test_dir = given_input_dir.lower() == test_input_cml
			input_dir = generate_test_dir() if to_gen_test_dir else given_input_dir
			valid_input_dir = check_dir(input_dir)
			if (not valid_input_dir):
				print("Layering failed, try again after addressing reported errors (if any).") 
			self._active_dir = os.path.abspath(input_dir)
			batch_size = default_batch_size if not given_batch_size else int(given_batch_size)
			self._init_batcher(batch_size )

			