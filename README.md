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

### 01-08-2025
- sophisticated redesign of test_dir auto generation for instrumented tests by ensuring duplicate items are removed and upon exhausting alphabet (for dir names) other folders besides test_dir_orig will be auto-deleted
- finish function ensures no re-batching or re-prompting of user to continue batching after all batches have been processed
- loop stops execution after all batches processed and fixed bug of ternary and double-print (using input and print, erroneously, in recursive call) causing input failing to be processed as correct/incorrect
- finally completed user prompt loop in coherent fashion without use of extraneous messages or reporting and with proper sequence (A point of headache before debugging mentioned and finish function)
- renamed exec loop to run
- validation of what files are in each batch per-batch (optimization)
- audio loading storage of track length. experimental, as audacity may start a fit if special non-ascii characters are in files imported (even though manual import in audacity interface does not typically throw errors) and require renaming -- but specific investigation of this may reveal prior version's renaming effort is unecessary. If otherwise I will have to store the fp of the original audio track to use as a track label in addition to the length, so that the user can correlate each track to which file was imported rather than useless data of tracks named "0" or "a" etc.
- in future consider design (not planned feature atm) of allowing user to specify whether to process next batch in a new window or same window


next steps are to implement macro functions using a macro factory for formatting (possibly a file with macro formatted strings) and use macro handler to provide functionality for features such as repeater, auto trim, auto layer and auto-amplify

ultimately the goal is to ensure if user wants to layer any subliminal affirmations (different affirmations if split into multiple sections or files for one subliminal created from scratch) all layers can be adjusted to same length with repeater, and automatically corrected if repeats exceed original length by auto-trim

additionally as this is a revamp I don't intend yet to implement auto-tempo features to adjust tempo to shorter lengths - this is such that automatically the longest length of any audio track is what will be selected and not the shortest or a user target