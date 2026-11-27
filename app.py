"""CV Match - Streamlit frontend (final version).

    cv_parser.extract_text_from_pdf(uploaded_file) -> str   (raises ValueError)
    matcher.analyze_cv(cv_text, job_description)  -> dict   (raises ValueError)
"""

import streamlit as st

from cv_parser import extract_text_from_pdf
from matcher import analyze_cv

st.set_page_config(page_title="CV Match", page_icon="📄", layout="wide")


def score_color(score: int) -> str:
    """Pick a Streamlit text color for the score."""
    if score >= 70:
        return "green"
    if score >= 40:
        return "orange"
    return "red"


def show_results(result: dict) -> None:
    """Render the dictionary returned by analyze_cv."""
    score = max(0, min(100, int(result["score"])))

    st.subheader("Match score")
    st.markdown(f"## :{score_color(score)}[{score} / 100]")
    st.progress(score)

    col_matched, col_missing = st.columns(2)

    with col_matched:
        st.subheader("✅ Matched skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.markdown(f"- :green[{skill}]")
        else:
            st.info("No skills from the job description were found in your CV.")

    with col_missing:
        st.subheader("⚠️ Missing skills")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.markdown(f"- :red[{skill}]")
            st.caption(
                "Only add a skill to your CV if you genuinely have it. "
                "Otherwise, treat it as something to learn."
            )
        else:
            st.success("Your CV covers every skill found in the job description.")

    st.subheader("💡 CV improvement suggestions")
    if result["suggestions"]:
        for tip in result["suggestions"]:
            st.markdown(f"- {tip}")
    else:
        st.info("No suggestions for this CV and job description.")


# ---------------------------------------------------------------------------
# PAGE
# ---------------------------------------------------------------------------
st.title("📄 CV Match")
st.write(
    "Compare your CV with a job description to see your match score, "
    "which skills you already show, and which ones the job asks for that "
    "your CV does not mention. Only list skills you genuinely have."
)

left, right = st.columns(2)
with left:
    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
with right:
    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder="Paste the full job posting here...",
    )

analyze_clicked = st.button("Analyze", type="primary")

if analyze_clicked:
    if uploaded_cv is None:
        st.warning("Please upload your CV as a PDF first.")
    elif not job_description.strip():
        st.warning("Please paste a job description first.")
    else:
        try:
            with st.spinner("Analyzing your CV..."):
                cv_text = extract_text_from_pdf(uploaded_cv)
                result = analyze_cv(cv_text, job_description)
        except ValueError as error:
            st.error(f"Could not analyze your CV: {error}")
        except Exception:
            st.error("Something unexpected went wrong. Please try again.")
        else:
            show_results(result)
else:
    st.info(
        "Upload a PDF CV, paste a job description, then click **Analyze** "
        "to see your results here."
    )