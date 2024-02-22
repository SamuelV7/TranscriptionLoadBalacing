import os

class AudioFiles:
    def __init__(self, path):
        self.path = path

    def get_files(self):
        return [f for f in os.listdir(self.path) if f.endswith('.mp3')]

the_files = AudioFiles('file_storage_mp3').get_files() 
print(the_files)