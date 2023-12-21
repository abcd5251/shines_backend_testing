from pytube import YouTube
from google.cloud import bigquery
from google.oauth2 import service_account
from pytube import YouTube
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

DATASET_NAME = os.getenv("DATASET_NAME")
KEY_PATH = './credentials.json'
CREDENTIALS = service_account.Credentials.from_service_account_file(
        KEY_PATH , scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
CLIENT = bigquery.Client(credentials=CREDENTIALS, project=CREDENTIALS.project_id,)


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

def get_yt_channel_data(search_query:str, page:int):

    page = page * 5
    # get specific information
    query = """
    SELECT *
    FROM `shines-backend-406614.{}.{}` 
    LIMIT 5 OFFSET {}
    """.format(DATASET_NAME, search_query, page)

    

    query_job = CLIENT.query(query)

    results = query_job.result()
   
   
    final_df = pd.DataFrame([dict(row.items()) for row in results])
    
    play_link = []
    for yt_url in final_df["video_url"]:
        temp_link = get_mp4_link(yt_url)
        play_link.append(temp_link)
    final_df["play_link"] = play_link


    return final_df

def get_tag_info(tag_num:int, page : int):
    
    page = page * 5
    web3_mapping = {
        0: "NFT",
        1: "Ethereum",
        2: "GameFi",
        3: "ZK",
        4: "Layer2"
    }

    print(web3_mapping[tag_num])
    query = """
    SELECT *
    FROM `shines-backend-406614.{}.*`
    WHERE video_class = "{}"
    LIMIT 5 OFFSET {}
    """.format(DATASET_NAME, web3_mapping[tag_num], page)
    

    
    query_job = CLIENT.query(query)

    results = query_job.result()
   
   
    final_df = pd.DataFrame([dict(row.items()) for row in results])
    play_link = []
    for yt_url in final_df["video_url"]:
        temp_link = get_mp4_link(yt_url)
        play_link.append(temp_link)
    final_df["play_link"] = play_link


    return final_df


if __name__ == "__main__":
    channel_information = get_yt_channel_data("ABCDELabs", 1)

    