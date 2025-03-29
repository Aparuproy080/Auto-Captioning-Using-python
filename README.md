📜 README.md – Auto-Captioning Tool
markdown
Copy
Edit
# 🎥 Auto-Captioning Tool (Whisper + FFmpeg)

An **AI-powered automatic captioning tool** that extracts audio from a video and generates subtitles (`.srt`) using OpenAI's **Whisper** model. Supports **CUDA (GPU) acceleration** and **CPU-only** mode.

---

## 🚀 Features
✅ **Fast & accurate transcription** using `faster-whisper`  
✅ **Supports multiple Whisper models** (`tiny`, `small`, `base`, etc.)  
✅ **Automatic audio extraction** from video files  
✅ **CUDA support for faster transcription**  
✅ **Subtitles in `.srt` format** with proper timestamps  
✅ **Customizable model & settings via CLI**  

---

## 📦 Installation
### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-username/Auto-Captioning-Using-python.git
cd Auto-Captioning-Using-python
```
### **2️⃣ Install Dependencies**
Make sure you have **Python 3.8+** installed.

```bash
pip install -r requirements.txt 
```
### **3️⃣ Install FFmpeg (Required for audio extraction)**
**Windows**
Download from FFmpeg.org

Add it to your system PATH

**Linux (Ubuntu/Debian)**
```bash

sudo apt update && sudo apt install ffmpeg -y
```
**Mac (Homebrew)**

```bash
brew install ffmpeg
```
🎬 Usage

tiny model is fastest, but less accurate

Use small for a balance of speed & accuracy

For GPU (CUDA) Acceleration
Make sure PyTorch detects GPU:

```python
Copy
Edit
import torch
print(torch.cuda.is_available())  # Should return True
```
The script automatically runs on CUDA (GPU) if available

Use float16 instead of int8 for faster transcription

***📜 Example Output (.srt File)***
rust
Copy
Edit
1
00:00:01,000 --> 00:00:05,500
Hello, and welcome to our AI-based captioning tool.

2
00:00:06,000 --> 00:00:10,000
This tool automatically generates subtitles for your videos.