import pytube
from pytube import YouTube

link = input("Enter URL (Video): ")
video = YouTube(link)
vid = video.streams.get_highest_resolution()
vid.download('C:/Users/Chiu/PyCharmProjects/py_storage/py_youtube')
