"""Skill detection for CVs and job descriptions."""
import re

# Canonical skill name -> spellings that may appear in text
SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "C++": ["c++"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Git": ["git", "github"],
    "Docker": ["docker"],
    "Linux": ["linux"],
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "reactjs"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Streamlit": ["streamlit"],
    "REST API": ["rest api", "rest apis", "restful"],
    "Excel": ["excel"],
    "Power BI": ["power bi", "powerbi"],
    "Communication": ["communication"],
    "Teamwork": ["teamwork", "team player", "collaboration"],
}


def _contains(text, alias):
    """True if alias appears as a whole word/phrase ('java' must not match 'javascript')."""
    pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
    return re.search(pattern, text) is not None


def extract_skills(text):
    """Return a sorted list of canonical skills found in the text."""
    text = text.lower()
    return sorted(
        skill for skill, aliases in SKILLS.items()
        if any(_contains(text, a) for a in aliases)
    )


def compare_skills(cv_text, job_text):
    """Return (matched, missing) based on the skills the job asks for."""
    cv_skills = set(extract_skills(cv_text))
    job_skills = set(extract_skills(job_text))
    return sorted(job_skills & cv_skills), sorted(job_skills - cv_skills)