import scrapetube
import pandas as pd
from pytube import YouTube
from google.cloud import bigquery
from google.oauth2 import service_account
from concurrent.futures import TimeoutError
import os
import json
from modules.utils import openai_model
from pandas_gbq import to_gbq
import uuid
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID = "shines-backend-406614"
DATASET_NAME = os.getenv("DATASET_NAME")
URL = "https://www.youtube.com/watch?v="

def upload_gcp(dataframe, table_name: str, credentials):
    to_gbq(dataframe, f"{DATASET_NAME}.{table_name}", project_id=PROJECT_ID, if_exists="replace", credentials=credentials)

def classify_category(information:str):
    # use ChatGPT to classify
    category = openai_model(information)
    return category

def save_channel_links(username: str):
    # GCP credentials setting
    key_path = './credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)
        

    videos = scrapetube.get_channel(channel_username = username)
    
    video_id = []
    video_url = []
    video_title = []
    video_author = []
    video_description = []
    video_publish_date = []
    video_image = []
    #video_keywords = []
    #video_rating = []
    video_class = []
    video_views = []
    video_duration = []


    for idx, video in enumerate(videos):
        yt_url = URL + video['videoId']
        if idx > 3:
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
            category = classify_category(video_information)
                     

            # Video saving list
            video_id.append(video_uuid )
            video_url.append(yt_url)
            video_title.append(title)
            video_author.append(author)
            video_description.append(description)
            video_publish_date.append(publish_date.strftime("%Y-%m-%d %H:%M:%S"))
            video_image.append(thumbnail_url)
            #video_keywords.append(keywords)
            #video_rating.append(rating)
            video_class.append(category)
            video_views.append(views)
            video_duration.append(duration)

            print("save:",title)
            print("save:",author)

            
        except Exception as e:
            print(f"error {str(e)}")   

    result = pd.DataFrame({
        "video_uuid": video_id,
        "video_url": video_url,
        "video_title": video_title,
        "video_author": video_author,
        "video_description": video_description,
        "video_publish_date": video_publish_date,
        "video_image": video_image,
        "video_class": video_class,
        "video_views": video_views,
        "video_duration": video_duration
    })
    
    # save_place = "./result.csv"
    # result.to_csv(save_place, index = False, encoding = "utf-8-sig")
    
    upload_gcp(result, username, credentials)
    


if __name__ == "__main__":   
    channels = ["ABCDELabs"]  
    
    for channel in channels:
        save_channel_links(channel)