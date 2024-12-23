import customtkinter
import yt_dlp
import os
import time
from datetime import timedelta
import humanize
from PIL import Image, ImageTk
import requests
from io import BytesIO

def format_size(bytes):
    return humanize.naturalsize(bytes, binary=True)

# mp3 init
def beginDownload():
    # show prog bar when button pressed
    progressBar.pack(padx=10, pady=10)
    progPercentage.pack()
    downloadStats.pack()
    
    start_time = time.time()
    try:
        ytLink = link.get()
        if not ytLink.strip():
            raise ValueError("No link provided. Please enter a valid YouTube link.")
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    # calculations for download process
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                    speed = d.get('speed', 0)
                    
                    if total and downloaded:
                        progress = min(downloaded / total, 1.0)
                        app.after(10, lambda: progressBar.set(progress))
                        
                        # etas
                        if speed and speed > 0:
                            eta = (total - downloaded) / speed
                            eta_str = str(timedelta(seconds=int(eta)))
                        else:
                            eta_str = "calculating..."
        
                        percent = f"{int(progress * 100)}%"
                        speed_str = f"{format_size(speed)}/s" if speed else "calculating..."
                        size_str = f"{format_size(downloaded)} / {format_size(total)}"
                        elapsed = time.time() - start_time
                        elapsed_str = str(timedelta(seconds=int(elapsed)))
                        
                        app.after(10, lambda: progPercentage.configure(text=percent))
                        app.after(10, lambda: downloadStats.configure(
                            text=f"Speed: {speed_str}\n"
                                 f"Size: {size_str}\n"
                                 f"Elapsed Time: {elapsed_str}\n"
                                 f"ETA: {eta_str}"
                        ))
                        app.update()
                except Exception as e:
                    print(f"Progress update error: {e}")
                    # continue download if prog fails
                    pass
                    
            elif d['status'] == 'finished':
                try:
                    total_time = time.time() - start_time
                    file_size = os.path.getsize(d['filename'])
                    
                    app.after(10, lambda: finishLabel.configure(
                        text="Download Complete!",
                        text_color="green"
                    ))
                    app.after(10, lambda: downloadStats.configure(
                        text=f"Completed in: {str(timedelta(seconds=int(total_time)))}\n"
                             f"Final Size: {format_size(file_size)}"
                    ))
                    app.after(10, lambda: progressBar.set(1))
                    app.update()
                except Exception as e:
                    print(f"Completion update error: {e}")
                    finishLabel.configure(text="Download Complete!", text_color="green")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }

        # fetch metadata for thumbnail
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(ytLink, download=False)
            thumbnail_url = info.get('thumbnail', '')
            display_thumbnail(thumbnail_url)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            finishLabel.configure(text="Starting download...", text_color="white")
            ydl.download([ytLink])
            
    except Exception as e:
        print(f"Error: {e}")
        finishLabel.configure(text="Error: Invalid Link or Connection Issue!", text_color="red")
        # if error hide prog bar
        progressBar.pack_forget()
        progPercentage.pack_forget()
        downloadStats.pack_forget()

# mp4 init
def beginDownloadMP4():
    # show progress bar when button is pressed
    progressBar.pack(padx=10, pady=10)
    progPercentage.pack()
    downloadStats.pack()

    start_time = time.time()
    try:
        ytLink = link.get()
        if not ytLink.strip():
            raise ValueError("No link provided. Please enter a valid YouTube link.")

        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                    speed = d.get('speed', 0)

                    if total and downloaded:
                        progress = min(downloaded / total, 1.0)
                        app.after(10, lambda: progressBar.set(progress))

                        if speed > 0:
                            eta = (total - downloaded) / speed
                            eta_str = str(timedelta(seconds=int(eta)))
                        else:
                            eta_str = "calculating..."

                        percent = f"{int(progress * 100)}%"
                        speed_str = f"{format_size(speed)}/s" if speed else "calculating..."
                        size_str = f"{format_size(downloaded)} / {format_size(total)}"
                        elapsed = time.time() - start_time
                        elapsed_str = str(timedelta(seconds=int(elapsed)))

                        app.after(10, lambda: progPercentage.configure(text=percent))
                        app.after(10, lambda: downloadStats.configure(
                            text=f"Speed: {speed_str}\n"
                                 f"Size: {size_str}\n"
                                 f"Elapsed Time: {elapsed_str}\n"
                                 f"ETA: {eta_str}"
                        ))
                        app.update()
                except Exception as e:
                    print(f"Progress update error: {e}")
                    pass

            elif d['status'] == 'finished':
                try:
                    total_time = time.time() - start_time
                    file_size = os.path.getsize(d['filename'])
                    
                    app.after(10, lambda: finishLabel.configure(
                        text="Download Complete!",
                        text_color="green"
                    ))
                    app.after(10, lambda: downloadStats.configure(
                        text=f"Completed in: {str(timedelta(seconds=int(total_time)))}\n"
                             f"Final Size: {format_size(file_size)}"
                    ))
                    app.after(10, lambda: progressBar.set(1))
                    app.update()
                except Exception as e:
                    print(f"Completion update error: {e}")
                    finishLabel.configure(text="Download Complete!", text_color="green")
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4', 
            'progress_hooks': [progress_hook],
        }

        # fetch metadata for thumbnail
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(ytLink, download=False)
            thumbnail_url = info.get('thumbnail', '')
            display_thumbnail(thumbnail_url)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            finishLabel.configure(text="Starting download...", text_color="white")
            ydl.download([ytLink])

    except Exception as e:
        print(f"Error: {e}")
        finishLabel.configure(text="Error: Invalid Link or Connection Issue!", text_color="red")
        progressBar.pack_forget()
        progPercentage.pack_forget()
        downloadStats.pack_forget()

# function to display thumbnail
def display_thumbnail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = Image.open(BytesIO(response.content))
        image_data.thumbnail((200, 200))  # resize
        thumbnail_image = ImageTk.PhotoImage(image_data)
        thumbnail_label.configure(image=thumbnail_image)
        thumbnail_label.image = thumbnail_image
        thumbnail_label.pack(pady=10)
    except Exception as e:
        print(f"Error displaying thumbnail: {e}")
        thumbnail_label.pack_forget()

# sys settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube MP3 Downloader")

# icon
try:
    icon_path = os.path.join(os.getcwd(), "public", "logo.ico")
    app.iconbitmap(icon_path)
except Exception as e:
    print(f"Warning: Could not set application icon. Error: {e}")

# ui
title = customtkinter.CTkLabel(app, text="Paste in a YouTube link")
title.pack(padx=15, pady=15)

link = customtkinter.CTkEntry(app, width=350, height=40)
link.pack()

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack(pady=5)

thumbnail_label = customtkinter.CTkLabel(app)
thumbnail_label.pack_forget()

# prog bar hidden by default
progPercentage = customtkinter.CTkLabel(app, text="0%")
downloadStats = customtkinter.CTkLabel(app, text="")

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)

download = customtkinter.CTkButton(app, text="Download as MP3", command=beginDownload)
downloadmp4 = customtkinter.CTkButton(app, text="Download as MP4", command=beginDownloadMP4)
download.pack(padx=25, pady=15)
downloadmp4.pack(padx=25, pady=15)

# run apps
app.mainloop()
