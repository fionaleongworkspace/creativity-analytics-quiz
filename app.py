# app.py — Creativity ↔ Analytics Quiz (Streamlit, single-question flow)
import streamlit as st
from datetime import datetime
import textwrap

st.set_page_config(page_title="Creativity ↔ Analytics Quiz", page_icon="✨", layout="centered")
# --- Visual polish pack ---
st.markdown("""
<style>
/* Page background gradient for depth */
.stApp {background: linear-gradient(180deg, #ffffff 0%, #faf8ff 60%, #ffffff 100%);}

/* Center column max width */
.main .block-container {max-width: 860px; padding-top: 2.2rem; padding-bottom: 4rem;}

/* Hero title weight & tracking */
h1 {letter-spacing: .2px;}

/* Subtle divider */
.hr {height: 8px; border: 0; border-radius: 999px; background: #e9e4ff; margin: 12px 0 24px;}

/* Radio group as soft card */
div.row-widget.stRadio > div {
  background: #fff; border: 1px solid #ECE9FF; border-radius: 16px;
  padding: 14px 16px; box-shadow: 0 6px 18px rgba(122,61,228,.06);
}

/* Radio labels spacing */
label[data-baseweb="radio"] > div:nth-child(2) { line-height: 1.35; }

/* Buttons: rounded + semi-bold */
div.stButton > button { border-radius: 12px; font-weight: 600; padding: .6rem 1rem; }

/* Disabled button visibility */
button[kind="secondary"] {opacity: .7}

/* Progress bar thinner */
[data-baseweb="progress-bar"] div[role="progressbar"] { height: 6px; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# Optional banner/logo (upload 'logo.png' or 'banner.jpg' to repo root)
# st.image("banner.jpg", use_column_width=True)

TITLE = "Creativity ↔ Analytics Quiz"
INTRO = "Answer 10 quick A/B choices. There’s no “right” answer — we’re mapping your default problem-solving style."

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

    Try it and comment your result: {st.query_params.get("utm_source", "LinkedIn")}
    """).strip()

# --- State init ---
if "i" not in st.session_state:
    st.session_state.i = 0                # current question index
if "answers" not in st.session_state:
    st.session_state.answers = [""] * len(QUESTIONS)
if "done" not in st.session_state:
    st.session_state.done = False
if "name" not in st.session_state:
    st.session_state.name = ""

# --- UI ---
st.title(TITLE)
st.write(INTRO)

with st.expander("Optional: add your name for the result card", expanded=False):
    st.session_state.name = st.text_input("Name (for the result card)", value=st.session_state.name)

total = len(QUESTIONS)
i = st.session_state.i
st.progress(int((i if not st.session_state.done else total) / total * 100))

if not st.session_state.done:
    q, A_text, B_text = QUESTIONS[i]
    st.markdown(f"### {i+1}. {q}")

    # existing choice (if any)
    current = st.session_state.answers[i] or None
    choice = st.radio(
        "Pick one:",
        options=["A", "B"],
        format_func=lambda x: A_text if x == "A" else B_text,
        index=0 if current == "A" else (1 if current == "B" else None),
        key=f"q_{i}"
    )
    st.session_state.answers[i] = choice

    cols = st.columns([1,1,1])
    with cols[0]:
        if st.button("⬅ Back", disabled=(i == 0)):
            st.session_state.i -= 1
            st.stop()
    with cols[1]:
        if st.button("Clear"):
            st.session_state.answers[i] = ""
            st.rerun()
    with cols[2]:
        if i < total - 1:
            st.button("Next ➡", on_click=lambda: st.session_state.update(i=i+1))
        else:
            # last question → finish
            st.button("See my result", on_click=lambda: st.session_state.update(done=True))
else:
    # Results page
    label, a, b = score_profile([x or "A" for x in st.session_state.answers])  # default blanks to A
    who = (st.session_state.name or "You").strip()
    st.success(f"**{who} = {label}**  ·  A: {a}  B: {b}")
    st.write(RESULT_BLURBS[label])

    st.markdown("### Your Result Summary")
    st.write(f"- Profile: **{label}**")
    st.write(f"- Tally: **{a}×A / {b}×B**")
    st.caption("Tip: Balanced teams mix creative ignition with analytical acceleration.")

    st.markdown("### Share this on LinkedIn")
    st.code(share_text(st.session_state.name, label, a, b), language="markdown")

    ts = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    csv = f"name,profile,A_count,B_count,timestamp_utc\n{(st.session_state.name or 'Anonymous')},{label},{a},{b},{ts}\n"
    st.download_button("Download my result (.csv)", data=csv, file_name=f"quiz_result_{ts}.csv", mime="text/csv")

    st.markdown("---")
    if st.button("Restart quiz"):
        st.session_state.i = 0
        st.session_state.answers = [""] * len(QUESTIONS)
        st.session_state.done = False
        st.rerun()

st.caption("Built with Streamlit • v1.0")
