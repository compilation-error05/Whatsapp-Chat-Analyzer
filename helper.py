from urlextract import URLExtract
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import re

import emoji
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
        
    #1.fetch number of messages
    num_message=df.shape[0]
    #2.number of words
    words=[]
    for message in df['user_message']:
        words.extend(message.split())
    #3.number of media messages
    num_media=df[df['user_message']=='<Media omitted>\n'].shape[0]
    #4.no. of links
    links = []
    for message in df['user_message']:
        links.extend(extract.find_urls(message))
    return num_message,len(words),num_media,len(links)
def most_busy_users(df):
    x=df['user'].value_counts().head()
    name=x.index
    count=x.values
    fig,ax=plt.subplots()
    plt.bar(name,count)
    ax.set_xticklabels(name, rotation='vertical')
    ax.set_xlabel('Users')
    ax.set_ylabel('Message Count')
    ax.set_title('Most Active Users')
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'user':'Name','count':'Percentage'})
    return fig,df
def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    #to remove the stop words
    #1st remove the grp notification    
    temp=df[df['user']!='group_notification']
    #2nd stop words that is media files
    temp = temp[temp['user_message'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        f=open('stop_hinglish.txt','r')
        stop_words=f.read()
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    temp['user_message']=temp['user_message'].apply(remove_stop_words)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    df_wc=wc.generate(temp['user_message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    #to remove the stop words
    #1st remove the grp notification    
    temp=df[df['user']!='group_notification']
    #2nd stop words that is media files
    temp = temp[temp['user_message'] != '<Media omitted>\n']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    #stop_words
    words=[]
    for message in temp['user_message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['user_message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Count'])
    return emoji_df
def montly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['user_message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]+"-"+str(timeline['year'][i])))
    timeline['time']=time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['user_message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='user_message', aggfunc='count').fillna(0)

    return user_heatmap
