import streamlit as st
import re
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# Define footer text


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            #st.markdown("<br>", unsafe_allow_html=True)  # Force a line break
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        #Montly timeline
        st.title("Montly Timeline")
        timeline=helper.montly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.plot(timeline['time'],timeline['user_message'])
        st.pyplot(fig)
        #daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.plot(daily_timeline['only_date'],daily_timeline['user_message'])
        st.pyplot(fig)
        #activity map
        st.title("Activity_Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.monthly_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #most buisiest user in the group
        if selected_user=='Overall':
            st.title("Most Active users")
            col1,col2=st.columns(2)
            most_active_user_fig,new_df=helper.most_busy_users(df)
            with col1:
                st.header("Most Active Users")
                st.pyplot(most_active_user_fig)
            with col2:
                st.dataframe(new_df)
                
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

            
            
        
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])#x-axis,y-axis
        
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f%%")
            ax.axis('equal')  # Ensure pie chart is circular
            st.pyplot(fig)

        