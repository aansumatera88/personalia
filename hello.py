import streamlit as st

st.set_page_config(page_title="Hello World", page_icon="mylogo2.png", layout="wide")


if "HelloWold" not in st.session_state:
    st.session_state.HelloWold = "Hello Wold"
    
st.write(st.session_state.HelloWold)

st.balloons()