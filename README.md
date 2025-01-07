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
	- allow user to choose whether the program runs "in place" or uses a working directory copy

## CML Exec

(python3) main.py input_dir=[input_folder_path] batch_size= [int up to 30] auto_amplify=[int up to 35]

auto_amplify=0 means no change in volume level per each track.

## Devlog

### 01-05-2025
First program init and use of batcher.

### 01-06-2025

- extracted arg handler to separate file (based on batch packer, which remains untouched as utility) because it's useful outside the batcher
- extracted check_path_basic from batcher to seperate file (again, untouched in packer) because it's useful outside that class!
- validation_handler anticipated to complete more verification of files and dirs

### 01-07-2025
- renamed validation to fileio_handler
- loads of progress on auto_layering with user input loop (one batch at a time) and beginning phases of loading and processing audio
- frustrated by attempts to install pyaudacity failing thus far, will try again tomorrow as it's a natural stopping point
- slightly modified batch_packer and extracted some of its values to external file for access by auto_layering
- function to auto-generate test disposable directories to use auto_layering infinite amount of times without modifying existing directory (original)
- managing one-batch-at-a-time loading with batch_idx indexing into each batch in active dir after batching complete (all at once before processing each batch)