from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from fileio_handler import 
class Audio:
	_filename: ""
	_audio_info_length = 0
	_audio_info_filetype = ""
	_audio_track_num = -1
	_audio_info_orig = None

	#presume the calling handles the fp being the abspath
	def __init__(self, full_fp, audio_track_number):
		self._filename = s

class AudioHandler:
	_current_audios = {}
	_audio_dir_path = ""

	def validate_audio(self):
		for audio_fp in os.listdir(self._audio_dir_path):
			audio_full_fp = os.path.join(self._audio_list_dir_path, audio_fp) 
			audio = load_audios(os.path.abspath(audio_full_fp))
			if (audio is not None):
				self._current_audios[audio_fp] = int(audio.info.length)
				#next step is to import the audio track
			else:
				print("There was an audio error processing {audio_fp}")
				return False

	def __init__(self, audio_list_dirp):
		self._audio_dirp = audio_list_dirp

def load_audio(audio_fp):
	if 'm4a' in audio_fp:
		return MP4(audio_fp)
	elif 'mp3' in audio_fp:
		return MP3(audio_fp)
	else:
		return None

def Macro_repeat(audio_meta, )