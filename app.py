import streamlit as st
import Preprocessor, helper
import matplotlib.pyplot as plt

st.title('WhatsApp Chat Analyzer')


uploaded_file = st.sidebar.file_uploader('Choose a file', type=['txt'])

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
        


        
        if st.sidebar.button('Show Analysis'):
            cols1, cols2, cols3, cols4 = st.columns(4)

            no_msg, word, num_media, links = helper.find_stats(selected_user, df)

            with cols1:
                st.header('Total Messages')
                st.title(no_msg)

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


#               WORD CLOUD
            try:
                st.title('World Cloud')
                df_wc = helper.create_cloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except KeyError as e:
                st.error(e)

#               MOST COMMON WORD 
            try:
                st.title('Most Common Words')
                most_common_df = helper.most_common_words(selected_user , df)
                fig , ax = plt.subplots()
                ax.barh(most_common_df[0]  , most_common_df[1])
                st.pyplot(fig)
                st.dataframe(most_common_df)
            
            except KeyError as e:
                st.error(e)                


            # try:
            
            #     st.title('find messages')
                
            #     msg_df = helper.get_message(selected_user , df , w)
            #     st.dataframe(msg_df,use_container_width=True)

            # except KeyError as e:
            #     st.error(e)

        
        # Word To Find
        w = st.sidebar.text_input("Word to find message ")

        if st.sidebar.button('word to find'):
             
            try:
                st.title('word in msgs')
                
                msg_df = helper.get_message(selected_user , df , w)
                st.dataframe(msg_df)


            except KeyError as e:
                st.error(e)
        

        # Find By Column
        clmn = df.columns.tolist()

        selected_clmn = st.sidebar.selectbox('select column',clmn)
        if selected_clmn:
            selected_data = st.sidebar.text_input('Enter ')

        if st.sidebar.button('find'):
            st.dataframe(helper.get_data_by_clmn(selected_user , df , selected_clmn , selected_data))
        