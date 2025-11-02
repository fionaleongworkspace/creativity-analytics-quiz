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

/* Soft divider (now gradient) */
.hr {
  height: 8px; border: 0; border-radius: 999px;
  background: linear-gradient(90deg, #007BFF 0%, #8A2BE2 100%);
  margin: 12px 0 24px;
}

/* Radio group as soft card */
div.row-widget.stRadio > div {
  background: #fff; border: 1px solid #ECE9FF; border-radius: 16px;
  padding: 14px 16px; box-shadow: 0 6px 18px rgba(122,61,228,.06);
}

/* Radio labels readability */
label[data-baseweb="radio"] > div:nth-child(2) { line-height: 1.35; }

/* Buttons: rounded + semi-bold */
div.stButton > button { border-radius: 12px; font-weight: 600; padding: .6rem 1rem; }

/* Progress bar: thin, rounded, gradient fill */
[data-baseweb="progress-bar"] div[role="progressbar"] {
  height: 6px;
  border-radius: 999px;
  background: linear-gradient(90deg, #007BFF 0%, #8A2BE2 100%) !important;
}

/* Empty track softer */
[data-baseweb="progress-bar"] > div:first-child {
  background-color: #f2efff !important;
}

/* Fade animation for Progress label */
@keyframes fadeInOut {
  0% { opacity: 0.4; }
  50% { opacity: 1; }
  100% { opacity: 0.4; }
}

.progress-label {
  text-align: right;
  font-weight: 600;
  color: #6c63ff;
  animation: fadeInOut 2s ease-in-out infinite;
}

</style>
""", unsafe_allow_html=True)


# ---------- Content ----------
TITLE = "Creativity ↔ Analytics Quiz"
INTRO = (
    "Answer 10 quick A/B choices. There’s no “right” answer — "
    "this is just to find out your default problem-solving style."
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

# ---------- Profiles ----------
PROFILES = {
    "Creative Maven": {
        "headline": "You lead with heart, not spreadsheets.",
        "desc": (
            "Ideas find you before you find them. You think in stories, colors, and possibilities—"
            "then shape the logic later. You bring energy, spark, and human connection to every "
            "project, often reminding the team that *data doesn’t dream — people do.*"
        ),
        "superpower": "Turning emotion into movement.",
        "watchout": "Getting lost in possibilities—bring the numbers in before you pitch.",
        "share_hook": "Tag your favorite data-driven teammate — they probably balance you out!"
    },
    "Analytical Ace": {
        "headline": "You turn the chaos of marketing into measurable momentum.",
        "desc": (
            "You’re the one who brings structure to the storm. Hypotheses, baselines, and dashboards "
            "are your native language — but you’re not cold; you just believe clarity is kindness. "
            "You make creativity accountable, and ideas scalable."
        ),
        "superpower": "Seeing patterns where others see noise.",
        "watchout": "Over-optimizing — sometimes, magic can’t be A/B tested.",
        "share_hook": "Tag a creative wild card who keeps your charts interesting!"
    },
    "Hybrid Synthesizer": {
        "headline": "You switch between art and algorithm like second nature.",
        "desc": (
            "You’re both dreamer and doer — equally comfortable pitching a vision or debugging a metric. "
            "You connect the left and right brains of marketing, blending story with science. "
            "When others pick sides, you pick balance — and that’s your edge."
        ),
        "superpower": "Translating creativity into strategy (and back again).",
        "watchout": "Doing too much yourself — bridges need both sides to stand strong.",
        "share_hook": "Tag a teammate who leans more creative or more data — see if you make the perfect pair."
    }
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

# ---------- Hero header (single instance) ----------
st.markdown("""
<h1 style="
  font-weight: 800;
  background: linear-gradient(90deg, #007BFF 0%, #8A2BE2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 0.5em;">
  Creativity ↔ Analytics Quiz
</h1>
""", unsafe_allow_html=True)
st.write(INTRO)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ---------- Name input ----------
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

# ---------- Progress (single instance, placed under hero) ----------
progress_percent = int((st.session_state.get("i", 0) / len(QUESTIONS)) * 100)

# Create a small "Progress" label aligned with the bar
c1, c2 = st.columns([6, 1])
with c1:
    st.write("")  # spacer
with c2:
    st.markdown(
    f"<p style='text-align:right; font-weight:600; color:#6c63ff;'>Progress: {progress_percent}%</p>",
    unsafe_allow_html=True,
)

st.progress(progress_percent)


# ---------- UI flow ----------
total = len(QUESTIONS)
i = st.session_state.i

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
    label, a, b = score_profile([x or "A" for x in st.session_state.answers])  # default blanks to A
    who = (st.session_state.get("name") or "You").strip()

    st.success(f"**{who} = {label}**  ·  A: {a}  B: {b}")
    profile = PROFILES[label]

st.markdown(f"**{profile['headline']}**")
st.write(profile["desc"])

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**Superpower:** {profile['superpower']}")
with c2:
    st.markdown(f"**Watch out for:** {profile['watchout']}")

st.info(profile["share_hook"])


    st.markdown("### Your Result Summary")
    st.write(f"- Profile: **{label}**")
    st.write(f"- Tally: **{a}×A / {b}×B**")
    st.caption("Tip: Balanced teams mix creative ignition with analytical acceleration.")

    st.markdown("### Share this on LinkedIn")
st.markdown(
    "💬 *Post your result with **#CreativityAnalyticsQuiz** — let’s see which side LinkedIn leans toward!*"
)

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
