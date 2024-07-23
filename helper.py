from urlextract import URLExtract   
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd 
import emoji
import os
import re

def desc():
    return """
Welcome to the WhatsApp Chat Analyzer! This tool allows you to analyze your WhatsApp chat data and gain insights into your messaging patterns. :iphone: :speech_balloon:

## Features
- **:incoming_envelope: Total Messages**: Get the total number of messages in the chat.
- **:memo: Total Words**: Count the total number of words exchanged.
- **:camera: Media Shared**: See the total number of media files shared.
- **:link: Links Shared**: View the number of links shared in the chat.
- **:busts_in_silhouette: Most Busy Users**: Identify the most active participants in the chat.
- **:cloud: Word Cloud**: Visualize the most frequently used words.
- **:speaking_head_in_silhouette: Most Common Words**: Find out the most common words used in the chat.
- **:smiley: Emoji Counter**: Analyze the usage of emojis.
- **:mag: Search Messages by Word**: Find messages containing a specific word.

## How to Use
1. **:file_folder: Upload Your Chat File**: Click on the "Choose a file" button in the sidebar to upload your WhatsApp chat file (in .txt format).
2. **:bust_in_silhouette: Select User**: Choose a user from the dropdown to analyze the chat data for a specific participant or select "Overall" for all participants.
3. **:bar_chart: Show Analysis**: Click the "Show Analysis" button to generate and view the statistics and visualizations.
4. **:mag_right: Search for a Word**: Use the text input in the sidebar to search for messages containing a specific word.

Upload your WhatsApp chat file and start exploring your chat data! :rocket:

---

### :octocat: Connect with Me
For more projects and code, visit my [GitHub profile](https://github.com/bannu82).
"""

def find_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Fetch Number of messages
    num_messages = df.shape[0]

    # Fetch Total Number of words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    # Fetch Number of media messages
    num_media_message = df[df['messages'] == '<Media omitted>'].shape[0]

    # Fetch Number of links shared
    extractor = URLExtract()
    links = []
    for msg in df['messages']:
        if extractor.find_urls(msg):
            links.extend(extractor.find_urls(msg))

    return num_messages, len(words), num_media_message, len(links)


def most_busy_user(df):
    x = df['users'].value_counts().head(5)
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'users': 'name', 'count': 'percent'})
    return x, df


def create_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]        

    df = df[df['users'] != 'Other Notification']
    df = df[df['messages'] != '<Media omitted>']
    df = df[df['messages'] != '']

    # Check if 'messages' column exists
    if 'messages' not in df.columns:
        raise KeyError("The 'messages' column is missing in the DataFrame.")
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user , df):
    f = open('stop_hinglish.txt' , 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    df = df[df['users'] != 'Other Notification']
    df = df[df['messages'] != '<Media omitted>']
    df = df[df['messages'] != '']

    words = []

    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    words_count = Counter(words).most_common(10)

    words_list = []
    count_list =[]
    for i in range(len(words_count)) :
        words_list.append(words_count[i][0])
        count_list.append(words_count[i][1])

    data = pd.DataFrame({'Words': words_list, 'Counts': count_list})
    return data


def get_message(selected_user , df , word):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]    
    
    df1 = pd.DataFrame(columns=df.columns)    
    
    for idx, msg in df.iterrows():
        if word in msg['messages'].split():
            df1 = pd.concat([df1, df.loc[[idx]]], ignore_index=True)
    
    return df1


def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis = []
    
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df 

def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year' , 'month_num' ,'month']).count()['messages'].reset_index()
    
    time = []
    
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time 
    
    return timeline

def daily_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline