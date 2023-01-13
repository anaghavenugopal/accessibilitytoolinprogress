import streamlit as st
st.title("Accessibility Analysis Tool")
st.map()
st.sidebar.caption("Select the desired features to perform the analysis")
st.sidebar.multiselect('Travel Time',['5 minutes','10 minutes','15 minutes','30 minutes','45 minutes','60 minutes'])
st.sidebar.multiselect('Modes',['Walking','Cycling','Public Transit'])
st.sidebar.multiselect('Points of Interest',['Restaurant','Bank','Pharmacy','Supermarket','Cafe','University'])
st.caption("Select the coordinates in map by clicking the arrow icon")
st.button("Run and View Analysis")
st.button("Download Report")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.write(' ')
