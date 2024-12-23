# YouTube MP3 Downloader

## Overview

This YouTube MP3 Downloader is a simple Python application that allows users to download audio from YouTube videos in MP3 format.Paste a YouTube link into the application, and upon clicking the "Download as MP3" button, the audio will be extracted and saved to the local directory.

## Features

- Sleek UI built with `customtkinter`.
- Saves the audio file in MP3 format and freshly supported MP4 format!
- Downloads the best audio and video quality available.

## Dependencies

To run this application, you need to have Python installed. These are the dependencies:

- `customtkinter`: A modern and customizable tkinter interface.
- `yt-dlp`: A command-line program to download videos from YouTube and other sites.
- `humanize`: Turns a number into a human-readable duration.
- `pillow`: Library for saving image formats.
- `requests`: Makes HTTPS requests to a specified URL.

### Installation

You can install the required dependencies using pip. Run the following commands in your terminal:

```bash
pip install customtkinter yt-dlp
```

## Usage

1. Clone or download the repository.
2. cd to the project directory.
3. Run the application using the command:

   ```bash
   python main.py
   ```

4. Paste a YouTube link into the input field.
5. Click the "Download as MP3" button to start the download.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
