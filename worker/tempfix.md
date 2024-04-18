For those having this issue, check your asr.py file and ensure at line 322 that after "suppress_numerals": False, that you have the following three lines
"max_new_tokens": None, "clip_timestamps": None, "hallucination_silence_threshold": None,

For whatever reason I did not have these arguments in mine and it was causing the issue. Adding those solved it. You can also just download and replace your asr.py file with the current one from the repository as the current file has these options in it.


MacOs : /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/whisperx/asr.py