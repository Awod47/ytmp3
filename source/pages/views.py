from django.shortcuts import render, HttpResponse
import requests
from pytube import YouTube
import os
import re
import shutil



# Create your views here.
def home_view(request, *args, **kwargs):

    remove_file()

    video = ""

    if request.POST:
        url = request.POST['video_url']
        pattern = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$")
        res = pattern.match(url)
        if res:
            
            video = YouTube(url)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(output_path= './downloads', filename=f"{video.title}.mp3")
        


        return render(request, 'home.html', {'url':url})
        
    return render(request, 'home.html', {})

def download_file(request):
    file_name = ""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_to_file = os.path.join(base_dir, 'downloads')
    for root,dir,files in os.walk(path_to_file):
        for file in files:
            file_name = file
    file_path = path_to_file + "\\" + file_name

    response = HttpResponse(open(file_path, 'rb').read())
    response['Content-Type'] = 'application/forcedownload'
    response['Content-Disposition'] = f'attachment; filename={file_name}' 
    return response

def remove_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_to_file = os.path.join(base_dir, 'downloads')
    shutil.rmtree(path_to_file)
    os.mkdir(path_to_file)


    



