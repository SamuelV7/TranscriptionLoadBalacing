from pytube import Playlist, YouTube
import redis
from downloader import Util
from downloader import Downloader
import os

class PlaylistYT:
    def __init__(self, url):
        self.url = url
    
    def get_playlist(self):
        self.playlist = Playlist(self.url)
        return self

    def list_videos(self):
        for video in self.playlist.videos:
            print(video.title)
        return self

    def length(self):
        self.len = len(self.playlist.videos)
        return self
    
    def not_downloaded(self):
        videos_yet_to_download = []
        for video in self.playlist.videos:
            # check if audio exists
            file_to_check = Util.get_file_name(video.title, "mp3")
            if not os.path.isfile(f"./file_storage_mp3/{file_to_check}"):
                videos_yet_to_download.append(video)
        self.videos_yet_to_download = videos_yet_to_download
        return self

    def download_not_downloaded(self):
        for video in self.videos_yet_to_download:
            Downloader(video.watch_url).download().convert_to_mp3().delete_video_file()
            r = RedisDB()
            # save to redis with key as the url and value as full file name
            # and other details like title, etc
            to_save = {
                "title": video.title,
                "file_name": Util.get_file_name(video.title, "mp3"),
                "url": video.watch_url
            }
            r.set(video.watch_url, to_save)
        return self

class RedisDB:
    def __init__(self):
        self.r = redis.Redis(host='redis_downloader', port=6379, decode_responses=True)
    
    def set(self, key, value):
        self.r.set(key, value)
        return self
    
    def get(self, key):
        return self.r.get(key)

p = PlaylistYT("https://www.youtube.com/watch?v=MfFd9Ij10-w&list="
                    +"PL3f0nkvUr4WRhzyK5jf0pMBe8i94kT-PV&pp=iAQB")

p.get_playlist().length().not_downloaded().download_not_downloaded()
