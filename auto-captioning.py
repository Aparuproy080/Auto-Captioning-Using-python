import os,logging,torch,subprocess
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
    """Extract audio from video file."""
    audio_file = video_path[:-4] + ".mp3"
    if not os.path.exists(audio_file):
        logging.info(f"⚗️ Extracting audio from {video_path}")
        
        
        command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",  # Convert to MP3 format
        "-q:a", "2",  # High quality (lower values are better)
        audio_file
        ]
        logging.info(f"Running command: {' '.join(command)}")
        try:   
            subprocess.run(command, check=True)
            logging.info(f"🔊 Audio extracted to {audio_file}")
        except subprocess.CalledProcessError as e:  
            logging.error(f"Error extracting audio: {e}")
            raise
    else:
        logging.info(f"Audio file {audio_file} already exists. Skipping extraction.")
    return audio_file



def generate_captions(audio_path,model_size="base"):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = WhisperModel(model_size, device=device, compute_type="int8")
    logging.info(f"Loading {model} model on {device}...")

    # Load the audio file
    logging.info("Transcribing audio 🎧 ...")
    segments, info = model.transcribe(audio_path,beam_size=5)
    logging.info(f"Detected {info.language} with {info.language_probability:.2f} probability.")
    logging.info("Transcription completed.✅")
    logging.info(f"Transcription took {info.duration:.2f} seconds.")
    # Generate captions
    srt_file= audio_path.replace(".mp3",".srt")
    with open(srt_file,'w') as file:
        for i,segment in enumerate(segments,1):
            file.write(f"{i}\n")
            start_time = format_time(segment.start)
            end_time = format_time(segment.end)
            text = segment.text
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{text}\n\n")
    logging.info(f"Subtitles saved as {srt_file} ✅")
    return srt_file


if __name__ == "__main__":
    video_path = input("Enter the path of your video file:")  # Path to your video file
      # Path to save the extracted audio file
    setup_logging()
    audio_file = extract_audio(video_path)
    srt_file = generate_captions(audio_file)
    logging.info(f"Subtitles saved as {srt_file} ✅")
    logging.info("Auto-captioning process completed. ✅")
    logging.info("Cleaning up temporary files...")  
    os.remove(audio_file)
    logging.info("Temporary files cleaned up. ✅")
    logging.info("Process completed. ✅")
    logging.info("Thank you for using the auto-captioning tool! 🎉")
