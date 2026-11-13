"""
app.py
Customer Success Copilot: paste customer notes, get an account analysis.
Run it with:  python3 -m streamlit run app.py
"""

import html
import json

import streamlit as st
from google import genai
from google.genai import errors, types

from prompts import SYSTEM_PROMPT, build_user_prompt
from demo_results import DEMO_RESULTS
from sample_notes import SAMPLES

DEFAULT_MODEL = "gemini-3.8-flash"  # first choice; change via GEMINI_MODEL in secrets
# Backups tried in order if the first model is busy (503) or unavailable (404)
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
MAX_CUSTOM_RUNS = 3  # how many of their own notes each visitor can analyze

st.set_page_config(page_title="Customer Success Copilot", layout="wide")

# ---------- Styling ----------
# Streamlit's look is customized with CSS. Colors live in .streamlit/config.toml.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stMarkdown, .stTextArea textarea, button, input { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(180deg, #E6F2EC 0%, #F3F8F5 45%, #F3F8F5 100%); }
.block-container { padding-top: 1.6rem; max-width: 1180px; }
#MainMenu, footer, header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F3D30 0%, #17533F 100%); }
[data-testid="stSidebar"] * { color: #EAF4EF; }
[data-testid="stSidebar"] h3 { color: #FFFFFF; font-weight: 700; letter-spacing: -0.01em; }
[data-testid="stSidebar"] [data-baseweb="input"], [data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="base-input"] {
    background: #FFFFFF !important; border-radius: 14px !important; border: none !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] *,
[data-testid="stSidebar"] [data-baseweb="input"] svg { color: #14231D !important; fill: #14231D !important; }
[data-testid="stSidebar"] .stButton > button { background: #9FE3BF; color: #0F3D30 !important;
    border: none; border-radius: 999px; font-weight: 700; }
[data-testid="stSidebar"] .stButton > button * { color: #0F3D30 !important; }
[data-testid="stSidebar"] .stButton > button:hover { background: #B9EDD1; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.18); }

/* ---- Hero banner ---- */
.hero { background: radial-gradient(circle at 85% 20%, #2F8A68 0%, rgba(47,138,104,0) 45%),
                    linear-gradient(135deg, #0F3D30 0%, #1B5E4A 60%, #237A5E 100%);
        border-radius: 28px; padding: 2.2rem 2.4rem; margin-bottom: 1.4rem;
        box-shadow: 0 18px 40px -18px rgba(15,61,48,0.55); }
.hero .eyebrow { color: #9FE3BF; }
.hero .app-title { color: #FFFFFF; }
.hero .app-sub { color: #CFE8DC; margin-bottom: 0; }
.chip { display: inline-block; background: rgba(255,255,255,0.12); color: #EAF4EF;
        border: 1px solid rgba(255,255,255,0.18); border-radius: 999px;
        padding: 0.25rem 0.75rem; font-size: 0.78rem; margin: 1rem 0.35rem 0 0; }

.eyebrow { font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
           color: #1B5E4A; font-weight: 700; margin-bottom: 0.35rem; }
.app-title { font-size: 2.3rem; font-weight: 800; letter-spacing: -0.03em; margin: 0; line-height: 1.1; }
.app-sub { font-size: 1.02rem; margin: 0.6rem 0 1rem 0; max-width: 680px; line-height: 1.55; }

/* ---- Input + buttons ---- */
.stTextArea textarea { border-radius: 22px !important; background: #FFFFFF !important;
    border: 1.5px solid #CFE2D8 !important; padding: 1rem 1.2rem !important;
    box-shadow: 0 6px 20px -12px rgba(15,61,48,0.25); }
.stTextArea textarea:focus { border-color: #1B5E4A !important; }
.main .stButton > button[kind="primary"], .stButton > button[kind="primary"] {
    border-radius: 999px; padding: 0.65rem 1.8rem; font-weight: 700; border: none;
    background: linear-gradient(135deg, #1B5E4A, #2A8564);
    box-shadow: 0 10px 22px -10px rgba(27,94,74,0.7); }

/* ---- Cards ---- */
.card { background: #FFFFFF; border-radius: 24px; padding: 1.3rem 1.4rem; min-height: 160px;
        box-shadow: 0 10px 30px -16px rgba(15,61,48,0.30); border: 1px solid #DCEBE3; }
.card-label { font-size: 0.72rem; color: #5E7068; text-transform: uppercase;
              letter-spacing: 0.1em; font-weight: 700; }
.card-value { font-size: 2rem; font-weight: 800; color: #14231D; margin-top: 0.3rem; letter-spacing: -0.02em; }
.bar { height: 8px; border-radius: 8px; background: #E4EFE9; margin-top: 0.8rem; overflow: hidden; }
.bar > span { display: block; height: 100%; border-radius: 8px; }

.pill { display: inline-block; padding: 0.22rem 0.75rem; border-radius: 999px;
        font-size: 0.78rem; font-weight: 700; margin-top: 0.6rem; }
.good { background: #D3F2E2; color: #11643F; }
.warn { background: #FFE9C7; color: #8A4E05; }
.bad  { background: #FFD9D4; color: #A3261C; }
.neutral { background: #E4ECE8; color: #3F514A; }

.account-panel { background: #FFFFFF; border-radius: 24px; padding: 1.4rem 1.6rem; margin: 0.4rem 0 1rem 0;
                 border: 1px solid #DCEBE3; border-left: 6px solid #1B5E4A;
                 box-shadow: 0 10px 30px -18px rgba(15,61,48,0.30); }
.account-name { font-size: 1.5rem; font-weight: 800; color: #14231D; margin: 0.1rem 0 0.35rem 0; letter-spacing: -0.02em; }
.summary { color: #34463F; font-size: 1rem; line-height: 1.6; }

.item { background: #FFFFFF; border: 1px solid #DCEBE3; border-radius: 18px;
        padding: 0.95rem 1.15rem; margin-bottom: 0.7rem;
        box-shadow: 0 6px 18px -14px rgba(15,61,48,0.35); }
.item-title { font-weight: 650; color: #14231D; }
.item-sub { color: #5E7068; font-size: 0.9rem; margin-top: 0.25rem; }
.quote { background: #F0F8F4; border-left: 3px solid #2A8564; border-radius: 0 12px 12px 0;
         padding: 0.45rem 0.8rem; color: #33463F; font-style: italic; font-size: 0.9rem; margin-top: 0.55rem; }
.section-h { font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.12em;
             color: #1B5E4A; font-weight: 700; margin: 1.2rem 0 0.65rem 0; }

/* ---- Tabs as pills ---- */
.stTabs [role="tablist"] { gap: 0.35rem; background: #FFFFFF; padding: 0.4rem; border-radius: 999px;
    border: 1px solid #DCEBE3; width: fit-content; max-width: 100%; flex-wrap: wrap;
    box-shadow: 0 6px 18px -14px rgba(15,61,48,0.35); }
.stTabs [role="tab"] { border-radius: 999px !important; padding: 0.45rem 1.05rem !important;
    border: none !important; background: transparent; height: auto !important; }
.stTabs [role="tab"] p { font-weight: 600; color: #3F514A; font-size: 0.9rem; }
.stTabs [role="tab"][aria-selected="true"] { background: #1B5E4A !important; }
.stTabs [role="tab"][aria-selected="true"] p { color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"], .stTabs .react-aria-SelectionIndicator { display: none !important; }
.stTabs [role="tab"] { cursor: pointer; }
.stCodeBlock, pre { border-radius: 18px !important; }
[data-testid="stAlert"] { border-radius: 18px; }
.footer-note { color: #6E8078; font-size: 0.82rem; margin-top: 2.2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)


# ---------- Helpers ----------
def get_secret(name: str, default=None):
    """Read a value from .streamlit/secrets.toml without crashing if the file doesn't exist."""
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def analyze_notes(api_key: str, model: str, notes: str, tone: str) -> dict:
    """Send the notes to Google Gemini and get back a structured JSON analysis.
    If a model is busy or unavailable, try the backup models one by one."""
    client = genai.Client(api_key=api_key)
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_error = None
    for name in models_to_try:
        try:
            response = client.models.generate_content(
                model=name,
                contents=build_user_prompt(notes, tone),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,  # low = more consistent, less "creative"
                    response_mime_type="application/json",  # forces the AI to reply in JSON
                ),
            )
            return json.loads(response.text)
        except errors.ServerError as e:  # 503 busy, 500 server problem: try the next model
            last_error = e
        except errors.ClientError as e:
            if e.code == 404:  # model retired or not offered: try the next model
                last_error = e
            else:
                raise  # wrong key or free limit reached: stop and report it
    raise last_error


def find_demo(notes: str):
    """If the notes are one of our samples (unchanged), return its saved analysis."""
    for name, sample_text in SAMPLES.items():
        if notes.strip() == sample_text.strip():
            return DEMO_RESULTS.get(name)
    return None


# Which color each label gets
TONE = {"Low": "good", "Medium": "warn", "High": "bad",
        "Healthy": "good", "At Risk": "warn", "Critical": "bad",
        "Champion": "good", "Decision Maker": "neutral", "Neutral": "neutral",
        "Detractor": "bad", "Unknown": "neutral"}


def esc(text) -> str:
    """Make AI text safe to show inside our HTML."""
    return html.escape(str(text or ""))


def pill(label: str) -> str:
    return f'<span class="pill {TONE.get(label, "neutral")}">{esc(label)}</span>'


def card(label: str, value: str, extra: str = "") -> str:
    return (f'<div class="card"><div class="card-label">{label}</div>'
            f'<div class="card-value">{value}</div>{extra}</div>')


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### Settings")

    # The key is read privately from .streamlit/secrets.toml (or the host's secrets settings).
    # Visitors never see or enter a key.
    api_key = get_secret("GEMINI_API_KEY")

    model = get_secret("GEMINI_MODEL", DEFAULT_MODEL)
    tone = st.selectbox("Follow-up email tone",
                        ["Warm and reassuring", "Clear and direct", "Celebratory", "Formal"])

    st.divider()
    st.markdown("### Try an example")
    sample_choice = st.selectbox("Sample account", list(SAMPLES.keys()))
    if st.button("Load sample notes", width="stretch"):
        st.session_state["notes"] = SAMPLES[sample_choice]

# ---------- Header ----------
st.markdown('<div class="hero"><div class="eyebrow">Account intelligence</div>'
            '<h1 class="app-title">Customer Success Copilot</h1>'
            '<p class="app-sub">Turn raw call notes into account health, churn risk backed by evidence, '
            'stakeholder insight, next steps and ready-to-send follow-ups.</p>'
            '<span class="chip">Health scoring</span><span class="chip">Churn evidence</span>'
            '<span class="chip">Stakeholder map</span><span class="chip">Escalation drafts</span></div>',
            unsafe_allow_html=True)

notes = st.text_area("Customer notes", key="notes", height=200, label_visibility="collapsed",
                     placeholder="Paste call notes, emails or meeting summaries here...")

if st.button("Analyze account", type="primary"):
    demo = find_demo(notes)
    runs = st.session_state.get("custom_runs", 0)
    if not notes.strip():
        st.warning("Paste some customer notes or load a sample from the sidebar.")
    elif demo:
        # Sample notes: show the saved analysis instantly, no key and no cost
        st.session_state["result"] = demo
        st.session_state["is_demo"] = True
    elif not api_key:
        st.info("Live analysis of your own notes isn't available right now. "
                "Load one of the samples from the sidebar to see the full analysis.")
    elif runs >= MAX_CUSTOM_RUNS:
        st.info(f"You've used all {MAX_CUSTOM_RUNS} live analyses for this visit. "
                "The samples in the sidebar still work anytime.")
    else:
        with st.spinner("Analyzing the account..."):
            try:
                st.session_state["result"] = analyze_notes(api_key, model, notes, tone)
                st.session_state["is_demo"] = False
                st.session_state["custom_runs"] = runs + 1
            except errors.ClientError as e:
                if getattr(e, "code", None) == 429:
                    st.warning("The free AI limit has been reached for now. Please try again in a few "
                               "minutes, or load a sample from the sidebar.")
                else:
                    st.error("The AI service couldn't process this request. Check the API key, "
                             "or try a sample from the sidebar.")
            except errors.ServerError:
                st.warning("Google's AI is very busy right now. Please try again in a minute, "
                           "or load a sample from the sidebar.")
            except Exception:
                st.error("Something went wrong while analyzing. Please try again, "
                         "or load a sample from the sidebar.")

result = st.session_state.get("result")

if result:
    st.markdown(f'<div class="account-panel"><div class="eyebrow">Account</div>'
                f'<div class="account-name">{esc(result.get("account_name", "Account"))}</div>'
                f'<div class="summary">{esc(result.get("summary"))}</div>'
                + ('<span class="pill neutral">Saved demo analysis</span>' if st.session_state.get("is_demo") else '')
                + '</div>',
                unsafe_allow_html=True)

    # --- Score cards ---
    score = result.get("health_score", 0)
    try:
        score = max(0, min(100, int(score)))
    except (TypeError, ValueError):
        score = 0
    label = result.get("health_label", "Unknown")
    bar_color = {"good": "#23A06A", "warn": "#E39A2D", "bad": "#D2483D"}.get(TONE.get(label), "#8A918E")
    risk = result.get("churn_risk", {})
    single = result.get("single_threaded")

    c1, c2, c3 = st.columns(3)
    c1.markdown(card("Health score", f"{score}<span style='font-size:1rem;color:#8A918E'>/100</span>",
                     f'<div class="bar"><span style="width:{score}%;background:{bar_color}"></span></div>'
                     f'{pill(label)}'), unsafe_allow_html=True)
    n_reasons = len(risk.get("reasons", []))
    c2.markdown(card("Churn risk", esc(risk.get("level", "Unknown")),
                     f'<span class="pill {TONE.get(risk.get("level"), "neutral")}">'
                     f'{n_reasons} warning sign{"s" if n_reasons != 1 else ""} found</span>'),
                unsafe_allow_html=True)
    c3.markdown(card("Relationship", "Single-threaded" if single else "Multi-threaded",
                     f'<span class="pill {"warn" if single else "good"}">'
                     f'{"One key contact" if single else "Several contacts"}</span>'),
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["Risk and actions", "Stakeholders", "Commitments",
                    "Follow-up email", "Internal escalation", "Growth and gaps"])

    # --- Risk reasons with evidence + next actions ---
    with tabs[0]:
        st.markdown('<div class="section-h">Why this risk level</div>', unsafe_allow_html=True)
        for r in risk.get("reasons", []):
            st.markdown(f'<div class="item"><div class="item-title">{esc(r.get("reason"))}</div>'
                        f'<div class="quote">"{esc(r.get("evidence"))}"</div></div>',
                        unsafe_allow_html=True)
        st.markdown('<div class="section-h">Next actions</div>', unsafe_allow_html=True)
        for a in result.get("next_actions", []):
            st.markdown(f'<div class="item"><div class="item-title">{esc(a.get("action"))}</div>'
                        f'{pill(a.get("priority", "Unknown"))}</div>', unsafe_allow_html=True)

    # --- Stakeholder map ---
    with tabs[1]:
        people = result.get("stakeholders", [])
        if single:
            st.warning("This account depends on one contact. Building a second relationship would lower the risk.")
        if not people:
            st.info("No stakeholders mentioned in the notes.")
        cols = st.columns(2)
        for i, p in enumerate(people):
            cols[i % 2].markdown(
                f'<div class="item"><div class="item-title">{esc(p.get("name"))}</div>'
                f'<div class="item-sub">{esc(p.get("role"))}</div>'
                f'{pill(p.get("stance", "Unknown"))}'
                f'<div class="item-sub">{esc(p.get("note"))}</div></div>', unsafe_allow_html=True)

    # --- Commitments tracker ---
    with tabs[2]:
        commitments = result.get("commitments", [])
        if not commitments:
            st.info("No commitments found in the notes.")
        for c in commitments:
            st.markdown(f'<div class="item"><div class="item-title">{esc(c.get("what"))}</div>'
                        f'<div class="item-sub">Owner: {esc(c.get("owner"))} &nbsp;·&nbsp; '
                        f'Due: {esc(c.get("due"))}</div></div>', unsafe_allow_html=True)

    # --- Follow-up email ---
    with tabs[3]:
        email = result.get("follow_up_email", {})
        st.markdown(f'<div class="section-h">Subject</div>'
                    f'<div class="item-title">{esc(email.get("subject"))}</div>'
                    f'<div class="section-h">Body</div>', unsafe_allow_html=True)
        st.code(email.get("body", ""), language=None, wrap_lines=True)
        st.caption("Use the copy icon in the top right corner of the box.")

    # --- Internal escalation ---
    with tabs[4]:
        esc_info = result.get("internal_escalation", {})
        if esc_info.get("needed"):
            st.markdown(f'<div class="item"><div class="item-sub">Route to</div>'
                        f'<div class="item-title">{esc(esc_info.get("team"))}</div>'
                        f'{pill(esc_info.get("urgency", "Unknown"))}</div>', unsafe_allow_html=True)
            st.code(esc_info.get("message", ""), language=None, wrap_lines=True)
        else:
            st.success("No internal escalation needed right now.")

    # --- Expansion signals + missing info ---
    with tabs[5]:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown('<div class="section-h">Expansion signals</div>', unsafe_allow_html=True)
            for s in result.get("expansion_signals", []) or ["None spotted in these notes"]:
                st.markdown(f'<div class="item">{esc(s)}</div>', unsafe_allow_html=True)
        with g2:
            st.markdown('<div class="section-h">Missing info to ask about</div>', unsafe_allow_html=True)
            for m in result.get("missing_info", []) or ["Nothing obvious"]:
                st.markdown(f'<div class="item">{esc(m)}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer-note">Built by Hadia Tahir. AI can make mistakes, '
            'so review everything before sending.</div>', unsafe_allow_html=True)
