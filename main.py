import os
import tkinter
import customtkinter
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import yt_dlp
import requests
import io
import queue

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- Basic App Setup ---
        self.title("🎬 YouTube Video Downloader")
        self.geometry("700x650")
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- State and Threading ---
        self.save_path = tkinter.StringVar(value=os.getcwd())
        self.ui_queue = queue.Queue()
        self.process_queue() # Start the queue listener

        # --- Main Frames ---
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.preview_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = customtkinter.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)
        
        self.progress_frame = customtkinter.CTkFrame(self)
        self.progress_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        # --- Widgets ---
        # Input Frame
        self.url_label = customtkinter.CTkLabel(self.input_frame, text="Enter YouTube Video Link")
        self.url_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5))
        
        self.link_var = tkinter.StringVar()
        self.link_entry = customtkinter.CTkEntry(self.input_frame, width=350, height=40, textvariable=self.link_var)
        self.link_entry.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="ew")
        
        self.fetch_btn = customtkinter.CTkButton(self.input_frame, text="Fetch Info", command=self.start_fetch_info)
        self.fetch_btn.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        self.clear_btn = customtkinter.CTkButton(self.input_frame, text="Clear", command=self.clear_ui, width=60)
        self.clear_btn.grid(row=1, column=2, padx=(0, 10), pady=5)

        # Preview Frame
        self.video_title = customtkinter.CTkLabel(self.preview_frame, text="Video title will appear here", wraplength=600, font=("Segoe UI", 16, "bold"))
        self.video_title.grid(row=0, column=0, padx=10, pady=(10, 5))

        self.thumbnail_label = customtkinter.CTkLabel(self.preview_frame, text="")
        self.thumbnail_label.grid(row=1, column=0, padx=10, pady=10)

        # Action Frame
        self.folder_btn = customtkinter.CTkButton(self.action_frame, text="Choose Save Folder", command=self.choose_folder)
        self.folder_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.download_btn = customtkinter.CTkButton(self.action_frame, text="Download Best Video+Audio", command=lambda: self.start_download(video=True))
        self.download_btn.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="ew")

        self.audio_btn = customtkinter.CTkButton(self.action_frame, text="Download Audio (MP3)", command=lambda: self.start_download(video=False))
        self.audio_btn.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # Progress Frame
        self.progress_percent = customtkinter.CTkLabel(self.progress_frame, text="", font=("Segoe UI", 16, "bold"))
        self.progress_percent.grid(row=0, column=0, pady=(5, 0))

        self.progress_info = customtkinter.CTkLabel(self.progress_frame, text="", font=("Segoe UI", 12))
        self.progress_info.grid(row=1, column=0)

        self.progressBar = customtkinter.CTkProgressBar(self.progress_frame, width=400)
        self.progressBar.set(0)
        self.progressBar.grid(row=2, column=0, padx=10, pady=10)
        
        self.status_label = customtkinter.CTkLabel(self, text=f"Save location: {os.getcwd()}", wraplength=650)
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        
    def start_fetch_info(self):
        ytlink = self.link_var.get().strip()
        if not ytlink:
            messagebox.showwarning("Warning", "Please enter a YouTube link!")
            return
        
        self.set_ui_state("disabled")
        self.status_label.configure(text="Fetching video info...", text_color="orange")
        threading.Thread(target=self.fetch_info_thread, args=(ytlink,), daemon=True).start()

    def fetch_info_thread(self, ytlink):
        try:
            ydl_opts = {"quiet": True, "skip_download": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(ytlink, download=False)

            title = info.get("title", "Unknown Title")
            self.ui_queue.put(("title", title))
            
            thumbnail_url = info.get("thumbnail")
            if thumbnail_url:
                response = requests.get(thumbnail_url, stream=True)
                img_data = response.content
                pil_image = Image.open(io.BytesIO(img_data))
                ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(320, 180))
                self.ui_queue.put(("thumbnail", ctk_image))
            
            self.ui_queue.put(("status", "Info fetched successfully.", "green"))

        except Exception as e:
            self.ui_queue.put(("error", f"Could not fetch video info.\n{e}"))
        finally:
            self.ui_queue.put(("state", "normal"))
            
    def start_download(self, video=True):
        ytlink = self.link_var.get().strip()
        if not ytlink:
            messagebox.showwarning("Warning", "Please enter a YouTube link!")
            return
            
        self.set_ui_state("disabled")
        self.status_label.configure(text="Preparing to download...", text_color="orange")
        threading.Thread(target=self.download_thread, args=(ytlink, video), daemon=True).start()

    def download_thread(self, ytlink, video=True):
        try:
            ydl_opts = {
                "progress_hooks": [self.progress_hook],
                "outtmpl": os.path.join(self.save_path.get(), "%(title)s.%(ext)s"),
                "quiet": True,
            }
            if video:
                ydl_opts.update({"format": "bestvideo+bestaudio/best", "merge_output_format": "mp4"})
            else:
                ydl_opts.update({"format": "bestaudio", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]})
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ytlink])

            self.ui_queue.put(("success", "Download Completed Successfully!"))
        except Exception as e:
            self.ui_queue.put(("error", str(e)))
        finally:
            self.ui_queue.put(("state", "normal"))
            
    def progress_hook(self, d):
        if d["status"] == "downloading":
            if d.get("total_bytes"):
                percent = d.get("downloaded_bytes", 0) / d.get("total_bytes", 1)
            else:
                percent = 0 # For live streams with unknown size
                
            speed = d.get("_speed_str", "0 KB/s")
            eta_seconds = d.get("eta", 0)
            eta_str = f"{int(eta_seconds // 60):02d}:{int(eta_seconds % 60):02d}" if eta_seconds else "??:??"
            
            self.ui_queue.put(("progress", percent, speed, eta_str))
            
        elif d["status"] == "finished":
            self.ui_queue.put(("progress_finalizing",))

    def process_queue(self):
        try:
            while not self.ui_queue.empty():
                message = self.ui_queue.get_nowait()
                msg_type = message[0]

                if msg_type == "title":
                    self.video_title.configure(text=message[1])
                elif msg_type == "thumbnail":
                    self.thumbnail_label.configure(image=message[1], text="")
                elif msg_type == "status":
                    self.status_label.configure(text=message[1], text_color=message[2])
                elif msg_type == "error":
                    messagebox.showerror("Error", message[1])
                    self.status_label.configure(text="An error occurred.", text_color="red")
                elif msg_type == "success":
                    self.status_label.configure(text="Download Complete! ✅", text_color="green")
                    messagebox.showinfo("Success", message[1])
                elif msg_type == "state":
                    self.set_ui_state(message[1])
                elif msg_type == "progress":
                    percent, speed, eta_str = message[1], message[2], message[3]
                    self.progressBar.set(percent)
                    self.progress_percent.configure(text=f"{percent*100:.1f} %")
                    self.progress_info.configure(text=f"Speed: {speed} ETA: {eta_str}")
                elif msg_type == "progress_finalizing":
                    self.progressBar.set(1.0)
                    self.progress_percent.configure(text="100 %")
                    self.progress_info.configure(text="Merging / Finalizing...")
        
        finally:
            self.after(100, self.process_queue) # Check again in 100ms
            
    def set_ui_state(self, state):
        """Enable or disable all interactive widgets."""
        self.fetch_btn.configure(state=state)
        self.download_btn.configure(state=state)
        self.audio_btn.configure(state=state)
        self.folder_btn.configure(state=state)
        self.link_entry.configure(state=state)
        self.clear_btn.configure(state=state)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)
            self.status_label.configure(text=f"Save location: {folder}", text_color="blue")

    def clear_ui(self):
        self.link_var.set("")
        self.video_title.configure(text="Video title will appear here")
        self.thumbnail_label.configure(image=None, text="")
        self.progressBar.set(0)
        self.progress_percent.configure(text="")
        self.progress_info.configure(text="")
        self.status_label.configure(text=f"Save location: {self.save_path.get()}", text_color="gray50")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()

