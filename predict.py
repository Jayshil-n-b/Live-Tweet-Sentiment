import pandas as pd
import tweepy
import streamlit as st
from textblob import TextBlob


def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getSentiment(score):
    if (score < 0):
        return 'Negative'
    elif (score == 0):
        return 'Neutral'
    else:
        return 'Positive'


def getAnalysis(inputText):
    subjectivity = getSubjectivity(inputText)
    polarity = getPolarity(inputText)
    sentiment = getSentiment(polarity)
    return [subjectivity, polarity, sentiment]


# Twitter API secrets.
user_key = "EnDz7gkde5lPh0uPFbJGuyAbd"
user_secret = "J1mTNw5B5OEmmxkfFfVj0kxO9raGquPkqkqpCTeGz1MnV8G3lK"
access_token = "1410964135974608899-0gQFEa2WJ6QxXw0oWDxrVAKzbl9xCQ"
access_token_secret = "wVkn5OsNQVK0LBcaGmP962o85wF3Q3GSYLv2wypsRwDhB"

# Create instance of tweepy api.
auth = tweepy.OAuthHandler(user_key, user_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# Create functions to handle requirements.


def fetchTweets():
    public_tweets = api.home_timeline()
    colums = ['Tweet']
    data = []
    for tweet in public_tweets:
        data.append([tweet.text])
    df = pd.DataFrame(data, columns=colums)
    df["Subjectivity"] = df["Tweet"].apply(getSubjectivity)
    df["Polarity"] = df["Tweet"].apply(getPolarity)
    df["Sentiment"] = df["Polarity"].apply(getSentiment)
    return df.to_csv().encode("utf-8")


st.title('Live Tweet Sentiment Prediction')
if st.button('Fetch and Predict Sentiment'):
    df = fetchTweets()
    st.download_button(
        label="Download predicted CSV",
        data=df,
        file_name="predictedSentiments.csv",
        mime="text/csv",
    )

# review_csv = st.file_uploader("Upload CSV file here", type="csv")

# if review_csv is not None:
#     df = pd.read_csv(review_csv)
#     out_csv = process(df)
#     st.download_button(
#         label="Download predicted CSV",
#         data=out_csv,
#         file_name="predictedReviews.csv",
#         mime="text/csv",
#     )
