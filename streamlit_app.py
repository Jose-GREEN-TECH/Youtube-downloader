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

# Premium Custom CSS (Jose's Original Design)
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
    button[kind="primary"] {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%) !important;
        border-radius: 50px !important; font-weight: 700 !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Application Logic
with st.container():
    st.markdown("<h1>Ultra Downloader 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p>Download YouTube Videos & Audio securely to your device.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: #00C9FF; text-align: center; margin-top: -10px;'>✨ Designed by Jose ✨</p>", unsafe_allow_html=True)
    
    url = st.text_input("🔗 YouTube Link", placeholder="https://www.youtube.com/watch?v=...")
    format_choice = st.selectbox("📂 Format", ["Video (MP4)", "Audio (MP3)"])

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("Download Now 🎬", type="primary"):
        if not url:
            st.warning("⚠️ Please enter a valid YouTube URL.")
        else:
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            def my_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p_str = d.get('_percent_str', '0%').replace('%','').strip()
                        p_float = float(''.join(c for c in p_str if c.isdigit() or c == '.'))
                        progress_bar.progress(int(p_float))
                        status_placeholder.info(f"⚡ Processing: {p_str}%")
                    except: pass

            with tempfile.TemporaryDirectory() as tmp_dir:
                # ADVANCED CONFIG TO BYPASS 403 FORBIDDEN
                ydl_opts = {
                    'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [my_hook],
                    'nocheckcertificate': True,
                    # Browser Impersonation
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    # Link to your uploaded cookies file
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                    # Modern YouTube protocol bypass
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
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
                        status_placeholder.info("🔍 Bypassing security...")
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        
                        # Correct extension for MP3 post-processing
                        if format_choice == "Audio (MP3)":
                            file_path = os.path.splitext(file_path)[0] + ".mp3"
                        
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                            st.download_button(
                                label="💾 Save to PC",
                                data=file_bytes,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4" if "MP4" in format_choice else "audio/mpeg",
                                use_container_width=True
                            )
                    
                    status_placeholder.success("✅ Download Prepared Successfully!")
                    st.balloons()
                except Exception as e:
                    status_placeholder.error(f"❌ Critical Error: {str(e)}")
                    st.info("💡 Hint: Ensure 'cookies.txt' is uploaded to GitHub and hasn't expired.")
