import os
import streamlit as st
import yt_dlp
import tempfile
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Ultra YouTube Downloader",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium Custom CSS (Kept your original styling)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(25, 30, 36, 0.45); border-radius: 24px; padding: 40px 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    h1 { text-align: center; background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important; font-weight: 800 !important; }
    p { text-align: center; color: #A0AEC0; font-size: 1.15rem; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.3) !important; color: white !important;
        border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%) !important;
        border-radius: 50px !important; font-weight: 700 !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<h1>Ultra Downloader 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p>Download YouTube Videos & Audio securely to your device.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: #00C9FF; text-align: center; margin-top: -10px;'>✨ Designed by Jose ✨</p>", unsafe_allow_html=True)
    
    url = st.text_input("🔗 YouTube Link", placeholder="https://www.youtube.com/watch?v=...")
    format_choice = st.selectbox("📂 Format", ["Video (MP4)", "Audio (MP3)"])

    st.markdown("<hr>", unsafe_allow_html=True)

    # State management for the file buffer
    if 'download_ready' not in st.session_state:
        st.session_state.download_ready = False
        st.session_state.file_data = None
        st.session_state.file_name = ""

    if st.button("Download Now 🎬", type="primary"):
        if not url:
            st.warning("⚠️ Please enter a valid YouTube URL.")
        else:
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            def my_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = d.get('_percent_str', '0%').replace('%','')
                        progress_bar.progress(int(float(p)))
                        status_placeholder.info(f"⚡ Downloading: {p}%")
                    except: pass
                if d['status'] == 'finished':
                    progress_bar.progress(100)

            # Create a temporary directory to store the file before serving it
            with tempfile.TemporaryDirectory() as tmp_dir:
                ydl_opts = {
                    'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [my_hook],
                    'nocheckcertificate': True,
                    'socket_timeout': 30,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9',
                    },
                }

                if format_choice == "Audio (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
                    })
                else:
                    ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'})

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        if format_choice == "Audio (MP3)":
                            file_path = file_path.rsplit('.', 1)[0] + ".mp3"
                        
                        with open(file_path, "rb") as f:
                            st.session_state.file_data = f.read()
                            st.session_state.file_name = os.path.basename(file_path)
                            st.session_state.download_ready = True
                    
                    status_placeholder.success("✅ Ready for saving!")
                except Exception as e:
                    status_placeholder.error(f"❌ Error: {str(e)}")
                    st.session_state.download_ready = False

    # Show the actual browser download button once processed
    if st.session_state.download_ready:
        st.download_button(
            label="💾 Click here to Save to PC",
            data=st.session_state.file_data,
            file_name=st.session_state.file_name,
            mime="video/mp4" if "MP4" in format_choice else "audio/mpeg",
            use_container_width=True
        )
        st.balloons()