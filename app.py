import re
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import TypedDict

import streamlit as st


class SubtitleLine(TypedDict):
    id: int
    start: str
    end: str
    source: str
    target: str


st.set_page_config(
    page_title="AI KHEMRA BRO · AI Dubbing Workstation",
    page_icon="ខ",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+Khmer:wght@400;500;600;700&display=swap');
      :root { --navy: #0b0f18; --panel: #121827; --line: #263147; --cyan: #29d9f2; --pink: #ff20e7; --lime: #ccff42; }
      html, body, [class*="css"] { font-family: 'DM Sans', 'Noto Sans Khmer', sans-serif; }
      .stApp { background:var(--navy); color:#f4f7ff; }
      [data-testid="stSidebar"] { background:#111827; border-right:1px solid #263147; }
      [data-testid="stSidebar"] * { color:#f4f7ff; }
      .brand-card { border:1px solid #e020ff; border-radius:18px; padding:22px 16px; text-align:center; background:linear-gradient(145deg,#171a28,#0f1422); box-shadow:0 0 24px rgba(224,32,255,.22); margin:6px 0 18px; }
      .brand-mark { display:inline-flex; align-items:center; justify-content:center; width:50px; height:50px; border-radius:15px; background:linear-gradient(135deg,#ff22ea,#7b35ff); color:white; font-size:26px; font-weight:700; margin-bottom:10px; }
      .brand-name { color:white; font-size:22px; font-weight:700; letter-spacing:-.04em; }
      .brand-sub { color:#20e1f3; font-size:11px; font-weight:700; letter-spacing:.09em; margin-top:10px; }
      .profile-card { border:1px solid #1dd5ef; border-radius:15px; padding:14px; background:#101927; margin:14px 0 20px; }
      .profile-name { color:#f4f7ff; font-weight:700; }
      .eyebrow { color:var(--cyan); font-size:11px; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }
      h1 { color:#f7faff; font-size:clamp(2rem,4vw,3.2rem) !important; letter-spacing:-.06em; margin:.2rem 0 .6rem !important; }
      h2, h3 { color:#f7faff; letter-spacing:-.03em; }
      .hero-copy { color:#a9b6cb; font-size:15px; line-height:1.75; }
      .sample-header { border:2px solid #d92bff; border-radius:19px; padding:20px 26px 19px; text-align:center; background:linear-gradient(145deg,#171a28,#0e1420); box-shadow:0 0 30px rgba(217,43,255,.20); margin:0 auto 14px; max-width:920px; }
      .sample-header-title { color:#f9fbff; font-size:32px; font-weight:800; letter-spacing:-.04em; }
      .sample-header-sub { color:#1fe4ef; font-size:12px; font-weight:800; letter-spacing:.12em; margin-top:8px; }
      .sample-header-kh { color:#c7d2e4; font-size:13px; margin-top:10px; }
      .social-row { display:flex; justify-content:center; gap:10px; margin-top:14px; }
      .social-row a { color:#06111d; background:#20d9ed; border-radius:7px; padding:7px 15px; font-weight:700; font-size:12px; text-decoration:none; }
      .step-card { background:linear-gradient(135deg,#151d2f,#101625); border:1px solid #29364e; border-radius:18px; padding:22px; min-height:120px; }
      .step-num { display:inline-flex; width:30px; height:30px; align-items:center; justify-content:center; border-radius:9px; background:var(--cyan); color:#0b0f18; font-weight:800; margin-bottom:14px; }
      .step-card h3 { font-size:18px; margin:0 0 6px; }
      .step-card p { color:#9eacc0; font-size:13px; margin:0; line-height:1.55; }
      .dark-panel { background:linear-gradient(140deg,#171e31,#111722); border:1px solid #263147; border-radius:18px; padding:22px; }
      .status-pill { border:1px solid #4b5a73; background:#172236; color:#c7d2e4; border-radius:999px; padding:5px 10px; font-size:11px; font-weight:700; }
      .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #29354a; }
      .stTabs [data-baseweb="tab"] { color:#9dacbf; padding:12px 16px; }
      .stTabs [aria-selected="true"] { color:var(--cyan); border-bottom-color:var(--cyan); }
      .stButton > button, .stDownloadButton > button { border-radius:10px; font-weight:700; background:#1b2740; border:1px solid #35445d; color:#f4f7ff; }
      .stButton > button[kind="primary"] { background:linear-gradient(90deg,#ff1edf,#7e37ff); border-color:#ff1edf; color:white; }
      .stProgress > div > div > div > div { background:var(--cyan); }
      [data-testid="stFileUploader"] { background:#121a29; border:1px dashed #35506f; border-radius:15px; padding:10px; }
      textarea, input { background:#111a2a !important; color:#f4f7ff !important; }
      .stAlert { background:#172236; }
      .mobile-clear > button { background:#18d7ee; border-color:#18d7ee; color:#06111d; box-shadow:0 0 14px rgba(24,215,238,.35); }
      @media (max-width: 700px) {
        [data-testid="stSidebar"] { display:none; }
        [data-testid="stAppViewContainer"] > .main { padding:1.3rem .72rem 2rem; }
        .sample-header { margin-top:.15rem; padding:25px 14px 21px; }
        .sample-header-title { font-size:27px; }
        .sample-header-sub { font-size:9px; letter-spacing:.08em; }
        .sample-header-kh, .social-row { display:none; }
        .stTabs [data-baseweb="tab-list"] { gap:5px; }
        .stTabs [data-baseweb="tab"] { min-width:0; padding:9px 5px; font-size:10px; white-space:normal; text-align:center; }
        h2 { font-size:25px !important; line-height:1.15 !important; }
        .stButton > button, .stDownloadButton > button { min-height:38px; font-size:11px; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def make_line(index: int, start: str, end: str, source: str) -> SubtitleLine:
    return {"id": index, "start": start.strip(), "end": end.strip(), "source": source.strip(), "target": ""}


def parse_srt(text: str) -> list[SubtitleLine]:
    blocks = [b for b in re.split(r"\n\s*\n", text.replace("\r", "").strip()) if b.strip()]
    lines: list[SubtitleLine] = []
    for index, block in enumerate(blocks, 1):
        rows = block.splitlines()
        timing_index = next((i for i, row in enumerate(rows) if " --> " in row), -1)
        if timing_index < 0:
            continue
        cue_id = int(rows[0]) if rows[0].strip().isdigit() else index
        start, end = rows[timing_index].split(" --> ", 1)
        lines.append(make_line(cue_id, start, end, "\n".join(rows[timing_index + 1 :])))
    return lines


def parse_vtt(text: str) -> list[SubtitleLine]:
    clean = re.sub(r"^WEBVTT[^\n]*\n", "", text.replace("\r", ""), flags=re.I)
    blocks = [b for b in re.split(r"\n\s*\n", clean.strip()) if b.strip()]
    lines: list[SubtitleLine] = []
    for index, block in enumerate(blocks, 1):
        rows = block.splitlines()
        timing_index = next((i for i, row in enumerate(rows) if " --> " in row), -1)
        if timing_index < 0:
            continue
        start, end = rows[timing_index].split(" --> ", 1)
        lines.append(make_line(index, start, end.split()[0], "\n".join(rows[timing_index + 1 :])))
    return lines


def parse_ass(text: str) -> list[SubtitleLine]:
    lines: list[SubtitleLine] = []
    for row in text.replace("\r", "").splitlines():
        if not row.startswith("Dialogue:"):
            continue
        fields = row.removeprefix("Dialogue:").strip().split(",")
        if len(fields) < 10:
            continue
        source = ",".join(fields[9:]).replace(r"\N", "\n")
        lines.append(make_line(len(lines) + 1, fields[1], fields[2], source))
    return lines


def parse_subtitle(text: str, fmt: str) -> list[SubtitleLine]:
    if fmt == "ass":
        return parse_ass(text)
    if fmt == "vtt":
        return parse_vtt(text)
    return parse_srt(text)


def export_subtitle(lines: list[SubtitleLine], fmt: str) -> str:
    if fmt == "vtt":
        body = "\n\n".join(f"{line['id']}\n{line['start']} --> {line['end']}\n{line['target'] or line['source']}" for line in lines)
        return f"WEBVTT\n\n{body}\n"
    if fmt == "ass":
        header = "[Script Info]\nTitle: AI KHEMRA BRO translation\nScriptType: v4.00+\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        body = "\n".join(f"Dialogue: 0,{line['start']},{line['end']},Default,,0,0,0,,{(line['target'] or line['source']).replace(chr(10), r'\\N')}" for line in lines)
        return f"{header}\n{body}\n"
    return "\n\n".join(f"{line['id']}\n{line['start']} --> {line['end']}\n{line['target'] or line['source']}" for line in lines) + "\n"


def demo_lines() -> list[SubtitleLine]:
    return parse_srt("1\n00:00:02,000 --> 00:00:04,700\n你终于来了。\n\n2\n00:00:05,200 --> 00:00:08,000\n我等你很久了。\n\n3\n00:00:08,600 --> 00:00:12,000\n今晚的月亮，真的很漂亮。")


def load_demo() -> None:
    st.session_state.lines = demo_lines()
    st.session_state.file_name = "demo-scene.srt"
    st.session_state.format = "srt"


def google_translate(texts: list[str], api_key: str, source: str, target: str) -> list[str]:
    """Translate subtitle text with Google Cloud Translation Basic API v2."""
    if not api_key.strip():
        raise ValueError("សូមបញ្ចូល Google Translate API key ជាមុនសិន។")
    query = [("key", api_key.strip()), ("target", target), ("format", "text")]
    if source != "auto":
        query.append(("source", source))
    query.extend(("q", text) for text in texts)
    request = urllib.request.Request(
        "https://translate.googleapis.com/language/translate/v2?" + urllib.parse.urlencode(query),
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8")).get("error", {}).get("message", "Request rejected")
        except (json.JSONDecodeError, UnicodeDecodeError):
            detail = "Request rejected"
        raise RuntimeError(f"Google Translation API: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError("មិនអាចភ្ជាប់ Google Translation API បានទេ។") from error
    translations = payload.get("data", {}).get("translations", [])
    if len(translations) != len(texts):
        raise RuntimeError("Google Translation API បានឆ្លើយតបមិនពេញលេញ។")
    return [item.get("translatedText", "") for item in translations]


def configured_google_key() -> str:
    """Read an optional translation key from Streamlit secrets or the environment."""
    try:
        secret_key = str(st.secrets.get("GOOGLE_TRANSLATE_API_KEY", ""))
    except (FileNotFoundError, KeyError, RuntimeError):
        secret_key = ""
    return secret_key.strip() or os.environ.get("GOOGLE_TRANSLATE_API_KEY", "").strip()


def main() -> None:
    if "lines" not in st.session_state:
        load_demo()

    with st.sidebar:
        st.markdown('<div class="brand-card"><div class="brand-mark">ខ</div><div class="brand-name">AI KHEMRA BRO</div><div class="brand-sub">GLOBAL AI DUBBING & SUBTITLING</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-card"><div class="profile-name">👋 somevut036</div><div style="color:#f4f7ff;font-size:16px;margin-top:12px">ROLE: SOMEVUT036</div><div style="color:#f4f7ff;font-size:16px;margin-top:8px">🗓️ PLAN: 2027-06-30</div><div style="color:#f4f7ff;font-size:16px;font-weight:700;margin-top:8px">⌛ 289 DAYS LEFT</div></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.info("នេះជាកម្មវិធី demo ដោយមិនទាន់មាន account session។")
        st.markdown("### 🌍 Target Language (ភាសាគោលដៅ)")
        st.caption("ជ្រើសរើសភាសា (Select Language):")
        st.selectbox("Target language", ["Khmer (ខ្មែរ)", "English", "Thai", "Vietnamese"], label_visibility="collapsed", key="target_language")
        st.markdown("### 🔑 API Keys Manager")
        st.caption("Optional: paste Gemini API Keys (one per line)")
        gemini_api_keys = st.text_area("Gemini API keys", placeholder="", height=95, label_visibility="collapsed", key="gemini_api_keys")
        if gemini_api_keys.strip():
            st.success("Gemini key loaded for this session.")
        else:
            st.caption("Demo mode: subtitle upload, editing, export, and sample data work without an AI key.")
        st.markdown("### 🎭 Translation Style")
        st.caption("ជ្រើសរើសប្រភពបកប្រែ (Translate API):")
        translation_provider = st.radio("Translate API", ["Gemini API", "Google API"], label_visibility="collapsed", key="translation_provider")
        google_api_key = st.text_input("Google API key", value=configured_google_key(), type="password", placeholder="Google API key (AIza…)", key="google_translation_api_key")
        google_source = st.selectbox("Source language", [("auto", "Auto detect"), ("zh-CN", "Chinese (简体中文)"), ("en", "English")], format_func=lambda item: item[1], key="google_source_language")
        google_target = st.selectbox("Google target language", [("km", "Khmer (ខ្មែរ)"), ("en", "English"), ("th", "Thai")], format_func=lambda item: item[1], key="google_target_language")
        if st.button("Test Google API key", use_container_width=True):
            try:
                google_translate(["Hello"], google_api_key, google_source[0], google_target[0])
                st.success("Google Translation API key ដំណើរការ។")
            except (ValueError, RuntimeError) as error:
                st.error(str(error))
        st.markdown("### ⚙️ Audio Sync Mode")
        st.caption("ជ្រើសរើសល្បឿនសំឡេង:")
        st.radio("Audio sync", ["Speed Up Only (លឿន)", "Speed Up & Slow Down (លឿន និង យឺត)"], label_visibility="collapsed", key="audio_sync_mode")
        st.markdown("### 🗣️ Voice Mode (ជ្រើសរើសសំឡេង)")
        st.caption("កំណត់សំឡេងសម្រាប់ Tab 1 & Tab 2:")
        st.radio("Voice mode", ["Auto (ប្រុស/ស្រី តាម Tag)", "All Male (ប្រុសសុទ្ធ)", "All Female (ស្រីសុទ្ធ)"], label_visibility="collapsed", key="voice_mode")
        st.selectbox("AI model", ["Demo / local UI", "Gemini Flash (requires provider)", "Gemini Pro (requires provider)"], label_visibility="collapsed", key="ai_model")

    st.markdown('<div class="sample-header"><div class="sample-header-title">AI KHEMRA BRO</div><div class="sample-header-sub">GLOBAL KHMER AI DUBBING WORKSTATION</div><div class="sample-header-kh">បកប្រែ subtitle និងបង្កើតសំឡេងខ្មែរ ក្នុងកម្មវិធីតែមួយ</div><div class="social-row"><a href="https://github.com/kmr64681-create/AI-KHEMRA-BRO" target="_blank">💻 GitHub</a><a href="https://github.com/kmr64681-create/AI-KHEMRA-BRO/issues" target="_blank">🛠️ Support</a></div></div>', unsafe_allow_html=True)

    tabs = st.tabs(["📹 Video → SRT", "🗎 AI Subtitle Translator", "📜 SRT → Speech", "🎙️ Text → Speech"])

    with tabs[0]:
        st.markdown("## 1️⃣ Generate Subtitles (Khmer (ខ្មែរ))")
        video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv"], key="video_upload")
        if video:
            st.success(f"បាន upload: {video.name} · {video.size / 1024 / 1024:.1f} MB")
        st.markdown("### Generated SRT")
        st.caption("You can edit the SRT here before generating audio:")
        st.text_area("Generated SRT", placeholder="Generated subtitle text will appear here after connecting a transcription model…", height=210, label_visibility="collapsed")
        c1, c2 = st.columns(2)
        with c1:
            st.write("")
        with c2:
            if st.button("🧠 Analyze Inner Thoughts", type="primary", use_container_width=True):
                st.info("Video transcription UI is ready. Connect a speech-to-text model to generate timestamps automatically.")
        st.markdown("## 2️⃣ AI Dubbing (Edge TTS Studio)")
        if st.button("🎙️ Generate Dubbed Audio (MP3)", type="primary"):
            st.info("ភ្ជាប់ Edge TTS provider ដើម្បីបង្កើតសំឡេង dubbing ជា MP3។")
        st.markdown('<div class="mobile-clear">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Video Project", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("## AI SRT Translator")
        st.caption("Upload subtitle → review original text → translate into Khmer → download.")
        uploaded = st.file_uploader("Upload .srt, .ass, or .vtt", type=["srt", "ass", "vtt"], key="subtitle_upload")
        if uploaded:
            fmt = Path(uploaded.name).suffix.lower().lstrip(".")
            text = uploaded.getvalue().decode("utf-8-sig", errors="replace")
            parsed = parse_subtitle(text, fmt)
            if parsed:
                st.session_state.lines = parsed
                st.session_state.file_name = uploaded.name
                st.session_state.format = fmt
                st.success(f"បានផ្ទុក {len(parsed)} បន្ទាត់ · {fmt.upper()}")
            else:
                st.error("រកមិនឃើញ subtitle lines ក្នុងឯកសារនេះទេ")

        lines = st.session_state.lines
        fmt = st.session_state.format
        translated = sum(1 for line in lines if line["target"].strip())
        m1, m2, m3 = st.columns(3)
        m1.metric("Subtitle lines", len(lines))
        m2.metric("Translated", f"{translated}/{len(lines)}")
        m3.metric("Format", fmt.upper())
        st.progress(translated / len(lines) if lines else 0)
        st.markdown(f'<span class="status-pill">{st.session_state.file_name}</span>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("✨ Translate whole story", type="primary", use_container_width=True):
                try:
                    translated_text = google_translate([line["source"] for line in lines], google_api_key, google_source[0], google_target[0])
                    for line, result in zip(lines, translated_text):
                        line["target"] = result
                    st.success(f"បានបកប្រែ {len(translated_text)} បន្ទាត់ដោយ Google Translate។")
                except (ValueError, RuntimeError) as error:
                    st.error(str(error))
        with c2:
            line_ids = [line["id"] for line in lines]
            selected_id = st.selectbox("Line", line_ids, format_func=lambda value: f"Line {value:02d}", label_visibility="collapsed")
            if st.button("Translate line", use_container_width=True):
                selected_line = next(line for line in lines if line["id"] == selected_id)
                try:
                    selected_line["target"] = google_translate([selected_line["source"]], google_api_key, google_source[0], google_target[0])[0]
                    st.success(f"Line {selected_id:02d} បានបកប្រែដោយ Google Translate។")
                except (ValueError, RuntimeError) as error:
                    st.error(str(error))
        with c3:
            export = export_subtitle(lines, fmt)
            st.download_button("⬇️ Download", export, file_name=f"{Path(st.session_state.file_name).stem}-kh.{fmt}", mime="text/plain", use_container_width=True)
        with c4:
            if st.button("↺ Reset", use_container_width=True):
                load_demo()
                st.rerun()
        with c5:
            if st.button("⌫ Clear", use_container_width=True):
                for line in lines:
                    line["target"] = ""
                st.success("បានលុបការបកប្រែខ្មែរទាំងអស់។")

        st.markdown("### Review and edit Khmer translation")
        for index, line in enumerate(lines):
            with st.container(border=True):
                st.caption(f"#{line['id']:02d} · {line['start']} → {line['end']}")
                st.write(line["source"])
                line["target"] = st.text_area("Khmer", value=line["target"], key=f"target_{index}", placeholder="បញ្ចូលការបកប្រែខ្មែរ…", label_visibility="collapsed")

    with tabs[2]:
        st.markdown("## Subtitle to Speech")
        st.caption("បម្លែង subtitle ដែលបានបកប្រែទៅជាសំឡេងខ្មែរ។")
        st.text_area("SRT text", value=export_subtitle(st.session_state.lines, st.session_state.format), height=200)
        voice = st.selectbox("Voice", ["Khmer Female 01", "Khmer Male 01", "Khmer Neutral"], key="subtitle_speech_voice")
        if st.button("🎙️ Generate Khmer Audio", type="primary"):
            st.info(f"Voice {voice} ត្រូវបានជ្រើសរើស។ ភ្ជាប់ TTS provider ដើម្បីបង្កើត MP3/WAV។")

    with tabs[3]:
        st.markdown("## Text-to-Speech")
        st.text_area("Text to speak", placeholder="សរសេរអត្ថបទខ្មែរនៅទីនេះ…", height=190)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Voice", ["Khmer Female 01", "Khmer Male 01", "Khmer Neutral"], key="tts_voice")
        with c2:
            st.slider("Speed", 0.7, 1.3, 1.0, 0.05)
        if st.button("🔊 Generate speech", type="primary", use_container_width=True):
            st.info("Text-to-Speech UI ត្រូវបានរៀបចំរួច។ ភ្ជាប់ speech provider ដើម្បីទទួលបាន audio file។")


if __name__ == "__main__":
    main()
