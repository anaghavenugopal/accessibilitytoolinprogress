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
    st.image("https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.wixstatic.com%2Fmedia%2Fc54b12_66218b11fcc74760b7f7ffb04f1419d6~mv2.png%2Fv1%2Fcrop%2Fx_9%2Cy_12%2Cw_880%2Ch_243%2Ffill%2Fw_520%2Ch_134%2Cal_c%2Cq_85%2Cusm_0.66_1.00_0.01%2Cenc_auto%2FCurrent%2520logo.png&imgrefurl=https%3A%2F%2Fwww.smartmobilityhubs.eu%2F&tbnid=7wsbqSKDyiMdAM&vet=12ahUKEwiT9PWxs8T8AhVWwrsIHeWPCn8QMygAegUIARDQAQ..i&docid=wAME54JwqfjubM&w=520&h=134&q=smarthubs%20&ved=2ahUKEwiT9PWxs8T8AhVWwrsIHeWPCn8QMygAegUIARDQAQ")

with col3:
    st.write(' ')
