import scrapetube
import uuid
import json
from pytube import YouTube

username = "ABCDELabs"
URL = "https://www.youtube.com/watch?v="

def get_mp4_link(youtube_url:str):
    try:
        # Youtube object
        yt = YouTube(youtube_url)

        # get youtube video streams
        video_streams = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()

        # get youtube video mp4 link
        mp4_link = video_streams.url

        return mp4_link

    except Exception as e:
        print(f"Error: {e}")
        return None

def save_channel_links(username: str):
    # GCP credentials setting

    videos = scrapetube.get_channel(channel_username = username, content_type = "shorts")


    for idx, video in enumerate(videos):
        yt_url = URL + video['videoId']
        if idx > 1:
            break
        try:
            # Create uuid 
            video_uuid = str(uuid.uuid4())
            # Create a YouTube object
            yt = YouTube(yt_url)
            
            # Get video details
            title = yt.title
            duration = yt.length
            views = yt.views
            author = yt.author
            publish_date = yt.publish_date
            rating = yt.rating
            keywords = yt.keywords
            video_info = yt.vid_info
            metadata = yt.metadata
            caption_tracks = yt.caption_tracks
            captions = yt.captions
            channel_id = yt.channel_id
            fmt_streams = yt.fmt_streams
            streams = yt.streams
            streaming_data = yt.streaming_data
            description = yt.description
            thumbnail_url = yt.thumbnail_url
            best_format = yt.streams.get_highest_resolution()
            file_size_bytes = best_format.filesize
            
            # search information
            video_information = f"Title : {title}\nDescription : {description}"
            
            mp4_link = get_mp4_link(yt_url)


            print("save:",title)
            print("save:",author)

            
        except Exception as e:
            print(f"error {str(e)}")   

    result = {
        "video_uuid": video_uuid,
        "video_url": yt_url,
        "video_title": title,
        "video_author": author,
        "video_description": description,
        "video_mp4_link": mp4_link,
    }
    
    return result

result = save_channel_links(username)
with open("temp.json", 'w') as json_file:
    json.dump(result, json_file)

print(f'Result has been saved to: {"temp.json"}')
print(result)