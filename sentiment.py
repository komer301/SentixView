from googleapiclient.discovery import build
import pandas as pd
import config
from transformers import pipeline

api_service_name = "youtube"
api_version = "v3"
api_key = config.apiKey

def analysis(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    # video_id = "SIm2W9TtzR0"
    video_response=youtube.commentThreads().list(
        part='snippet',
        videoId=video_id
        ).execute()
    comments = {}
    sent_pipeline = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
    while video_response:
            for item in video_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments[comment] = sent_pipeline(comment)[0]['label']
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                        part = 'snippet',
                        videoId = video_id,
                        pageToken = video_response['nextPageToken']
                    ).execute()
            else:
                break

    comments_df = pd.DataFrame.from_dict(comments,orient='index',columns=['sentiment']).reset_index()
    comments_df.columns = ['comment', 'sentiment']
    sentiment_distribution = comments_df['sentiment'].value_counts(normalize=True) * 100
    sentiment_json = sentiment_distribution.to_json()
    return sentiment_json



