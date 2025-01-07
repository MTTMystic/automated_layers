from .fileio_handler import  *
import sys
import shutil
import os
from .globals import *
from .audio_handler import *
sys.path.append("./batch_packer/src")
from batch_packer import BatchPacker
from constants import *

from enum import Enum

class AutoLayer:

	class UserInput(Enum):
		CONTINUE_NEXT_BATCH = 'y'
		EXIT_LOOP = 'exit'
	
	_batch_dirs = []
	_batch_idx = 0

	current_audios = {}

	def _validate_batch_files(self, batch_dirp):
		if (check_dir_path(batch_dirp)):
			for fp in os.listdir(batch_dirp):
				if not check_filetype(fp):
					return False
			return True
		else:
			print("batch dir could not be validated, see error and correct if possible")
			return False

	def process_batch(self):
		self._current_batch = self._batch_dirs[self._batch_idx]
		if (self._validate_batch_files(self._current_batch)):
			#first step is to load file as audio track
			#TODO mutagen imports and switch should not rely on dev foreknowledge of valid filetypes?
			for audio_fp in os.listdir(self._current_batch):
				audio_full_fp = os.path.join(self._current_batch, audio_fp) 
				audio = load_audio(os.path.abspath(audio_full_fp))
				if (audio is not None):
					self.current_audios[audio_fp] = audio
					#next step is to import the audio track
					
		else:
			print("failed to validate current batch")
			return False

	def _user_prompt_ready_check(self):
		user_prompt = print("\n".join([user_proceed,  user_prompt_exit, unsaved_progress_warning, " : "]))
		user_answer = input(user_prompt).lower()
		
		return user_answer
	
	def exec_loop(self):
		continue_loop = True
		awaiting_user_ready = False
		while continue_loop:
			while awaiting_user_ready:
				print("awaiting user ready")
				user_answer = self._user_prompt_ready_check()
				if user_answer in self.UserInput:
					if user_answer is self.UserInput.EXIT_LOOP:
						continue_loop = False
						continue
					else:
						awaiting_user_ready = False
				else:
					print(user_prompt_invalid_response)
					continue
			print("not awaiting user ready")
			continue_loop = self.process_batch()
			awaiting_user_ready = True
	
	def _init_batcher(self, batch_size):
		self._batcher = BatchPacker(self._active_dir, batch_size)
		self._batcher.gen_batch_all()
		self._batch_dirs = [os.path.join(self._active_dir, x) for x in os.listdir(self._active_dir)]
		print(self._batch_dirs)

	def __init__(self, input_dir, batch_size=None, auto_amp = 0):
		input_dir_fr =  input_dir

		if (input_dir_fr.lower() == test_input_cml):
			print("generate test dir")
			input_dir_fr = generate_test_dir()


		if (check_dir_path(input_dir_fr)):
			self._active_dir = os.path.abspath(input_dir_fr)

			batch_size_fr = default_batch_size
			if (batch_size):
				batch_size_fr = int(batch_size)

			self._init_batcher(batch_size_fr)

		else:
			print("Layering failed, try again after addressing reported errors (if any).") 