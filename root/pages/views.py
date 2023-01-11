from django.shortcuts import render, redirect
import yt_dlp
import os,stat
from django.http import FileResponse


#home page
def home(request):

    dir = './mp3downloads/'
    remove_files(dir)

    if request.method == "POST":
        video_url = request.POST.get("youtube-url")
        if video_url:
            video_info = yt_dlp.YoutubeDL().extract_info(url = video_url,download=False)
            filename = f"{video_info['title']}.mp3"
            thumbnail = video_info['thumbnail']
            options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':'./mp3downloads/'+filename,
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])
            print("Download complete... {}".format(filename))
            return render(request, "index.html", {"data": filename, "img":thumbnail})

    return render(request, "index.html", {})


def remove_files(dir_path):
    for file in os.listdir(dir_path):
        file_name = os.path.join(dir_path, file)
        os.chmod(file_name, stat.S_IWRITE)
        os.remove(file_name)



def download(request):
    dir_path = './mp3downloads/'
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
    file_to_download = open(str(file_path), 'rb')
    response = FileResponse(file_to_download, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename= %s' % file
    return response

def home_view(request):
    return redirect('home', {})