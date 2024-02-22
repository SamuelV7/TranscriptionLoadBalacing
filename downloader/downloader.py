from pytube import YouTube
import os
from moviepy.editor import VideoFileClip

class Util:
    def __init__(self):
        pass
    
    def clean_title(title):
        return "".join(c for c in title if c.isalpha() 
                            or c.isdigit() or c==' ' or c =='-').rstrip()
    def get_file_name(title, file_extension):
        title = Util.clean_title(title)
        return f"{title}.{file_extension}"
    
    def file_exists(yt_title, file_extension):
        file_to_check = Util.get_file_name(yt_title, file_extension)
        return os.path.isfile(f"./file_storage_mp3/{file_to_check}")


class Downloader:
    def __init__(self, url):
        self.url = url

    def download(self):
        # check if file exists
        self.yt = YouTube(self.url)
        if Util.file_exists(self.yt.title, "mp3"):
            print(f"{self.yt.title} already exists")
            return self
        yt_option = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        # save as mp3
        self.clean_title(self.yt.title)
        yt_option.download(filename=self.clean_title+".mp4")
        print("Download complete!")
        return self
    
    def convert_to_mp3(self):
        print("Converting to mp3...")
        # get rid of double quotes in the title
        self.downloaded_file = f"{self.clean_title}.mp4"
        video = VideoFileClip(self.downloaded_file)
        video.audio.write_audiofile(f"./file_storage_mp3/{self.clean_title}.mp3")
        print("Conversion complete!")
        return self
    

    def delete_video_file(self):
        os.remove(self.downloaded_file)
        return self
    
    def clean_title(self, title):
        self.clean_title = Util.clean_title(title)
        return self

# downloader = Downloader("https://www.youtube.com/watch?v=viIYJ8kf1MU").download().convert_to_mp3().delete_video_file()


