import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_skills(path="skills.txt"):
    with open(path) as f:
        return [line.strip().lower() for line in f if line.strip()]


def extract_skills(text, skills):
    found = set()
    for s in skills:
        pattern = r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(s)
    return found


def similarity(resume, jd):
    vectors = TfidfVectorizer(stop_words="english").fit_transform([resume, jd])
    return cosine_similarity(vectors[0], vectors[1])[0][0] * 100
