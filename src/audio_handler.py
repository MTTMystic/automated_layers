from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from .fileio_handler import *
from .macros import *
import pyaudacity as pa

class AudioInfo:
	filename_info_handle = "fn"
	length_info_handle = "len"
	ext_info_handle = "ext"
	num_info_handle = "track_no"

	_filename: ""
	_length = 0
	_ext = ""
	_num = -1

	def as_dict(self):
		return {
			filename_info_handle: self._filename,
			length_info_handle: self._length,
			ext_info_handle: self._ext,
			num_info_handle: track_num
		}

	def __init__(self, filename, length, num):
		self._filename = filename 
		self._length = length
		self._num = num
		self._ext = get_audio_ext(self._filename)

class AudioHandler:
	_current_audios_info = {}
	_audio_dirp = ""

	#modularity in case i want to do more in registering an audio 
	def load_audio(self):
		for idx, fp in enumerate(self._audio_dirp):
			length = 0
			if 'm4a' in fp:
				length = MP4(fp).info.length
			elif 'mp3' in fp:
				length = MP3(fp).info.length
			info = AudioInfo(fp, length, idx)
			self._current_audios_info[fp] = info

	def import_files(self):
		for audio_fn in self._current_audios_info.keys():
			audio_fp = get_audio_fullp(audio_fn)
			import_macro = Macros.import2.value.format(audio_fp)
			pa.do(import_macro)

	def get_audio_info(self, fn):
		return self._current_audios_info[get_basename(fn)].as_dict()

	def get_audio_fullp(self, audio_fp):
		return os.path.join(os.path.abspath(self._audio_dirp), audio_fp)

	def __init__(self, audio_list_dirp):
		self._audio_dirp = audio_list_dirp
		self.load_audio()
	

