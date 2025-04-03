import os
import logging
import torch
import subprocess
from moviepy.editor import AudioFileClip
from faster_whisper import WhisperModel

def format_time(seconds):
    """Convert time in seconds to SRT time format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("auto_captioning.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging is set up.")

def extract_audio(video_path):
    """Extract audio from video file using ffmpeg."""
    audio_file = video_path[:-4] + ".mp3"
    if not os.path.exists(audio_file):
        logging.info(f"⚗️ Extracting audio from {video_path}")
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "2",
            audio_file
        ]
        try:
            subprocess.run(command, check=True)
            logging.info(f"🔊 Audio extracted to {audio_file}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error extracting audio: {e}")
            raise
    else:
        logging.info(f"Audio file {audio_file} already exists. Skipping extraction.")
    return audio_file

def get_audio_duration(audio_path):
    """Get the duration of an audio file using moviepy."""
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()
    return duration

def split_audio(audio_path, chunk_length=1800):  # 30 minutes chunks
    """Splits audio into smaller chunks if longer than chunk_length (in seconds)."""
    command = [
        "ffmpeg", "-i", audio_path, "-f", "segment", "-segment_time",
        str(chunk_length), "-c", "copy", f"{audio_path[:-4]}_%03d.mp3"
    ]
    subprocess.run(command, check=True)
    audio_chunks = [os.path.join(os.path.dirname(audio_path), f) for f in sorted(os.listdir(os.path.dirname(audio_path))) if f.startswith(os.path.basename(audio_path)[:-4]) and f.endswith(".mp3")]
    return audio_chunks

def generate_captions(audio_chunks, model_size="base"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = WhisperModel(model_size, device=device, compute_type="int8")
    logging.info(f"Loading {model_size} model on {device}...")
    srt_file = audio_chunks[0].replace("_000.mp3", ".srt")
    with open(srt_file, 'w') as srt:
        counter = 1
        for chunk in audio_chunks:
            logging.info(f"Transcribing {chunk} 🎧 ...")
            segments, info = model.transcribe(chunk, beam_size=5)
            logging.info(f"Detected {info.language} with {info.language_probability:.2f} probability.")
            for segment in segments:
                srt.write(f"{counter}\n")
                srt.write(f"{format_time(segment.start)} --> {format_time(segment.end)}\n")
                srt.write(f"{segment.text}\n\n")
                counter += 1
            os.remove(chunk)  # Cleanup chunk files after processing
    logging.info(f"Subtitles saved as {srt_file} ✅")
    return srt_file

if __name__ == "__main__":
    setup_logging()
    video_path = input("Enter the path of your video file:")
    audio_file = extract_audio(video_path)
    duration = get_audio_duration(audio_file)
    if duration > 1800:
        audio_chunks = split_audio(audio_file)
    else:
        audio_chunks = [audio_file]
    srt_file = generate_captions(audio_chunks)
    os.remove(audio_file)  # Cleanup original audio
    logging.info("Process completed. ✅")
    