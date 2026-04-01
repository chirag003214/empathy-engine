import os
import sys
import streamlit as st

# ── allow imports from this folder when run from a different cwd ──
sys.path.insert(0, os.path.dirname(__file__))
os.makedirs("static", exist_ok=True)

# ── page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Empathy Engine",
    page_icon="🎙",
    layout="centered",
)

# ── cached model load (runs once per session) ────────────────────
@st.cache_resource(show_spinner="Loading emotion model (~300 MB on first run)…")
def load_modules():
    from emotion import detect_emotion
    from tts_engine import synthesize, get_voice_params
    return detect_emotion, synthesize, get_voice_params

detect_emotion, synthesize, get_voice_params = load_modules()

# ── constants ─────────────────────────────────────────────────────
EMOTION_COLORS = {
    "joy":      "#f59e0b",
    "surprise": "#8b5cf6",
    "anger":    "#ef4444",
    "sadness":  "#3b82f6",
    "fear":     "#6366f1",
    "disgust":  "#10b981",
    "neutral":  "#6b7280",
}

EXAMPLES = [
    "I just got promoted! This is the best day of my life!",
    "I can't believe they cancelled my order again. This is unacceptable.",
    "The meeting is scheduled for 3pm tomorrow.",
    "I'm not sure if I can handle this situation.",
]

OUTPUT_PATH = "static/output.wav"

# ── custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
/* card-like container */
section.main > div { max-width: 680px; margin: auto; }

/* hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* emotion badge */
.emotion-badge {
    display: inline-block;
    padding: 0.28rem 1.1rem;
    border-radius: 999px;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    text-transform: capitalize;
    letter-spacing: 0.03em;
}

/* confidence bar container */
.bar-wrap {
    background: #e2e8f0;
    border-radius: 999px;
    height: 12px;
    overflow: hidden;
    margin: 0.4rem 0 0.2rem;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* param box */
.param-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    text-align: center;
}
.param-key { font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
.param-val { font-size: 1.3rem; font-weight: 700; color: #1e293b; margin-top: 0.1rem; }

/* example chip buttons */
div[data-testid="stHorizontalBlock"] button {
    font-size: 0.78rem !important;
    padding: 0.25rem 0.7rem !important;
    border-radius: 999px !important;
}
</style>
""", unsafe_allow_html=True)

# ── header ────────────────────────────────────────────────────────
st.markdown("## 🎙 Empathy Engine")
st.caption("AI-powered emotional text-to-speech")
st.divider()

# ── session state ─────────────────────────────────────────────────
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ── example chips ─────────────────────────────────────────────────
st.markdown("**Examples**")
cols = st.columns(2)
for i, ex in enumerate(EXAMPLES):
    if cols[i % 2].button(ex[:55] + "…" if len(ex) > 55 else ex, key=f"ex_{i}"):
        st.session_state.input_text = ex
        st.rerun()

# ── text input ───────────────────────────────────────────────────
text = st.text_area(
    "Your text",
    value=st.session_state.input_text,
    placeholder="Type or paste any sentence here…",
    height=130,
    label_visibility="collapsed",
)

analyze_clicked = st.button("🔍 Analyze & Speak", type="primary", use_container_width=True)

# ── analysis ─────────────────────────────────────────────────────
if analyze_clicked:
    clean = text.strip()
    if not clean:
        st.error("Please enter some text before analyzing.")
    else:
        with st.spinner("Detecting emotion and synthesising speech…"):
            result = detect_emotion(clean)
            emotion   = result["emotion"]
            intensity = result["intensity"]
            synthesize(clean, emotion, intensity, OUTPUT_PATH)
            params = get_voice_params(emotion, intensity)

        st.session_state["last_result"] = {
            "emotion":   emotion,
            "intensity": intensity,
            "params":    params,
            "audio":     OUTPUT_PATH,
        }

# ── results panel ─────────────────────────────────────────────────
if "last_result" in st.session_state:
    r = st.session_state["last_result"]
    emotion   = r["emotion"]
    intensity = r["intensity"]
    params    = r["params"]
    color     = EMOTION_COLORS.get(emotion, "#6b7280")
    pct       = round(intensity * 100)

    st.divider()

    # Emotion badge
    col_lbl, col_val = st.columns([1, 3])
    col_lbl.markdown("<div style='padding-top:0.45rem; color:#94a3b8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em;'>EMOTION</div>", unsafe_allow_html=True)
    col_val.markdown(
        f"<span class='emotion-badge' style='background:{color}'>{emotion}</span>",
        unsafe_allow_html=True,
    )

    # Confidence bar
    col_lbl2, col_val2 = st.columns([1, 3])
    col_lbl2.markdown("<div style='padding-top:0.6rem; color:#94a3b8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em;'>CONFIDENCE</div>", unsafe_allow_html=True)
    col_val2.markdown(
        f"""
        <div class='bar-wrap'>
          <div class='bar-fill' style='width:{pct}%; background:{color}'></div>
        </div>
        <div style='font-size:0.85rem; font-weight:600; color:#475569; text-align:right'>{pct}%</div>
        """,
        unsafe_allow_html=True,
    )

    # Voice params
    col_lbl3, col_r, col_v = st.columns([1, 1.5, 1.5])
    col_lbl3.markdown("<div style='padding-top:0.8rem; color:#94a3b8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em;'>VOICE</div>", unsafe_allow_html=True)
    col_r.markdown(f"<div class='param-box'><div class='param-key'>Rate</div><div class='param-val'>{params['rate']}</div></div>", unsafe_allow_html=True)
    col_v.markdown(f"<div class='param-box'><div class='param-key'>Volume</div><div class='param-val'>{params['volume']:.2f}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # Audio player
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/wav", autoplay=True)
