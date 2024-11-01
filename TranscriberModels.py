import openai
import whisper
import torch
import sys
import io

def get_model(use_api):
    if use_api:
        return APIWhisperTranscriber()
    else:
        return WhisperTranscriber()

class WhisperTranscriber:
    def __init__(self):
        # Temporarily redirect stderr to suppress tqdm output during model loading
        original_stderr = sys.stderr
        sys.stderr = io.StringIO()  # Redirect stderr to avoid printing progress
        try:
            self.audio_model = whisper.load_model("tiny.en")
        finally:
            sys.stderr = original_stderr  # Restore stderr

        print(f"[INFO] Whisper using GPU: " + str(torch.cuda.is_available()))

    def get_transcription(self, wav_file_path):
        try:
            result = self.audio_model.transcribe(wav_file_path, fp16=torch.cuda.is_available())
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip()

class APIWhisperTranscriber:
    def get_transcription(self, wav_file_path):
        try:
            with open(wav_file_path, "rb") as audio_file:
                result = openai.Audio.transcribe("whisper-1", audio_file)
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip()
