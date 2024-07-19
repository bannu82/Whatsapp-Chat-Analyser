from urlextract import URLExtract   
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd 
import emoji
import os
import re

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
    df = df[df['messages']!='<Media omitted>']
    df = df[df['messages']!='']


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
    df = df[df['messages']!='<Media omitted>']
    df = df[df['messages']!='']


    words = []

    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))    




def get_message(selected_user , df , word):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]    
    
    df1 = pd.DataFrame(columns=df.columns)    
    
    for idx, msg in df.iterrows():
        if word in msg['messages'].split():
            df1 = pd.concat([df1, df.loc[[idx]]], ignore_index=True)
    
    return df1

def get_data_by_clmn(selected_user , df , clmn , data):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    print(clmn)
    if clmn == 'day' or 'hour' or 'minute' or 'year':
        d = int(data)
        return df[df[clmn]==d]  
    elif clmn == 'users' or 'messages' :
        return df[df[clmn]==str(data)]  

            
    
            
def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    emojis = []
    
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df 


def save_data_file(file_name , df):
    directory_path = 'Chats/'

    if os.path.exists(directory_path+re.sub('.txt', '.csv' ,file_name)):
        return "allready exist"
    else:
        df.to_csv( directory_path + re.sub('.txt', '.csv' ,file_name) )
        return "save file"