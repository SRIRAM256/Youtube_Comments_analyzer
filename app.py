from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import googleapiclient.discovery
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import pickle as pkl
from PIL import Image
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import re
import io

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


load_dotenv()
app = Flask(__name__)
CORS(app)
# YouTube API Configuration
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

# Function to fetch all comments
def fetch_comments(video_id):
    comments = []
    next_page_token = None
    count=30
    while count:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # Maximum allowed value
            pageToken=next_page_token,
            order="relevance",
        )
        response = request.execute()

        # Append comments from the current page
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # Check if there's another page
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

        count-=1

    return comments


def analyze(data):
    # take data it is  aa dataframe and import pickle files  and do calculTIONS
    lemma=WordNetLemmatizer()
    stop_words=set(stopwords.words("english"))

    def clean_text(text):
        text=text.lower()
        text=re.sub(r"[^a-zA-Z0-9]"," ",text)
        words=nltk.word_tokenize(text) 
        return " ".join([lemma.lemmatize(word) for word in words if word not in stop_words])
    
    data["Comment"]=data["Comment"].apply(clean_text)

    # model loading 
    vector=pkl.load(open("model/vectorizer.pkl","rb"))
    model=pkl.load(open("model/light_gbm_model.pkl","rb"))

    # testing 
    x_test=vector.transform(data["Comment"])
    y_pred=model.predict(x_test)

    #calculate positive and negative comments
    y_pred=[1 if i>=0.5 else 0 for i in y_pred]
    neg=sum(y_pred)
    pos=len(y_pred)-neg
    
    
    labels = ['Positive', 'Negative']
    sizes = [pos, neg]

    # Create a pie chart
    plt.figure(figsize=(8, 6))  
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return img

@app.route('/analyze/<video_id>', methods=['GET', 'POST'])
def analyze_video(video_id):
    try:
        # Fetch comments using the YouTube API
        comments = fetch_comments(video_id)

        # Convert comments to a DataFrame
        comments_df = pd.DataFrame(comments, columns=["Comment"])

        # Analyze comments and generate image
        img = analyze(comments_df)

        return send_file(img, mimetype='image/png')

    except Exception as e:  # Handle potential errors properly
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
