import os

from pytube import YouTube

def downloader(link,search_term):
    target_path=r'youtube_vedios/'
    try:
        for i in link:
            yt = YouTube(i)
            d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1]
            target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            d_video.download(target_folder)
    except:
        print("Download Error")

    print('Task Completed!')
#downloader(['https://www.youtube.com/watch?v=WMolA7QMP5w'],'krish nayak')