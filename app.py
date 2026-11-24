"""CV Match - Streamlit frontend (version 1, DUMMY backend).

The two functions in the DUMMY BACKEND section are temporary stand-ins
so the UI can be built and tested before Baqar's real code is merged.
In the final version they are replaced by:
    from cv_parser import extract_text_from_pdf
    from matcher import analyze_cv
"""

import streamlit as st

st.set_page_config(page_title="CV Match", page_icon="📄", layout="centered")


# ---------------------------------------------------------------------------
# DUMMY BACKEND (temporary, will be removed in the final version)
# ---------------------------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """DUMMY: pretends to read the PDF. Returns placeholder text."""
    if uploaded_file is None:
        raise ValueError("No PDF uploaded.")
    return f"DUMMY CV TEXT extracted from {uploaded_file.name}"


def analyze_cv(cv_text, job_description):
    """DUMMY: returns fixed sample data in the real contract format."""
    if not cv_text or not cv_text.strip():
        raise ValueError("CV text is empty.")
    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")
    return {
        "score": 72,
        "matched_skills": ["python", "sql", "git"],
        "missing_skills": ["docker", "aws"],
        "suggestions": [
            "Add a short summary at the top that mirrors the job title.",
            "Use numbers to show impact (for example, 'reduced load time by 30%').",
            "If you genuinely have experience with Docker, mention it in a project. "
            "If you don't, treat it as a learning goal instead of adding it.",
        ],
    }


# ---------------------------------------------------------------------------
# USER INTERFACE
# ---------------------------------------------------------------------------
st.title("📄 CV Match")
st.write(
    "Upload your CV and paste a job description to see how well they match. "
    "Only list skills you genuinely have."
)

uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
job_description = st.text_area(
    "Paste the job description", height=220, placeholder="Paste the full job posting here..."
)

if st.button("Analyze", type="primary"):
    if uploaded_cv is None:
        st.warning("Please upload your CV as a PDF first.")
    elif not job_description.strip():
        st.warning("Please paste a job description first.")
    else:
        cv_text = extract_text_from_pdf(uploaded_cv)
        result = analyze_cv(cv_text, job_description)

        st.info("Version 1: these results are DUMMY sample data, not a real analysis.")

        st.subheader("Match score")
        st.metric("Score", f"{result['score']} / 100")
        st.progress(result["score"] / 100)

        st.subheader("Matched skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("No matched skills found.")

        st.subheader("Missing skills")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("No missing skills found.")

        st.subheader("Suggestions")
        for tip in result["suggestions"]:
            st.write(f"- {tip}")