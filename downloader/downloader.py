from pytube import YouTube

print("Starting download...")
yt = YouTube("https://www.youtube.com/watch?v=viIYJ8kf1MU")
yt_option = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

yt_option.download()
print("Download complete!")

