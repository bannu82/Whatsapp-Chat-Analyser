import streamlit as st
import Preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.sidebar.title('WhatsApp Chat Analyzer')

# State management for collapsing sidebar
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

uploaded_file = st.sidebar.file_uploader('Choose a file', type=['txt'])

# Title and Introduction
if uploaded_file is None:
    st.markdown(helper.desc())

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = Preprocessor.preprocess(data)

    st.dataframe(df)

    # Verify the DataFrame columns
    if 'messages' not in df.columns:
        st.error("The 'messages' column is missing in the DataFrame.")
    else:
        # FETCH USERS
        user_list = df['users'].unique().tolist()
        user_list.remove('Other Notification')
        user_list.sort()
        user_list.insert(0, 'Overall')

        selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

        if not st.session_state.show_analysis:
            show_analysis = st.sidebar.button('Show Analysis')
            hint = st.sidebar.success('Click "Show Analysis" Button')
            
            if show_analysis:
                st.session_state.show_analysis = True
                hint.empty()

        if st.session_state.show_analysis:
            cols1, cols2, cols3, cols4 = st.columns(4)

            no_msg, word, num_media, links = helper.find_stats(selected_user, df)

            with cols1:
                st.header('Total Messages')
                st.title(f':green[{no_msg}]')

            with cols2:
                st.header('Total Words')
                st.title(word)

            with cols3:
                st.header('Media Shared')
                st.title(num_media)

            with cols4:
                st.header('Links Shared')
                st.title(links)

            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, df_busy = helper.most_busy_user(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(df_busy)

            # WORD CLOUD
            try:
                st.title('Word Cloud')
                df_wc = helper.create_cloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except KeyError as e:
                st.error(e)

            # MOST COMMON WORDS
            try:
                st.title('Most Common Words')
                most_common_df = helper.most_common_words(selected_user, df)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1])
                st.pyplot(fig)
            except KeyError as e:
                st.error(e)

            # EMOJI COUNTER
            try:
                st.title('Emoji Counter')
                emoji_df = helper.emoji_counter(selected_user, df)

                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df[1].head(5), labels=emoji_df[0].head(5), autopct='%0.2f')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(emoji_df)
            except KeyError as e:
                st.error(e)

        st.sidebar.divider()

        # Word To Find
        w = st.sidebar.text_input("Word to find message ")

        if st.sidebar.button('word to find'):
            try:
                st.title('Word in Messages')
                msg_df = helper.get_message(selected_user, df, w)
                st.dataframe(msg_df)
            except KeyError as e:
                st.error(e)
