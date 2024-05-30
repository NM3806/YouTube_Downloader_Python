# YouTube Video Downloader

This is a simple YouTube Video Downloader application built using Python, Tkinter, and the Pytube and Pydub libraries. The application allows you to download YouTube videos and audio files by providing a YouTube link.

## Features

- Download YouTube videos in the highest resolution.
- Download YouTube audio as MP3 files.
- Displays download progress with a progress bar and percentage.

## Prerequisites

- Python 3.x installed on your machine.
- Required Python libraries:
  - `tkinter`
  - `customtkinter`
  - `pytube`
  - `pydub`
  - `ffmpeg` (required by `pydub` for audio conversion)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/youtube-video-downloader.git
   cd youtube-video-downloader
   
2. Install the required Python libraries:

    ```bash
    pip install pytube customtkinter pydub

3. Install ffmpeg for audio conversion:

   - For Windows, download the static build from the FFmpeg website, extract the zip file, and add the bin folder to your system's PATH.

   - For macOS, you can install ffmpeg using Homebrew:
     
     ```bash
       brew install ffmpeg
     
   - For Linux, you can install ffmpeg using your package manager:
  
       ```bash
       sudo apt update
       sudo apt install ffmpeg

## Usage

1. Run the application:

   ```bash
    python app.py

2. Enter the YouTube video link in the input field.

3. Click on the "Download Video" button to download the video or the "Download Audio" button to download the audio as an MP3 file.

4. The download progress will be displayed, and a message will indicate when the download is complete.

## Code Explanation

- downloadVideo(): Function to download the video from the provided YouTube link.
- downloadAudio(): Function to download the audio from the provided YouTube link and convert it to MP3.
- onProgress(): Callback function to update the progress bar and percentage during the download process.
- customtkinter: Custom Tkinter library for creating modern user interfaces.

Enjoy downloading YouTube videos and audio with this simple app!
