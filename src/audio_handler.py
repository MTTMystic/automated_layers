from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from .fileio_handler import *
from .macros import *
import pyaudacity as pa
from enum import Enum
#TODO make this a user given value
default_target = 60

class AudioInfoProperties(Enum):
		filename =  "fn"
		length =   "len"
		ext = "ext"
		num = "track_no"

class AudioInfo:
	filename_handle = AudioInfoProperties.filename.name
	length_handle = AudioInfoProperties.length.name
	ext_handle = AudioInfoProperties.ext.name
	num_handle = AudioInfoProperties.num.name

	_filename: ""
	_length = 0
	_ext = ""
	_num = -1

	def get_subproperties(self, req_props):
		props_dict = {}
		all_props_dict = self.as_dict()
		for req_prop in req_props:
			props_dict[req_prop] = all_props_dict[req_prop]

		return props_dict
		
		"""
		if self.handles.filename_info_handle in requested_properties:
			properties_dict[self.handles.filename_info_handle] = self._filename
		elif self.length_info_handle in requested_properties:
			properties[self.handles.length.filename_info_handle] = self._length
		elif self.ext_info_handle in requested_properties:
			properties.append(self._ext)
		elif self.num_info_handle in requested_properties:
			properties.append(self._num)	
		return properties
		"""
		
	def as_dict(self):
		properties_dict = {
			AudioInfo.filename_handle: self._filename, 
			AudioInfo.length_handle: self._length, 
			AudioInfo.ext_handle: self._ext, 
			AudioInfo.num_handle: self._num}
		return properties_dict
	
	def __init__(self, filename, length, num):
		self._filename = filename
		self._length = length
		self._num = num
		self._ext = get_audio_ext(self._filename)

class AudioHandler:
	_current_audios_info = {}
	_audio_dirp = ""

	def _rename_audio_as_num(self, orig_path, num):
		#check for non-ascii characters
		new_name = ".".join(str(num), get_audio_ext(orig_path))
		new_dst = os.path.join(os.path.abspath(os.path.pardir(orig_path), new_name))
		
	#modularity in case i want to do more in registering an audio 
	def load_audio(self):
		for idx, fp in enumerate(os.listdir(self._audio_dirp)):
			#print(fp)
			audio_full_fp = self.get_audio_fullp(fp)
			length = 0
			if get_audio_ext(fp) == 'm4a':
				length = MP4(audio_full_fp).info.length
			elif get_audio_ext(fp) == 'mp3':
				length = MP3(audio_full_fp).info.length
			info = AudioInfo(fp, length, idx)
			self._current_audios_info[fp] = info

	def import_files(self):
		for audio_fn in self._current_audios_info.keys():
			audio_fp = self.get_audio_fullp(audio_fn)
			#print(audio_fp)
			import_macro = Macros.import2.value.format(audio_fp)
			print(import_macro)
			pa.do(import_macro)
	
	def change_tempo(self, orig, target):
		percent_change = ((orig - target) / orig) * 100
		percent_change = '%.2f'%(percent_change)
		tempo_macro = Macros.tempo_change.value.format(str(percent_change))
		#print("percent change is %.2f with original length %.2f and target length %.2f", percent_change, orig, target)
		#print(tempo_macro)
		#pa.do(tempo_macro)
			
	
	def change_tempo_all(self, target):
		for idx, audio_fn in enumerate(self._current_audios_info.keys()):
			sel_macro = Macros.track_sel.value.format(str(idx), "Add")
			pa.do(sel_macro)
			len_num_dict = self._current_audios_info[audio_fn].get_subproperties([AudioInfo.length_handle, AudioInfo.num_handle])
			if (len_num_dict[AudioInfo.length_handle] > target):
				print("track no: {}".format(len_num_dict[AudioInfo.num_handle]))
				self.change_tempo(len_num_dict[AudioInfo.length_handle], target)
			sel_macro - Macros.track_sel.value.format(str(idx), "Remove")	
	
	def get_audio_info(self, fn):
		return self._current_audios_info[get_basename(fn)].as_dict()

	def get_audio_fullp(self, audio_fp):
		return os.path.join(os.path.abspath(self._audio_dirp), audio_fp)
		#return os.path.join(self._audio_dirp, audio_fp)

	def __init__(self, audio_list_dirp):
		self._audio_dirp = audio_list_dirp
		self._current_audios_info = {}
		#print(audio_list_dirp)
		pa.do("New")
		self.load_audio()
		self.import_files()
		#self.change_tempo_all(default_target)
