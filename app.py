import re
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
    page_title="AI KHEMRA BRO",
    page_icon="ខ",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+Khmer:wght@400;500;600;700&display=swap');
      :root { --navy: #17243b; --coral: #ef7e57; --paper: #f7f2ea; }
      html, body, [class*="css"] { font-family: 'DM Sans', 'Noto Sans Khmer', sans-serif; }
      .stApp { background: var(--paper); color: var(--navy); }
      [data-testid="stSidebar"] { background: var(--navy); }
      [data-testid="stSidebar"] * { color: #f9f6f0; }
      .brand { display:flex; align-items:center; gap:14px; margin: 8px 0 28px; }
      .brand-mark { display:flex; align-items:center; justify-content:center; width:48px; height:48px; border-radius:16px; background:var(--coral); color:white; font-size:25px; font-weight:700; }
      .brand-title { font-size:20px; font-weight:700; letter-spacing:-.03em; }
      .eyebrow { color:#9a745f; font-size:11px; font-weight:700; letter-spacing:.17em; text-transform:uppercase; }
      h1 { color:var(--navy); font-size:clamp(2.2rem, 5vw, 4.3rem) !important; line-height:1.02 !important; letter-spacing:-.06em; margin:.35rem 0 .75rem !important; }
      h2, h3 { color:var(--navy); letter-spacing:-.03em; }
      .hero-copy { color:#68758a; font-size:16px; line-height:1.8; max-width:690px; }
      .stat { background:#fffdf9; border:1px solid #ded8ce; border-radius:18px; padding:15px 18px; text-align:center; }
      .stat-label { color:#929aa6; font-size:10px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
      .stat-value { color:var(--navy); font-size:28px; font-weight:700; }
      .panel { background:#fffdf9; border:1px solid #ded8ce; border-radius:22px; padding:24px; box-shadow:0 12px 34px rgba(59,47,34,.06); }
      .dark-panel { background:var(--navy); border-radius:22px; padding:24px; color:white; }
      .dark-panel h3, .dark-panel p { color:white; }
      .line-card { background:#fffdf9; border:1px solid #ebe3d8; border-radius:14px; padding:15px; margin:10px 0; }
      .time { color:#929aa6; font-family:monospace; font-size:12px; }
      .source { color:#33435b; font-size:15px; margin-top:7px; }
      .format-pill { display:inline-block; border-radius:999px; padding:4px 9px; background:#f1eee8; color:#8f8d88; font-size:10px; font-weight:700; letter-spacing:.12em; }
      .stButton > button { border-radius:12px; font-weight:600; }
      .stButton > button[kind="primary"] { background:var(--coral); border-color:var(--coral); }
      .stProgress > div > div > div > div { background:var(--coral); }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_from_name(name: str) -> str | None:
    extension = Path(name).suffix.lower().lstrip(".")
    return extension if extension in {"srt", "ass", "vtt"} else None


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


def show_translation_notice(message: str, kind: str = "info") -> None:
    if kind == "success":
        st.success(message)
    elif kind == "warning":
        st.warning(message)
    else:
        st.info(message)


def main() -> None:
    with st.sidebar:
        st.markdown('<div class="brand"><div class="brand-mark">ខ</div><div class="brand-title">AI KHEMRA BRO</div></div>', unsafe_allow_html=True)
        st.caption("Khmer-first AI workspace")
        page = st.radio("Menu", ["Home", "Subtitle Studio", "About"], label_visibility="collapsed")
        st.divider()
        st.caption("ភាសា / Language")
        st.selectbox("Language", ["ខ្មែរ + English", "ខ្មែរ", "English"], label_visibility="collapsed")

    if page == "Home":
        st.markdown('<div class="eyebrow">AI KHEMRA BRO · Khmer-first workspace</div>', unsafe_allow_html=True)
        st.title("Build useful AI tools\nfor Khmer people.")
        st.markdown('<p class="hero-copy">ស្វាគមន៍មកកាន់ AI KHEMRA BRO — កន្លែងសម្រាប់បង្កើត និងប្រើប្រាស់ឧបករណ៍ AI ដែលងាយស្រួល សាមញ្ញ និងគាំទ្រភាសាខ្មែរ។</p>', unsafe_allow_html=True)
        st.write("")
        left, right = st.columns([1.5, 1], gap="large")
        with left:
            st.markdown('<div class="panel"><div class="eyebrow">What we build</div><h2>Technology that feels closer to home.</h2><p>AI tools, translation workflows, automation, and web experiences designed with Khmer users in mind.</p></div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="dark-panel"><h3>Start here</h3><p>បើក Subtitle Studio ដើម្បីកែសម្រួល និងបកប្រែ subtitle ជាមួយ UI ដែលងាយប្រើ។</p></div>', unsafe_allow_html=True)
        st.write("")
        a, b, c = st.columns(3)
        for col, label, value in zip((a, b, c), ("Focus", "Languages", "Tools"), ("Khmer-first", "ខ្មែរ · English", "AI + Web")):
            with col:
                st.markdown(f'<div class="stat"><div class="stat-label">{label}</div><div class="stat-value">{value}</div></div>', unsafe_allow_html=True)

    elif page == "Subtitle Studio":
        st.markdown('<div class="eyebrow">Workspace / Subtitle Studio</div>', unsafe_allow_html=True)
        st.title("Make every line\nfeel natural.")
        st.markdown('<p class="hero-copy">បកប្រែ និងកែសម្រួល subtitle ចិនទៅខ្មែរ ជាមួយការគាំទ្រ .srt, .ass និង .vtt។</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop a subtitle file here", type=["srt", "ass", "vtt"], label_visibility="visible")
        if uploaded is not None:
            fmt = format_from_name(uploaded.name)
            text = uploaded.getvalue().decode("utf-8-sig", errors="replace")
            st.session_state.lines = parse_subtitle(text, fmt or "srt")
            st.session_state.file_name = uploaded.name
            st.session_state.format = fmt or "srt"
        if "lines" not in st.session_state:
            st.session_state.lines = demo_lines()
            st.session_state.file_name = "demo-scene.srt"
            st.session_state.format = "srt"

        lines = st.session_state.lines
        fmt = st.session_state.format
        translated = sum(1 for line in lines if line["target"].strip())
        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("Lines", len(lines))
        with p2:
            st.metric("Complete", f"{translated}/{len(lines)}")
        with p3:
            st.metric("Format", fmt.upper())
        st.progress(translated / len(lines) if lines else 0)

        st.markdown("### Story translation controls")
        st.caption("ជ្រើសរើសសកម្មភាពខាងក្រោម ដើម្បីបកប្រែរឿង និងរៀបចំឯកសាររបស់អ្នក។")
        selected_id = st.selectbox("Selected subtitle line", [line["id"] for line in lines], format_func=lambda value: f"Line {value:02d}")
        action_col_1, action_col_2 = st.columns(2, gap="medium")
        with action_col_1:
            if st.button("✨ Translate whole story", type="primary", use_container_width=True):
                show_translation_notice("ប៊ូតុងបកប្រែរឿងទាំងមូលរួចរាល់សម្រាប់ភ្ជាប់ AI translation service។ បច្ចុប្បន្ន អ្នកអាចកែសម្រួលខ្មែរដោយដៃតាមបន្ទាត់ខាងក្រោម។", "warning")
            if st.button("↗ Translate selected line", use_container_width=True):
                show_translation_notice(f"បានជ្រើសរើស Line {selected_id:02d}។ វានឹងបកប្រែជាខ្មែរនៅពេលភ្ជាប់ AI service។")
        with action_col_2:
            if st.button("↺ Reset demo story", use_container_width=True):
                st.session_state.lines = demo_lines()
                st.session_state.file_name = "demo-scene.srt"
                st.session_state.format = "srt"
                st.rerun()
            if st.button("⌫ Clear all Khmer translations", use_container_width=True):
                for line in lines:
                    line["target"] = ""
                show_translation_notice("បានលុបការបកប្រែខ្មែរទាំងអស់ចេញពី workspace។", "success")

        st.markdown("### File actions")
        controls = st.columns([1, 1, 1.4])
        with controls[0]:
            if st.button("Reset demo", use_container_width=True):
                st.session_state.lines = demo_lines()
                st.session_state.file_name = "demo-scene.srt"
                st.session_state.format = "srt"
                st.rerun()
        with controls[1]:
            if st.button("Clear translations", use_container_width=True):
                for line in lines:
                    line["target"] = ""
                st.rerun()
        with controls[2]:
            export = export_subtitle(lines, fmt)
            st.download_button("Download translated file", export, file_name=f"{Path(st.session_state.file_name).stem}-kh.{fmt}", mime="text/plain", use_container_width=True)

        st.markdown(f'<div class="panel"><span class="format-pill">{fmt.upper()}</span> <strong>{st.session_state.file_name}</strong><hr/>', unsafe_allow_html=True)
        for index, line in enumerate(lines):
            st.markdown('<div class="line-card">', unsafe_allow_html=True)
            st.markdown(f"<div class='time'>#{line['id']:02d} &nbsp; {line['start']} → {line['end']}</div><div class='source'>{line['source']}</div>", unsafe_allow_html=True)
            line["target"] = st.text_area("Khmer translation", value=line["target"], key=f"translation_{index}", placeholder="សរសេរការបកប្រែជាភាសាខ្មែរ…")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="eyebrow">About the project</div>', unsafe_allow_html=True)
        st.title("AI KHEMRA BRO")
        st.markdown('<p class="hero-copy">គម្រោងដែលផ្តោតលើការធ្វើឲ្យបច្ចេកវិទ្យា AI មានអារម្មណ៍ថាជិតស្និទ្ធ និងងាយប្រើសម្រាប់អ្នកប្រើប្រាស់ភាសាខ្មែរ។</p>', unsafe_allow_html=True)
        st.info("GitHub: github.com/kmr64681-create/AI-KHEMRA-BRO")
        st.markdown("### Direction\n\n- Khmer language tools\n- Practical AI workflows\n- Friendly interfaces\n- Open-source experiments")


if __name__ == "__main__":
    main()
