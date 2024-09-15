import whisperx
import time
import os
from dotenv import load_dotenv

load_dotenv()
env = os.environ.get("ENV")

device = "cpu"  # "cuda" or "cpu"
model = "large-v3"
if env == "dev":
    batch_size = 8  # reduce if low on GPU mem, before 16
    compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy), before float16
else:
    batch_size = 16
    compute_type = "float16"

# medium model is "medium", large model is "large-v2", ligh is "base"
tic = time.perf_counter()
model = whisperx.load_model(model, device, compute_type=compute_type)
toc = time.perf_counter()
print("Faster-Whisper model took ", toc - tic, " seconds to load")


def get_transcribe(audio_file, align=False):
    # 1. Transcribe with original whisper (batched)
    tic = time.perf_counter()
    audio = whisperx.load_audio(audio_file)
    tac = time.perf_counter()
    print("Audio splitting took ", tac - tic, " seconds")

    tic = time.perf_counter()
    result = model.transcribe(audio, batch_size=batch_size)
    toc = time.perf_counter()
    time_transcription = toc - tic
    print("Transcription took ", time_transcription, " seconds")

    if align:
        return result["segments"], time_transcription, 0

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    tic = time.perf_counter()

    langage = result["language"]

    # datas
    result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )
    toc = time.perf_counter()
    time_alignment = toc - tic
    print("Alignment took ", time_alignment, " seconds")

    # delete model if low on **GPU** resources
    # gc.collect(); torch.cuda.empty_cache(); del model_a

    return result["segments"], langage, time_transcription, time_alignment
