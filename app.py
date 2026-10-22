import streamlit as st
from utils import read_pdf, clean_text, load_skills, extract_skills, similarity

st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("AI Resume Screening & Job Matching")

skills = load_skills()
resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd = st.text_area("Paste the job description", height=200)

if st.button("Analyze"):
    if not resume_file or not jd.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        resume_text = clean_text(read_pdf(resume_file))
        jd_text = clean_text(jd)

        resume_skills = extract_skills(resume_text, skills)
        jd_skills = extract_skills(jd_text, skills)
        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills
        score = similarity(resume_text, jd_text)

        st.metric("Resume-Job Similarity", f"{score:.1f}%")
        st.success("Matching skills: " + (", ".join(sorted(matched)) or "None"))
        st.error("Missing skills: " + (", ".join(sorted(missing)) or "None"))
        if jd_skills:
            st.progress(len(matched) / len(jd_skills))
            st.caption(f"Skill match: {len(matched)} / {len(jd_skills)}")
