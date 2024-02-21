from pytube import YouTube
import ffmpeg
import os
# print("Starting download...")
# yt = YouTube("https://www.youtube.com/watch?v=viIYJ8kf1MU")
# yt_option = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# yt_option.download()
# print("Download complete!")

class Downloader:
    def __init__(self, url):
        self.url = url

    def download(self):
        print("Starting Download")
        self.yt = YouTube(self.url)
        yt_option = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        # save as mp3
        yt_option.download("./")
        print("Download complete!")
        return self
    
    def convert_to_mp3(self):
        print("Converting to mp3...")
        self.downloaded_file = f"./{self.yt.title}.mp4"
        stream = ffmpeg.input(self.downloaded_file)
        stream = ffmpeg.output(stream, f"file_storage/{self.yt.title}.mp3")
        ffmpeg.run(stream)
        print("Conversion complete!")
    
    def delete_video_file(self):
        os.remove(self.downloaded_file)

downloader = Downloader("https://www.youtube.com/watch?v=viIYJ8kf1MU").download().convert_to_mp3().delete_video_file()


