# app.py — Creativity ↔ Analytics Quiz (single-question flow, polished)
import streamlit as st
from datetime import datetime
import textwrap

# ---------- Page setup ----------
st.set_page_config(
    page_title="Creativity ↔ Analytics Quiz",
    page_icon="✨",       # replace with "logo.png" if you upload one to repo root
    layout="centered"
)

# ---------- Visual polish (CSS) ----------
st.markdown("""
<style>
/* Page background gradient for depth */
.stApp { background: linear-gradient(180deg, #ffffff 0%, #faf8ff 60%, #ffffff 100%); }

/* Center column width & padding */
.main .block-container { max-width: 860px; padding-top: 2.2rem; padding-bottom: 4rem; }

/* Hero title tracking */
h1 { letter-spacing: .2px; }

/* Soft divider */
.hr { height: 8px; border: 0; border-radius: 999px; background: #e9e4ff; margin: 12px 0 24px; }

/* Radio group as soft card */
div.row-widget.stRadio > div {
  background: #fff; border: 1px solid #ECE9FF; border-radius: 16px;
  padding: 14px 16px; box-shadow: 0 6px 18px rgba(122,61,228,.06);
}

/* Radio labels readability */
label[data-baseweb="radio"] > div:nth-child(2) { line-height: 1.35; }

/* Buttons: rounded + semi-bold */
div.stButton > button { border-radius: 12px; font-weight: 600; padding: .6rem 1rem; }

/* Progress bar thinner & rounded (selector works on current Streamlit) */
[data-baseweb="progress-bar"] div[role="progressbar"] { height: 6px; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# Optional banner/logo if you add a file (e.g., banner.jpg) to repo root:
# st.image("banner.jpg", use_column_width=True)

# ---------- Content ----------
TITLE = "Creativity ↔ Analytics Quiz"
INTRO = (
    "Answer 10 quick A/B choices. There’s no “right” answer — "
    "we’re mapping your default problem-solving style."
)

QUESTIONS = [
    ("When starting on a new brief, what’s your instinctive first step?",
     "A. Dive into moodboards, ideas, and possible creative angles.",
     "B. Study metrics, baselines, and constraints before ideating."),
    ("How do you prefer to approach brainstorming?",
     "A. Generate as many wild ideas as possible first — sorting can come later.",
     "B. Define success criteria early and ideate within clear boundaries."),
    ("When planning a new campaign, what excites you more?",
     "A. Crafting a big creative concept that people will emotionally connect with.",
     "B. Building a measurable, testable hypothesis to validate performance."),
    ("When writing copy, what’s your focus?",
     "A. Crafting a memorable voice that stands out from the crowd.",
     "B. Ensuring clarity and keyword alignment for strong search and conversion."),
    ("When developing visual direction, what matters most to you?",
     "A. Striking originality and designs that spark conversation.",
     "B. Visual consistency that aligns tightly with brand guidelines."),
    ("When prioritizing ideas, which one are you more likely to champion?",
     "A. The bold idea with the potential to create buzz and attention.",
     "B. The data-backed initiative with the clearest ROI potential."),
    ("How do you typically handle ambiguity or open-ended projects?",
     "A. Explore and experiment — inspiration often comes through discovery.",
     "B. Reduce uncertainty quickly by testing or analyzing data."),
    ("When gathering feedback, what’s your preferred source?",
     "A. Gut feel and reactions from your audience or peers.",
     "B. Quantitative metrics, survey data, or conversion results."),
    ("How do you prefer to iterate on work?",
     "A. Keep refining until it ‘feels right’ creatively.",
     "B. Ship quickly, measure performance, and optimize from results."),
    ("When celebrating a successful project, what do you tend to highlight?",
     "A. The creative idea, storytelling, and emotional impact.",
     "B. The measurable gains — engagement, ROI, or efficiency metrics."),
]

RESULT_BLURBS = {
    "Creative Maven": "You lead with imagination, concepting, brand story and distinctive ideas, then bring data in to refine.",
    "Analytical Ace": "You lead with structure, evidence and measurement, turning ambiguity into clear, testable action.",
    "Hybrid Synthesizer": "You blend bold ideas with rigorous evaluation, switching gears based on context. Best of both worlds."
}

def score_profile(answers):
    a = answers.count("A")
    b = answers.count("B")
    if a >= b + 2:
        label = "Creative Maven"
    elif b >= a + 2:
        label = "Analytical Ace"
    else:
        label = "Hybrid Synthesizer"
    return label, a, b

def share_text(name, label, a, b):
    return textwrap.dedent(f"""
    I just took a quick Creativity ↔ Analytics quiz. Result: **{label}** ({a}×A : {b}×B).

    Modern marketing needs both imagination *and* measurement — the edge is knowing when to lean which way.

    Try it and comment your result.
    """).strip()

# ---------- Hero header (inserted BEFORE state/UI) ----------
st.markdown("# Creativity ↔ Analytics Quiz")
st.write(INTRO)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

with st.expander("Optional: add your name for the result card", expanded=False):
    default_name = st.session_state.get("name", "")
    st.session_state["name"] = st.text_input("Name (for the result card)", value=default_name)

# ---------- State init ----------
if "i" not in st.session_state:
    st.session_state.i = 0                  # current question index
if "answers" not in st.session_state:
    st.session_state.answers = [""] * len(QUESTIONS)
if "done" not in st.session_state:
    st.session_state.done = False

# ---------- UI flow ----------
total = len(QUESTIONS)
i = st.session_state.i

# Progress bar
st.progress(int((i if not st.session_state.done else total) / total * 100))

if not st.session_state.done:
    # ----- Question card -----
    q, A_text, B_text = QUESTIONS[i]
    st.markdown(f"## {i+1}. {q}")

    # Previously chosen answer (if any)
    current = st.session_state.answers[i] or None

    choice = st.radio(
        "Pick one:",
        options=["A", "B"],
        format_func=lambda x: A_text if x == "A" else B_text,
        index=0 if current == "A" else (1 if current == "B" else None),
        key=f"q_{i}"
    )
    st.session_state.answers[i] = choice

    # Navigation buttons
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("⬅ Back", disabled=(i == 0)):
            st.session_state.i -= 1
            st.stop()
    with c2:
        if st.button("Clear"):
            st.session_state.answers[i] = ""
            st.rerun()
    with c3:
        if i < total - 1:
            st.button("Next ➡", on_click=lambda: st.session_state.update(i=i+1))
        else:
            st.button("See my result", on_click=lambda: st.session_state.update(done=True))
else:
    # ----- Results page -----
    # default any blanks to "A" to avoid None issues (or change to strict if you prefer)
    label, a, b = score_profile([x or "A" for x in st.session_state.answers])
    who = (st.session_state.get("name") or "You").strip()

    st.success(f"**{who} = {label}**  ·  A: {a}  B: {b}")
    st.write(RESULT_BLURBS[label])

    st.markdown("### Your Result Summary")
    st.write(f"- Profile: **{label}**")
    st.write(f"- Tally: **{a}×A / {b}×B**")
    st.caption("Tip: Balanced teams mix creative ignition with analytical acceleration.")

    st.markdown("### Share this on LinkedIn")
    st.code(share_text(st.session_state.get("name", ""), label, a, b), language="markdown")

    ts = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    csv = f"name,profile,A_count,B_count,timestamp_utc\n{(st.session_state.get('name') or 'Anonymous')},{label},{a},{b},{ts}\n"
    st.download_button("Download my result (.csv)", data=csv, file_name=f"quiz_result_{ts}.csv", mime="text/csv")

    st.markdown("---")
    if st.button("Restart quiz"):
        st.session_state.i = 0
        st.session_state.answers = [""] * len(QUESTIONS)
        st.session_state.done = False
        st.rerun()

# ---------- Footer ----------
st.markdown("---")
st.caption("Designed by Fiona Leong • Marketing & Data Analytics • Streamlit Web App 2025")


