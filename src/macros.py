from enum import Enum

class Macros(Enum):
	import2 = 'Import2: Filename={}'
	tempo_change = 'ChangeTempo: Percentage=\"{%.2f}\"'
	track_sel= 'SelectTracks: Track="{}" Mode="{}" TrackCount=1'
	track_sel_start_to_end = 'SelTrackStartToEnd'