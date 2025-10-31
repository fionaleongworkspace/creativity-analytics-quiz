# app.py
# ---- Creativity ↔ Analytics Quiz (Streamlit) ----
# Run locally:   streamlit run app.py
# Deploy free:   share.streamlit.io  (Streamlit Community Cloud)

import streamlit as st
from datetime import datetime
import textwrap

st.set_page_config(page_title="Creativity ↔ Analytics Quiz", page_icon="✨", layout="centered")

# --- Content ----
TITLE = "Creativity ↔ Analytics Quiz"
INTRO = """Answer 10 quick A/B choices. There’s no “right” answer — we’re mapping your *default problem-solving style*.
Pick the option that feels more natural *most of the time*."""
RESULT_BLURBS = {
    "Creative Maven": "You lead with imagination, concepting, brand story and distinctive ideas, then bring data in to refine.",
    "Analytical Ace": "You lead with structure, evidence and measurement, turning ambiguity into clear, testable action.",
    "Hybrid Synthesizer": "You blend bold ideas with rigorous evaluation, switching gears based on context. Best of both worlds."
}

# 10 prompts — A leans creative; B leans analytical
QUESTIONS = [
# 10 full questions — A leans creative; B leans analytical
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


# --- Helpers ---
def score_profile(answers):
    a = sum(1 for x in answers if x == "A")
    b = len(answers) - a
    if a >= b + 2:
        label = "Creative Maven"
    elif b >= a + 2:
        label = "Analytical Ace"
    else:
        label = "Hybrid Synthesizer"
    return label, a, b

def share_text(name, label, a, b):
    lines = f"""
    I just took a quick Creativity ↔ Analytics quiz. Result: **{label}** ({a}×A : {b}×B).

    I believe modern marketing needs both imagination *and* measurement — the real edge is knowing when to lean which way.

    Curious where you land? Try the quiz here and comment your result.
    """
    return textwrap.dedent(lines).strip()

# --- UI ---
st.title(TITLE)
st.write(INTRO)

with st.expander("Optional: add your name for the result card", expanded=False):
    name = st.text_input("Name (for the result card)", value="")

st.markdown("---")
answers = []
for i, (topic, optA, optB) in enumerate(QUESTIONS, start=1):
    choice = st.radio(
        f"{i}. {topic}",
        options=["A", "B"],
        format_func=lambda x, a=optA, b=optB: a if x == "A" else b,
        key=f"q{i}",
        horizontal=False,
    )
    answers.append(choice)

st.markdown("---")
if st.button("See my result"):
    label, a, b = score_profile(answers)
    who = name.strip() or "You"
    st.success(f"**{who} = {label}**  ·  A: {a}  B: {b}")
    st.write(RESULT_BLURBS[label])

    # Result card
    st.markdown("### Your Result Summary")
    st.write(f"- Profile: **{label}**")
    st.write(f"- Tally: **{a}×A / {b}×B**")
    st.write("—")
    st.caption("Tip: Balanced teams mix creative ignition with analytical acceleration.")

    # Share text (copy-paste into LinkedIn)
    st.markdown("### Share this on LinkedIn")
    txt = share_text(name, label, a, b)
    st.code(txt, language="markdown")

    # Optional: download personal result
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    csv = f"name,profile,A_count,B_count,timestamp_utc\n{(name or 'Anonymous')},{label},{a},{b},{ts}\n"
    st.download_button("Download my result (.csv)", data=csv, file_name=f"quiz_result_{ts}.csv", mime="text/csv")

st.caption("Built with Streamlit • v1.0")
