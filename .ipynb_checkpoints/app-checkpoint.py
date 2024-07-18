import streamlit as st
import Preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title('WhatsApp Chat Analyzer')


uploaded_file = st.sidebar.file_uploader('Choose a file', type=['txt'])

if uploaded_file is not None :
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = Preprocessor.preprocess(data)
    st.dataframe(df)

    #FETCH USERS
    user_list = df['users'].unique().tolist()
    user_list.remove('Other Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)
    
    if st.sidebar.button('Show Analysis'):
        
        cols1 , cols2 , cols3 , cols4 = st.columns(4)

        no_msg ,word , num_media , links= helper.find_stats(selected_user , df)

        

        with cols1:
            st.header('Total Messages')
            st.title(no_msg)

        with cols2:
            st.header('Total Words')
            st.title(word)

        with cols3:
            st.header('Media Shared')
            st.title(num_media)
        with cols3:
            st.header('Links Shared')
            st.title(links)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x =helper.most_busy_user(df)
            fig ,ax = plt.subplots() 
            
            col1 , col2 = st.columns(2) 
            
            with col1:
                ax.bar(x.index , x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


