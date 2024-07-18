import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[ap]m\s-\s'
    
    messages = re.split(pattern , data)[1:]
    striped_messages = [s.strip() for s in messages]

    dates = re.findall(pattern ,data)
    striped_dates = [s.strip(' - ') for s in dates]

    df  = pd.DataFrame({"date":striped_dates , 'message':striped_messages})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p')

    user = []
    message = []

    for m in df['message']:
        entry = re.split('([\W\w]+?):\s', m)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
            
        else:
            user.append('Other Notification')
            message.append(entry[0])
    df['users']= user
    df['messages'] = message
    df.drop(columns=['message'],inplace=True)    

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    return(df)
