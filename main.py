import customtkinter
import yt_dlp
import os

def beginDownload():
    try:
        ytLink = link.get()
        if not ytLink.strip():
            raise ValueError("No link provided. Please enter a valid YouTube link.")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'outtmpl': '%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytLink])
        print("Your Download is Complete!")
    except Exception as e:
        print(f"Error: {e}")
        print("Error 404. Invalid Link!")

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

download = customtkinter.CTkButton(app, text="Download as MP3", command=beginDownload)
download.pack(padx=25, pady=15)

# run apps
app.mainloop()
