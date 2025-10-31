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
    ("Briefs", "A. Start with moodboards and angles", "B. Start with metrics, baseline and constraints"),
    ("Brainstorming", "A. Diverge wildly first, sort later", "B. Define criteria first, ideate within bounds"),
    ("New campaign", "A. Big concept that people feel", "B. Clear hypothesis you can A/B test"),
    ("Copy choice", "A. Memorable voice that zigs", "B. Clarity + relevance from keyword data"),
    ("Visual direction", "A. Distinctive art that sparks talk", "B. Guideline-aligned, consistent and legible"),
    ("Prioritisation", "A. Back the idea with potential buzz", "B. Back the item with highest projected ROI"),
    ("Ambiguity", "A. Explore possibilities", "B. Reduce uncertainty with a small test"),
    ("Feedback", "A. Audience gut-feel matters most", "B. Quant feedback matters most"),
    ("Iteration", "A. Keep crafting until it ‘clicks’", "B. Ship, measure, then optimize "),
    ("Wins", "A. Talk about concept & craft", "B. Talk about lift, CAC, ROAS, CTR"),
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
