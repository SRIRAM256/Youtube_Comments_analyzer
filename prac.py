import googleapiclient.discovery
import pandas as pd
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyCzR9SfwFVQBpY6PxHmnNdm05U6nlDRuxk"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

# Function to fetch all comments
def fetch_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # Maximum allowed value
            pageToken=next_page_token
        )
        response = request.execute()

        # Append comments from the current page
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there's another page
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

# Fetch all comments for the video
video_id = "4_eeI1LElWc"
all_comments = fetch_comments(video_id)

comments_df = pd.DataFrame(all_comments, columns=["Comment"])


print("Comments fetched:", len(all_comments))
print(all_comments)