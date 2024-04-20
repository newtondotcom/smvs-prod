import whisperx
import gc 
import time
from testdata import datas

device = "cpu"  # "cuda" or "cpu"
batch_size = 8 # reduce if low on GPU mem, before 16
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy), before float16

# medium model is "medium", large model is "large-v2"
tic = time.perf_counter()
model = whisperx.load_model("base", device, compute_type=compute_type)
toc = time.perf_counter()
print("Faster-Whisper model took ", toc - tic, " seconds to load")

def get_transcribe(audio_file, align=False):
    # 1. Transcribe with original whisper (batched)
    tic = time.perf_counter()
    audio = whisperx.load_audio(audio_file)
    tac = time.perf_counter()
    print("Audio splitting took ",tac-tic," seconds")

    tic= time.perf_counter()
    result = model.transcribe(audio, batch_size=batch_size)
    toc = time.perf_counter()
    print("Transcription took ", toc - tic, " seconds")

    if align:
        return result['segments']

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code="fr", device=device)
    tic = time.perf_counter()
    result = whisperx.align(datas, model_a, metadata, audio, device, return_char_alignments=False)
    toc = time.perf_counter()
    print("Alignment took ", toc - tic, " seconds")

    # delete model if low on **GPU** resources
    #gc.collect(); torch.cuda.empty_cache(); del model_a
    
    return result['segments']

