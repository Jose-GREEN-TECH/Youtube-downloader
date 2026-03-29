import os
import streamlit as st
import yt_dlp

# Set page config FIRST
st.set_page_config(
    page_title="Ultra YouTube Downloader",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium Custom CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glassmorphism Container setup via inner blocks */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(25, 30, 36, 0.45);
        border-radius: 24px;
        padding: 40px 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Fix weird paddings */
    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 5rem !important;
    }

    /* Titles/Headers */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: -10px !important;
    }
    p {
        text-align: center;
        color: #A0AEC0;
        font-size: 1.15rem;
    }

    /* Input fields and Selectbox Styling */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 0.8rem 1rem !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #00C9FF !important;
        box-shadow: 0 0 15px rgba(0, 201, 255, 0.3) !important;
    }

    /* Labels */
    .stTextInput label, .stSelectbox label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px;
    }

    /* Primary Button */
    button[kind="primary"] {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px 0 rgba(255, 65, 108, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100% !important;
        margin-top: 15px !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 25px 0 rgba(255, 65, 108, 0.6) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00C9FF, #92FE9D) !important;
        border-radius: 10px;
    }
    
    hr {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Application Layout
with st.container():
    st.markdown("<h1>Ultra Downloader 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p>Download YouTube Videos & Audio in maximum quality securely.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: #00C9FF; text-align: center; margin-top: -10px;'>✨ Designed by Jose ✨</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    url = st.text_input("🔗 YouTube Link", placeholder="https://www.youtube.com/watch?v=...")
    
    # Use columns to align form fields better
    col1, col2 = st.columns([1, 1.5])
    
    if 'save_dir' not in st.session_state:
        st.session_state.save_dir = os.path.expanduser("~/Downloads")

    def open_folder_dialog():
        import subprocess
        import sys
        code = '''import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
folder = filedialog.askdirectory()
print(folder, end="")
'''
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        folder_path = result.stdout.strip()
        if folder_path:
            st.session_state.save_dir = folder_path

    with col1:
        format_choice = st.selectbox("📂 Format", ["Video (MP4)", "Audio Only (MP3)"])
    with col2:
        # Custom label to align perfectly
        st.markdown("<p style='color: #E2E8F0; font-weight: 600; font-size: 0.95rem; margin-bottom: 5px; margin-top:2px;'>📁 Save Location</p>", unsafe_allow_html=True)
        
        loc_col1, loc_col2 = st.columns([3, 1])
        with loc_col1:
            st.text_input("Hidden Label", key="save_dir", label_visibility="collapsed")
        with loc_col2:
            st.button("Browse", on_click=open_folder_dialog)
                    
    # The actual selected directory to save to
    save_dir = st.session_state.save_dir

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("Download Now 🎬", type="primary"):
        if not url:
            st.warning("⚠️ Please enter a valid YouTube URL.")
        elif not os.path.isdir(save_dir):
            st.error("❌ Invalid save location. Please provide a valid folder path.")
        else:
            # placeholders for updates that keep UI structure clean
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            status_placeholder.info("⏳ Initializing download sequence...")
            
            def strip_ansi(text):
                # Clean up yt-dlp terminal color codes
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                return ansi_escape.sub('', text)

            def my_hook(d):
                if d['status'] == 'downloading':
                    try:
                        percent_str = strip_ansi(d.get('_percent_str', '0%')).strip()
                        percent_float = float(percent_str.replace('%', ''))
                        
                        progress_bar.progress(int(percent_float))
                        speed = strip_ansi(d.get('_speed_str', 'N/A')).strip()
                        eta = strip_ansi(d.get('_eta_str', 'N/A')).strip()
                        
                        status_placeholder.info(f"⚡ **Downloading** | Progress: `{percent_str}` | Speed: `{speed}` | ETA: `{eta}`")
                    except Exception:
                        pass
                elif d['status'] == 'finished':
                    progress_bar.progress(100)
                    status_placeholder.success("✅ Download complete! Finalizing file integration...")
            
            # yt-dlp Configuration
            ydl_opts = {
                'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [my_hook],
                'nocheckcertificate': True,
                'quiet': True,
                'no_warnings': True
            }

            if format_choice == "Audio Only (MP3)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                })

            # Execute Download
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                status_placeholder.success(f"🎉 **Success!** Saved to: `{save_dir}`")
                st.balloons()
            except Exception as e:
                status_placeholder.error(f"❌ **Error:** {str(e)}")
