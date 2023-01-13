import streamlit as st
st.title("Accessibility Analysis Tool")
st.map()
df_uploaded = st.sidebar.file_uploader('Select the coordinates in map by clicking the arrow icon')
st.sidebar.multiselect('Travel Time',['5 minutes','10 minutes','15 minutes','30 minutes','45 minutes','60 minutes'])
st.sidebar.button("Download Report")
