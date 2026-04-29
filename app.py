# app.py — Mood Flow · Complete Redesign · Professional Light Theme

import streamlit as st
import sys
import os
import html

sys.path.insert(0, os.path.dirname(__file__))

from engine import MoodClassifier, UserMemory, RecommendationEngine
from data import MOOD_META


st.set_page_config(
    page_title="Mood Flow",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --bg:#F0F2F8;
  --white:#FFFFFF;
  --surface:#FAFBFF;
  --border:#E2E8F6;
  --border2:#C9D4EE;
  --text:#0F1523;
  --text2:#3D4769;
  --muted:#8993B3;
  --accent:#4F46E5;
  --accent-h:#3730C4;
  --accent-lt:#EEF0FD;
  --green:#10B981;
  --amber:#F59E0B;
  --red:#EF4444;
  --r:16px;
  --r-sm:10px;
  --sh1:0 1px 4px rgba(15,21,35,.05), 0 4px 16px rgba(15,21,35,.04);
  --sh2:0 2px 8px rgba(15,21,35,.06), 0 8px 32px rgba(15,21,35,.06);
}

html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],
.main,.main .block-container{
  background:var(--bg) !important;
  color:var(--text) !important;
  font-family:'Inter',sans-serif !important;
}

.block-container{
  padding:2rem 2.5rem 4rem !important;
  max-width:1180px !important;
}

#MainMenu,footer,header,[data-testid="stDecoration"],
.stDeployButton,[data-testid="stStatusWidget"]{
  display:none !important;
  visibility:hidden !important;
}

h1,h2,h3,h4{
  font-family:'Plus Jakarta Sans',sans-serif !important;
  color:var(--text) !important;
}

/* Sidebar */
[data-testid="stSidebar"]{
  background:var(--white) !important;
  border-right:1px solid var(--border) !important;
  box-shadow:2px 0 20px rgba(15,21,35,.04) !important;
}

[data-testid="stSidebar"] *:not([class*="material"]):not([data-testid="stIconMaterial"]){
  font-family:'Inter',sans-serif !important;
  color:var(--text) !important;
}

section[data-testid="stSidebar"]{
  min-width:260px !important;
  max-width:300px !important;
  width:280px !important;
  display:flex !important;
  visibility:visible !important;
  transform:none !important;
}

/* Hide Streamlit sidebar collapse raw icon text */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebar"] button[title="Close sidebar"],
[data-testid="stSidebar"] button[aria-label="Close sidebar"],
button[title="Close sidebar"],
button[aria-label="Close sidebar"],
button[title="Open sidebar"],
button[aria-label="Open sidebar"]{
  display:none !important;
  visibility:hidden !important;
  opacity:0 !important;
  width:0 !important;
  height:0 !important;
  overflow:hidden !important;
  pointer-events:none !important;
}

span[class*="material"],
i[class*="material"],
[data-testid="stIconMaterial"]{
  font-family:"Material Symbols Rounded","Material Icons" !important;
  font-size:0 !important;
  display:none !important;
}

/* Inputs */
input,[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea{
  background:var(--white) !important;
  border:1.5px solid var(--border2) !important;
  border-radius:var(--r-sm) !important;
  color:var(--text) !important;
  font-family:'Inter',sans-serif !important;
  font-size:.95rem !important;
  box-shadow:var(--sh1) !important;
  resize:none !important;
}

input:focus,[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus{
  border-color:var(--accent) !important;
  box-shadow:0 0 0 3px rgba(79,70,229,.12) !important;
  outline:none !important;
}

/* Buttons */
[data-testid="stButton"]>button{
  background:var(--white) !important;
  color:var(--text) !important;
  border:1.5px solid var(--border2) !important;
  border-radius:var(--r-sm) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:700 !important;
  font-size:.88rem !important;
  padding:.5rem 1.2rem !important;
  box-shadow:none !important;
  cursor:pointer !important;
}

[data-testid="stButton"]>button:hover{
  background:var(--surface) !important;
  border-color:var(--accent) !important;
  transform:translateY(-1px) !important;
}

[data-testid="stButton"]>button[kind="primary"]{
  background:var(--accent) !important;
  color:#fff !important;
  border:none !important;
  box-shadow:0 2px 10px rgba(79,70,229,.28) !important;
}

[data-testid="stButton"]>button[kind="primary"]:hover{
  background:var(--accent-h) !important;
}

/* Welcome */
.wcard{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:20px;
  padding:2.5rem 2.5rem 2rem;
  box-shadow:var(--sh2);
  max-width:520px;
  margin:2rem auto;
}

.wcard-logo{
  width:52px;
  height:52px;
  border-radius:14px;
  background:linear-gradient(135deg,#4F46E5,#818CF8);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1.5rem;
  box-shadow:0 4px 14px rgba(79,70,229,.35);
  margin-bottom:1.25rem;
}

.wcard-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.7rem;
  font-weight:800;
  color:var(--text);
  margin-bottom:.3rem;
}

.wcard-sub{
  font-size:.9rem;
  color:var(--muted);
  line-height:1.6;
  margin-bottom:1.5rem;
}

.input-lbl{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.72rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:var(--muted);
  margin-bottom:.35rem;
}

.mood-chips{
  display:flex;
  flex-wrap:wrap;
  gap:7px;
  margin-top:1.4rem;
}

.mood-chip{
  display:inline-flex;
  align-items:center;
  gap:5px;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:50px;
  padding:5px 12px;
  font-size:.73rem;
  font-weight:600;
  color:var(--text2);
  box-shadow:var(--sh1);
}

/* Topbar */
.topbar{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:1.2rem 1.5rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  box-shadow:var(--sh1);
  margin-bottom:1.2rem;
}

.topbar-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.25rem;
  font-weight:800;
  color:var(--text);
}

.topbar-sub{
  font-size:.78rem;
  color:var(--muted);
  margin-top:1px;
}

.session-pill{
  display:inline-flex;
  align-items:center;
  gap:5px;
  background:var(--accent-lt);
  border:1px solid rgba(79,70,229,.2);
  border-radius:50px;
  padding:4px 13px;
  font-size:.7rem;
  font-weight:700;
  color:var(--accent);
}

/* Input section */
.input-section{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:1.4rem 1.5rem 1.1rem;
  box-shadow:var(--sh1);
  margin-bottom:1rem;
}

.example-row{
  font-size:.74rem;
  color:var(--muted);
  margin-top:.5rem;
  line-height:1.65;
}

.example-row b{
  color:var(--text2);
  font-weight:600;
}

/* Mood banner */
.mood-banner{
  border-radius:var(--r);
  padding:1.35rem 1.5rem;
  border:1.5px solid;
  margin-bottom:1rem;
  position:relative;
  overflow:hidden;
}

.mood-banner::after{
  content:'';
  position:absolute;
  right:-30px;
  top:-30px;
  width:130px;
  height:130px;
  border-radius:50%;
  background:currentColor;
  opacity:.06;
}

.det-lbl{
  font-size:.65rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.1em;
  opacity:.6;
  margin-bottom:5px;
}

.mood-row{
  display:flex;
  align-items:center;
  gap:10px;
}

.mood-emo{
  font-size:2rem;
  line-height:1;
}

.mood-name{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.65rem;
  font-weight:800;
  line-height:1;
}

.mood-desc{
  font-size:.84rem;
  opacity:.75;
  margin-top:5px;
  line-height:1.5;
}

.mood-quote{
  font-size:.77rem;
  font-style:italic;
  border-top:1px solid;
  opacity:.55;
  margin-top:9px;
  padding-top:9px;
  line-height:1.5;
}

/* Confidence */
.conf-card{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:.95rem 1.1rem;
  box-shadow:var(--sh1);
  height:100%;
}

.conf-title{
  font-size:.65rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:var(--muted);
  margin-bottom:.7rem;
}

.cbar{
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:6px;
}

.cbar-lbl{
  width:68px;
  font-size:.74rem;
  color:var(--text2);
  font-weight:500;
  flex-shrink:0;
}

.cbar-track{
  flex:1;
  background:var(--bg);
  border-radius:4px;
  height:6px;
  overflow:hidden;
}

.cbar-fill{
  height:100%;
  border-radius:4px;
}

.cbar-pct{
  font-size:.7rem;
  color:var(--muted);
  width:28px;
  text-align:right;
  flex-shrink:0;
}

/* Recommendations */
.rec-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:2rem;
  font-weight:800;
  color:var(--text);
  margin:1.8rem 0 1.4rem;
}

.rec-row{
  background:#F8FAFC;
  border-left:6px solid var(--amber);
  border-radius:10px;
  padding:1.6rem 1.75rem;
  min-height:120px;
  display:flex;
  flex-direction:column;
  justify-content:center;
}

.rec-action{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.25rem;
  font-weight:800;
  color:var(--text);
  line-height:1.45;
  margin-bottom:.9rem;
}

.rec-score{
  font-size:.95rem;
  color:var(--text2);
  font-weight:500;
}

.rec-score span{
  font-weight:800;
  color:var(--text);
}

.rec-saved{
  font-size:.78rem;
  color:var(--green);
  font-weight:800;
  text-align:center;
  margin-top:2.65rem;
}

[data-testid="column"]{
  padding:0 5px !important;
}

/* Sidebar content */
.sb-logo{
  display:flex;
  align-items:center;
  gap:9px;
  padding:.4rem 0 .9rem;
}

.sb-logo-icon{
  width:32px;
  height:32px;
  border-radius:9px;
  background:linear-gradient(135deg,#4F46E5,#818CF8);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1rem;
  box-shadow:0 2px 8px rgba(79,70,229,.3);
}

.sb-logo-name{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.05rem;
  font-weight:800;
  color:var(--text);
}

.sb-logo-name span{
  color:var(--accent);
}

.sb-user{
  background:linear-gradient(135deg,var(--accent-lt),#F0F4FF);
  border:1px solid rgba(79,70,229,.18);
  border-radius:12px;
  padding:.8rem .95rem;
  display:flex;
  align-items:center;
  gap:9px;
  margin-bottom:.9rem;
}

.sb-av{
  width:36px;
  height:36px;
  border-radius:50%;
  background:linear-gradient(135deg,#4F46E5,#818CF8);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:'Plus Jakarta Sans',sans-serif;
  font-weight:800;
  font-size:.95rem;
  color:#fff;
  flex-shrink:0;
}

.sb-uname{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-weight:700;
  font-size:.88rem;
  color:var(--text);
}

.sb-usub{
  font-size:.67rem;
  color:var(--muted);
  margin-top:1px;
}

.sb-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:7px;
  margin-bottom:.9rem;
}

.sb-stat{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:10px;
  padding:.65rem .8rem;
  text-align:center;
  box-shadow:var(--sh1);
}

.sb-stat-n{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.45rem;
  font-weight:800;
  color:var(--text);
  line-height:1;
}

.sb-stat-l{
  font-size:.62rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.06em;
  color:var(--muted);
  margin-top:2px;
}

.sb-sec{
  font-size:.63rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:var(--muted);
  margin:.9rem 0 .45rem;
}

.sb-hist-item{
  display:flex;
  align-items:flex-start;
  gap:7px;
  padding:6px 0;
  border-bottom:1px solid var(--border);
}

.sb-dot{
  width:7px;
  height:7px;
  border-radius:50%;
  margin-top:5px;
  flex-shrink:0;
}

.sb-hmood{
  font-size:.73rem;
  font-weight:700;
  line-height:1.25;
}

.sb-hsnip{
  font-size:.67rem;
  color:var(--muted);
  line-height:1.3;
}

.sb-hdate{
  font-size:.6rem;
  color:#BBC4DB;
  margin-top:1px;
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def _clf():
    c = MoodClassifier()
    c.train()
    return c


@st.cache_resource
def _mem():
    return UserMemory()


@st.cache_resource
def _eng(_m):
    return RecommendationEngine(_m)


clf = _clf()
memory = _mem()
engine = _eng(memory)


def fresh_defaults():
    return {
        "page": "welcome",
        "uid": None,
        "username": None,
        "current_mood": None,
        "current_recs": [],
        "confidence": {},
        "feedback_given": set(),
        "last_input": "",
    }


for k, v in fresh_defaults().items():
    if k not in st.session_state:
        st.session_state[k] = v


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sb-logo">'
            '<div class="sb-logo-icon">🌊</div>'
            '<div class="sb-logo-name">Mood<span> Flow</span></div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<hr style="margin:.1rem 0 .9rem">', unsafe_allow_html=True)

        if not st.session_state.uid:
            st.markdown(
                '<p style="font-size:.82rem;color:#8993B3;line-height:1.65;">'
                'Log in on the main screen to see your personal profile, mood history, and stats here.'
                '</p>',
                unsafe_allow_html=True,
            )
            return

        uid = st.session_state.uid
        name = st.session_state.username

        st.markdown(
            f'<div class="sb-user">'
            f'<div class="sb-av">{html.escape(name[0].upper())}</div>'
            f'<div>'
            f'<div class="sb-uname">{html.escape(name)}</div>'
            f'<div class="sb-usub">Personalised profile active</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        sessions = memory.total_sessions(uid)
        liked_cnt = len(memory.liked_actions(uid))

        st.markdown(
            f'<div class="sb-grid">'
            f'<div class="sb-stat"><div class="sb-stat-n">{sessions}</div><div class="sb-stat-l">Check-ins</div></div>'
            f'<div class="sb-stat"><div class="sb-stat-n">{liked_cnt}</div><div class="sb-stat-l">Liked</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        freq = memory.mood_frequency(uid)
        if freq:
            top = list(freq.keys())[0]
            meta = MOOD_META.get(top, {})
            color = meta.get("color", "#4F46E5")

            st.markdown(
                f'<div style="font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:.3rem;">Most Frequent</div>'
                f'<div style="display:inline-flex;align-items:center;gap:6px;background:{color}14;border:1px solid {color}33;border-radius:50px;padding:4px 12px;margin-bottom:.2rem;">'
                f'<span>{meta.get("emoji", "")}</span>'
                f'<span style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;font-size:.8rem;color:{color};">{html.escape(top.title())}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        recent = memory.recent_history(uid, 6)
        if recent:
            st.markdown('<div class="sb-sec">Recent Check-ins</div>', unsafe_allow_html=True)

            sidebar_html = ""
            for entry in recent:
                mood = entry.get("mood", "happy")
                meta = MOOD_META.get(mood, {})
                color = meta.get("color", "#4F46E5")
                raw_input = entry.get("input", entry.get("text", ""))
                snip = raw_input[:38] + "..." if len(raw_input) > 38 else raw_input
                ts = entry.get("timestamp", entry.get("date", ""))[:10]

                sidebar_html += (
                    f'<div class="sb-hist-item">'
                    f'<div class="sb-dot" style="background:{color}"></div>'
                    f'<div>'
                    f'<div class="sb-hmood" style="color:{color}">{meta.get("emoji", "")} {html.escape(mood.title())}</div>'
                    f'<div class="sb-hsnip">{html.escape(snip)}</div>'
                    f'<div class="sb-hdate">{html.escape(ts)}</div>'
                    f'</div>'
                    f'</div>'
                )

            st.markdown(sidebar_html, unsafe_allow_html=True)

        st.markdown('<hr style="margin:.9rem 0 .7rem">', unsafe_allow_html=True)

        if st.button("↩  Switch User", use_container_width=True):
            st.session_state.update(fresh_defaults())
            st.rerun()


def render_conf_bars(conf: dict):
    st.markdown('<div class="conf-title">Model Confidence</div>', unsafe_allow_html=True)

    bars_html = ""
    for mood, prob in list(conf.items())[:4]:
        meta = MOOD_META.get(mood, {})
        color = meta.get("color", "#4F46E5")
        pct = int(prob * 100)

        bars_html += (
            f'<div class="cbar">'
            f'<div class="cbar-lbl">{meta.get("emoji", "")} {html.escape(mood.title())}</div>'
            f'<div class="cbar-track"><div class="cbar-fill" style="width:{pct}%;background:{color}"></div></div>'
            f'<div class="cbar-pct">{pct}%</div>'
            f'</div>'
        )

    st.markdown(bars_html, unsafe_allow_html=True)


def render_action_card(rec, idx: int, mood: str, uid: str):
    if isinstance(rec, str):
        rec = {"id": rec, "action": rec, "score": 5.0}
    elif not isinstance(rec, dict):
        rec = {"id": f"{mood[:2]}{idx}", "action": str(rec), "score": 5.0}

    aid = rec.get("id", f"{mood[:2]}{idx}")
    action_text = rec.get("action", str(rec))
    score = float(rec.get("score", 5.0))
    already = aid in st.session_state.feedback_given

    relevance = min(100, max(50, int(((score - 5.0) / 3.0 + 1.0) * 100)))

    meta = MOOD_META.get(mood, {})
    color = meta.get("color", "#F59E0B")

    card_col, like_col, dislike_col = st.columns([8, 0.8, 0.8])

    with card_col:
        st.markdown(
            f"""
            <div class="rec-row" style="border-left-color:{color};">
                <div class="rec-action">{html.escape(action_text)}</div>
                <div class="rec-score">Relevance: <span>{relevance}%</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if already:
        with like_col:
            st.markdown('<div class="rec-saved">Saved</div>', unsafe_allow_html=True)
    else:
        with like_col:
            if st.button("👍", key=f"L_{aid}_{idx}", help="Helpful"):
                memory.record_feedback(uid, aid, mood, "liked")
                st.session_state.feedback_given.add(aid)
                st.rerun()

        with dislike_col:
            if st.button("👎", key=f"D_{aid}_{idx}", help="Not for me"):
                memory.record_feedback(uid, aid, mood, "disliked")
                st.session_state.feedback_given.add(aid)
                st.rerun()

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)


def page_welcome():
    _, col, _ = st.columns([0.8, 3, 0.8])

    with col:
        st.markdown(
            '<div class="wcard">'
            '<div class="wcard-logo">🌊</div>'
            '<div class="wcard-title">Mood Flow</div>'
            '<div class="wcard-sub">'
            'Tell us how you are feeling in plain words. Our AI detects your emotional state '
            'and recommends meaningful, personalised actions, improving every time you use it.'
            '</div>'
            '<div class="input-lbl">Your Name</div>',
            unsafe_allow_html=True,
        )

        name = st.text_input(
            "",
            placeholder="e.g. Ashish",
            label_visibility="collapsed",
            key="welcome_name",
        )

        started = st.button(
            "Get My Action Plan →",
            use_container_width=True,
            type="primary",
        )

        if started:
            clean_name = name.strip()

            if not clean_name:
                st.warning("Please enter your name to continue.")
            else:
                uid, _ = memory.get_or_create_user(clean_name)
                st.session_state.update(
                    {
                        "uid": uid,
                        "username": clean_name,
                        "page": "main",
                    }
                )
                st.rerun()

        chips_html = '<div class="mood-chips">'
        for mood_meta in MOOD_META.values():
            chips_html += f'<div class="mood-chip">{mood_meta["emoji"]} {html.escape(mood_meta["label"])}</div>'
        chips_html += "</div>"

        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;font-size:.72rem;color:#BBC4DB;margin-top:1.2rem;">'
            '🔒 Stored securely · Improves with every session · 8 mood categories supported'
            '</div>',
            unsafe_allow_html=True,
        )


def page_main():
    uid = st.session_state.uid
    uname = st.session_state.username
    sess = memory.total_sessions(uid)

    greeting = f"Welcome back, {uname}" if sess > 0 else f"Hey {uname}, let's begin"

    st.markdown(
        f'<div class="topbar">'
        f'<div>'
        f'<div class="topbar-title">{html.escape(greeting)} 👋</div>'
        f'<div class="topbar-sub">Describe your feelings — I will find the right actions for you</div>'
        f'</div>'
        f'<div class="session-pill">📊 {sess} session{"s" if sess != 1 else ""} · Personalised for you</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="input-section">'
        '<div class="input-lbl">How are you feeling right now?</div>',
        unsafe_allow_html=True,
    )

    user_input = st.text_area(
        "",
        height=100,
        placeholder='e.g. "I feel really tired and bored, nothing seems interesting today..."',
        label_visibility="collapsed",
        key="mood_input",
    )

    st.markdown(
        '<div class="example-row"><b>Try:</b> "Stressed about deadlines" · '
        '"I am so bored, nothing to do" · "Feeling anxious and nervous" · "Really sad and low"</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    analyse = st.button(
        "🔍  Analyse My Mood",
        use_container_width=False,
        type="primary",
    )

    if analyse:
        txt = user_input.strip()

        if not txt:
            st.warning("Please describe how you are feeling first.")
        else:
            with st.spinner("Reading your emotional state..."):
                mood, conf = clf.predict(txt)
                recs = engine.get_recommendations(uid, mood, n=3)
                memory.record_mood(uid, mood, txt)

            st.session_state.update(
                {
                    "current_mood": mood,
                    "current_recs": recs,
                    "confidence": conf,
                    "last_input": txt,
                    "feedback_given": set(),
                }
            )
            st.rerun()

    mood = st.session_state.current_mood
    recs = st.session_state.current_recs

    if mood:
        meta = MOOD_META.get(
            mood,
            {
                "emoji": "😐",
                "color": "#4F46E5",
                "label": mood.title(),
                "desc": "",
            },
        )
        color = meta.get("color", "#4F46E5")

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

        c_mood, c_conf = st.columns([1.6, 1])

        with c_mood:
            inp = st.session_state.last_input
            quote = inp[:75] + ("..." if len(inp) > 75 else "")

            st.markdown(
                f'<div class="mood-banner" style="background:{color}0D;border-color:{color}44;color:{color};">'
                f'<div class="det-lbl">Detected Mood</div>'
                f'<div class="mood-row">'
                f'<span class="mood-emo">{meta.get("emoji", "")}</span>'
                f'<span class="mood-name">{html.escape(meta.get("label", mood.title()))}</span>'
                f'</div>'
                f'<div class="mood-desc" style="color:{color}BB;">{html.escape(meta.get("desc", ""))}</div>'
                f'<div class="mood-quote" style="border-color:{color}33;color:{color}99;">"{html.escape(quote)}"</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with c_conf:
            st.markdown('<div class="conf-card">', unsafe_allow_html=True)
            render_conf_bars(st.session_state.confidence)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="rec-title">{meta.get("emoji", "")} {html.escape(meta.get("label", mood.title()))} Recommendations</div>',
            unsafe_allow_html=True,
        )

        for i, rec in enumerate(recs):
            render_action_card(rec, i, mood, uid)

        st.markdown("<div style='margin-top:.5rem'></div>", unsafe_allow_html=True)

        if st.button("🔄  New Check-in"):
            st.session_state.update(
                {
                    "current_mood": None,
                    "current_recs": [],
                    "confidence": {},
                    "feedback_given": set(),
                    "last_input": "",
                }
            )
            st.rerun()


render_sidebar()

if st.session_state.page == "welcome":
    page_welcome()
else:
    page_main()
