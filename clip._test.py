import streamlit as st
import base64

st.set_page_config(page_title="ScrapSnap", layout="wide")

# --- 1. DATA ---
if 'total_cals' not in st.session_state:
    st.session_state.total_cals = 0
if 'last_val' not in st.session_state:
    st.session_state.last_val = 0

with st.sidebar:
    st.header("Input")
    val = st.number_input("Calories:", min_value=0, step=100)
    if st.button("Update"):
        st.session_state.last_val = val
        st.session_state.total_cals += val

    show_grid = st.checkbox("Show Grid", value=True)

# --- Math ---
curr = st.session_state.last_val
total = st.session_state.total_cals

s_old, s_co2, s_fam = curr / 1250, curr * (1.5 / 1000), curr / 4000
t_old, t_co2, t_fam = total / 1250, total * (1.5 / 1000), total / 4000