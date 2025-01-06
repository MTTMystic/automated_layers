# automated_layers
A new and improved version of the (old) 'automated_mixer' pyaudacity utility designed for submakers

The prior version was 'naive' (in terms of understanding the most efficient use of Audacity macros with pyaudacity, or anticipating common use-cases for sub layering and mixing) and a bit janky. This was in part from Audacity's known errors with mod-pipe named r/w pipes (at least on Windows? or supposedly in connection to running from IDE?) 

This version's program flow is intended as follows:

- input folder of files - pre-batch using utility file-batcher
- for each batch (subdir):
	- validate audio ext of each file (dev choice of terminate when invalid or ignoring invalid files)
	- load files as audio with mutagen to get track lengths
	- import files into audacity
	- for each track:
		- repeat until track >= longest track
		- trim excess beyond initial longest track length
		- auto-norm / loudness norm (both?)
	- optional user input: auto-amplify (by neg number) to lower track volumes before mixing as one layer

Possible extensions:
	- allow user to specify target length intended and fit tracks to that length using change tempo
	