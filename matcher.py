"""Matching logic between a CV and a job description."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import compare_skills


def calculate_similarity(cv_text, job_description):
    """TF-IDF cosine similarity between the two texts, from 0.0 to 1.0."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([cv_text, job_description])
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def generate_suggestions(matched, missing, score):
    """Honest suggestions. Never tells users to invent skills."""
    suggestions = []
    for skill in matched[:3]:
        suggestions.append(f"Highlight your {skill} projects or experience near the top of your CV.")
    for skill in missing[:3]:
        suggestions.append(
            f"The job mentions {skill}. If you have used it, add it with a concrete example; "
            f"if not, consider learning it through a small project."
        )
    if score < 50:
        suggestions.append("Tailor your CV wording to the job description using your real experience.")
    suggestions.append("Include relevant projects that demonstrate your technical skills.")
    return suggestions


def analyze_cv(cv_text, job_description):
    """Main backend function. Returns the agreed contract dictionary."""
    if not cv_text or not cv_text.strip():
        raise ValueError("CV text is empty. Upload a readable PDF.")
    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")

    matched, missing = compare_skills(cv_text, job_description)
    text_score = calculate_similarity(cv_text, job_description)

    total = len(matched) + len(missing)
    final = (0.6 * len(matched) / total + 0.4 * text_score) if total else text_score
    score = round(final * 100)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": generate_suggestions(matched, missing, score),
    }