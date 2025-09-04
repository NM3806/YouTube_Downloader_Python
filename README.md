# 🎬 YouTube Video Downloader

> A clean, modern desktop app for downloading YouTube videos and audio with ease.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## ✨ What it does

- **📥 Download videos** in the best quality available
- **🎵 Extract audio** and save as MP3 files  
- **👀 Preview content** before downloading
- **📊 Track progress** with real-time stats
- **📁 Choose where to save** your downloads

## 🖼️ Interface

Clean and intuitive design featuring:
- Simple URL input
- Video preview with thumbnail
- One-click download buttons
- Live progress tracking
- Custom folder selection

---

## 🚀 Quick Start

### What you need
- **Python 3.12.6** 
- **FFmpeg** (for video processing)

### Installation

**1. Get the code**
```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

**2. Install FFmpeg**

<details>
<summary>📋 Click to see installation instructions</summary>

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to your system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

</details>

**3. Set up Python**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements  
pip install -r requirements.txt
```

**4. Run the app**
```bash
python main.py
```

---

## 💡 How to use

1. **Paste a YouTube URL** into the input field
2. **Click "Fetch Info"** to preview the video (optional)
3. **Choose your download folder** (optional)
4. **Pick your format:**
   - `Download Best Video+Audio` → Full video as MP4
   - `Download Audio (MP3)` → Audio only
5. **Watch the progress** and wait for completion!

---

## 🛠️ Technical Details

### Built with
- **GUI Framework:** CustomTkinter (modern UI)
- **Download Engine:** yt-dlp (reliable & fast)
- **Image Processing:** Pillow (thumbnails)
- **HTTP Requests:** requests

### File structure
```
youtube-downloader/
├── main.py           # Main application
├── requirements.txt  # Dependencies
└── README.md        # This file
```

---

## ❓ Having issues?

<details>
<summary><strong>🚫 "FFmpeg not found" error</strong></summary>

- Make sure FFmpeg is installed
- Check it's added to your system PATH
- Restart your terminal after installing
</details>

<details>
<summary><strong>📱 Download fails</strong></summary>

- Check your internet connection
- Some videos might be private or restricted
- Update yt-dlp: `pip install --upgrade yt-dlp`
</details>

<details>
<summary><strong>🖥️ GUI doesn't show</strong></summary>

- Make sure tkinter is installed (comes with Python)
- On Linux: `sudo apt-get install python3-tk`
</details>

---

## ⚖️ Important Notice

**For personal use only.** Please respect:
- YouTube's Terms of Service
- Copyright laws
- Content creators' rights

This tool is for educational purposes. Use responsibly.

---

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature-name`
5. Open a Pull Request

---

## 📋 Roadmap

- [ ] Playlist downloads
- [ ] Quality selection (4K, 1080p, etc.)
- [ ] Download queue
- [ ] Dark/light theme toggle
- [ ] Subtitle downloads

---

## 💬 Support

Need help? 
- Check [existing issues](https://github.com/yourusername/youtube-downloader/issues)
- Create a [new issue](https://github.com/yourusename/youtube-downloader/issues/new)
- Include your OS, Python version, and error details

---

<div align="center">

**Made with ❤️ for the community**

[⭐ Star this repo](# "Star on GitHub") • [🐛 Report bug](# "Report an issue") • [💡 Request feature](# "Request a feature")

</div>