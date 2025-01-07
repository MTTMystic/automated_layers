from mutagen.mp4 import MP4
from mutagen.mp3 import MP3

def load_audio(audio_fp):
	if 'm4a' in audio_fp:
		return MP4(audio_fp)
	elif 'mp3' in audio_fp:
		return MP3(audio_fp)
	else:
		return None