import os
import tkinter
import customtkinter
from pytube import YouTube
from pydub import AudioSegment

def downloadVideo():
    try:
        ytlink = link.get()
        
        ytObject = YouTube(ytlink, on_progress_callback=onProgress)
        video = ytObject.streams.get_highest_resolution()

        # update instruction to title of the video
        title.configure(text= ytObject.title, text_color="white") 

        # Show progress bar and label
        progressBar.pack(padx=10, pady=10)
        progress_percent.pack()

        video.download()
        
        # Hide progress bar and label after download
        progressBar.pack_forget()
        progress_percent.pack_forget()
        
        status.configure(text="Download Complete! :D", text_color="green")
        print("Download Complete! :D")
    
    except Exception as e:
        status.configure(text=f"Error: {str(e)}", text_color="red")
        print(f"Error: {str(e)}")

def downloadAudio():
    try:
        ytlink = link.get()
        status.configure(text="Downloading...", text_color="blue")
        ytObject = YouTube(ytlink, on_progress_callback=onProgress)
        audio = ytObject.streams.get_audio_only()

        # update instruction to title of the audio
        title.configure(text= ytObject.title, text_color="white")

        # Show progress bar and label
        progressBar.pack(padx=10, pady=10)
        progress_percent.pack()

        output_file = audio.download()

        # Hide progress bar and label after download
        progressBar.pack_forget()
        progress_percent.pack_forget()

        # Convert to mp3
        base, ext = os.path.splitext(output_file)
        mp3_file = base + '.mp3'
        AudioSegment.from_file(output_file).export(mp3_file, format='mp3')
        os.remove(output_file)  # Remove the original file

        status.configure(text="Download Complete! :D", text_color="green")
        print("Download Complete! :D")
    
    except Exception as e:
        status.configure(text=f"Error: {str(e)}", text_color="red")
        print(f"Error: {str(e)}")

def onProgress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progPercentage = bytes_downloaded / total_size * 100

    percentage = str(int(progPercentage))
    progress_percent.configure(text=percentage + '%')
    progress_percent.update()

    progressBar.set(float(progPercentage) / 100)
    app.update_idletasks()

# system settings
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# app frame
app = customtkinter.CTk()
app.geometry("600x400")
app.title("YouTube Video Downloader")

# ui
title = customtkinter.CTkLabel(app, text="Enter YouTube video link")
title.pack(padx=10, pady=10)

# link input
link_var = tkinter.StringVar()  # gives real-time input to variable
link = customtkinter.CTkEntry(app, width=400, height=40, textvariable=link_var)
link.pack()

# download video button
download = customtkinter.CTkButton(app, text="Download Video", command=downloadVideo)
download.pack(padx=20, pady=20)

# download audio button
downloadmp3 = customtkinter.CTkButton(app, text="Download Audio", command=downloadAudio)
downloadmp3.pack(padx=20, pady=0)

# progress percentage and bar
progress_percent = customtkinter.CTkLabel(app, text="")
# progress_percent.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
# progressBar.pack(padx=10, pady=10)

# Status label
status = customtkinter.CTkLabel(app, text="")
status.pack(pady=(20, 10))

# run
app.mainloop()