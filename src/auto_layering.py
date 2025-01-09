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
		EXIT = 'exit'
	
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

	def _update_current_batch(self):
		self._current_batch = self._batch_dirs[self._batch_idx]
		return self._current_batch

	def process_batch(self):
		if (self._validate_batch_files(self._update_current_batch())):
			#first step is to load file as audio track
			#TODO mutagen imports and switch should not rely on dev foreknowledge of valid filetypes?
			for audio_fp in os.listdir(self._current_batch):
				audio_full_fp = os.path.join(self._current_batch, audio_fp) 
				audio = load_audio(os.path.abspath(audio_full_fp))
				if (audio is not None):
					self.current_audios[audio_fp] = int(audio.info.length)
					#next step is to import the audio track
				else:
					print("There was an audio error processing {audio_fp}")
					return False
		else:
			print("failed to validate current batch")
			return False
		self._batch_idx += 1
		return True

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
	
	def run(self):
		"""continue_loop = True
		while continue_loop:
			continue_loop = self.process_batch()
			awaiting_proceed = continue_loop
			while awaiting_proceed:
				user_answer = self._user_prompt_ready_check()
				if user_answer in self.UserInput:
					if user_answer is self.UserInput.EXIT_LOOP:
						continue_loop = False
						awaiting_proceed = False
					else:
						awaiting_proceed = False
				else:
					print(user_prompt_invalid_response)
					continue_loop = False"""
		continue_running = not self._finished()
		while continue_running:
			batch_succeed = self.process_batch()
			if (batch_succeed):
				print("batch processed")
			if (not batch_succeed):
				continue_running = False
			else:
				continue_running = not self._finished() and self._user_prompt_ready_check()
	
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