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

# Math
curr = st.session_state.last_val
total = st.session_state.total_cals
s_dol, s_fam = curr/2000 * 13.00, curr/3000
t_dol, t_fam = total/2000 * 13.00, total/3000

# --- 2. IMAGE ---
def get_base64(file):
    try:
        with open(file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

img_base64 = get_base64("ScrapSnap 2.0.png")

# --- 3. THE DISPLAY ---
if img_base64:
     
    html_code = f"""
    <div style="position: relative; width: 600px; height: 850px; margin: 0 auto; background-image: url('data:image/jpg;base64,{img_base64}'); background-size: 100% 100%;">
        
        <div style="position: absolute; top: 17%; left: 50%; transform: translateX(-50%); width: 100%; text-align: center; color: white; font-size: 72px; font-family: Impact; font-weight: 900; text-shadow: 2px 2px 8px black;">
            {curr}
        </div>

        <div style="position: absolute; top: 40.5%; left: 21%; transform: translateX(-50%); color: navy; font-size: 43px; font-family: Inter; font-weight: 800;">${s_dol:.2f}</div>
        <div style="position: absolute; top: 40.5%; left: 80%; transform: translateX(-50%); color: navy; font-size: 43px; font-family: Inter; font-weight: 800;">{s_fam:.1f}</div>

        <div style="position: absolute; top: 74%; left: 21%; transform: translateX(-50%); color: navy; font-size: 43px; font-family: Inter; font-weight: 800;">${t_dol:.2f}</div>
        <div style="position: absolute; top: 74%; left: 80%; transform: translateX(-50%); color: navy; font-size: 43px; font-family: Inter; font-weight: 800;">{t_fam:.1f}</div>
    </div>
    """
    
    st.components.v1.html(html_code, height=900)

else:
    st.error("Missing Image!")