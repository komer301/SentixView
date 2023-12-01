from googleapiclient.discovery import build
import pandas as pd
import config
from transformers import pipeline
import concurrent.futures

api_service_name = "youtube"
api_version = "v3"
api_key = config.apiKey
sent_pipeline = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

def fetch_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=500,
        textFormat="plainText"
    ).execute()
    comments = []

    while video_response:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay'][:500]
            comments.append(comment)

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=500,
                textFormat = "plainText",
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break

    return comments

def analyze_sentiment(comment):
    return sent_pipeline(comment)[0]['label']

def analysis(video_id):
    comments = fetch_comments(video_id)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        sentiment_labels = list(executor.map(analyze_sentiment, comments))

    comments_df = pd.DataFrame({
        'comment': comments,
        'sentiment': sentiment_labels
    })

    sentiment_distribution = round(comments_df['sentiment'].value_counts(normalize=True) * 100)
    sentiment_json = sentiment_distribution.to_json()
    
    return sentiment_json