import streamlit as st
import pdfplumber
import pandas as pd
import io

# -----------------------
# Extract text from PDF
# -----------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

# -----------------------
# Sample skills list
# -----------------------
def load_skills():
    return [
        "Python", "Java", "C++", "SQL", "NoSQL", "Django", "Flask", "Pandas", "NumPy",
        "Machine Learning", "Deep Learning", "Data Analysis", "Data Visualization",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "REST API", "NLP",
        "CI/CD", "FastAPI", "PostgreSQL", "MongoDB"
    ]

# -----------------------
# Analyze resume vs JD
# -----------------------
def analyze_resume(resume_text, jd_text, skills):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    matched = [skill for skill in skills if skill.lower() in resume_words and skill.lower() in jd_words]
    missing = [skill for skill in skills if skill.lower() in jd_words and skill.lower() not in resume_words]
    
    score = len(matched) / len(skills) * 100
    return round(score, 2), matched, missing

# -----------------------
# Streamlit App UI
# -----------------------
st.set_page_config(page_title="Multi-Resume Analyzer", layout="wide")
st.title("📄 AI-Powered Resume Analyzer (Multi-Resume)")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])

# Upload multiple resumes
resume_files = st.file_uploader("Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if jd_file and resume_files:
    # Extract JD text
    if jd_file.type == "application/pdf":
        jd_text = extract_text_from_pdf(jd_file)
    else:
        jd_text = str(jd_file.read(), "utf-8")

    # Load skills
    skills = load_skills()

    # Store results
    results = []

    for file in resume_files:
        resume_text = extract_text_from_pdf(file)
        score, matched, missing = analyze_resume(resume_text, jd_text, skills)

        results.append({
            "Resume File": file.name,
            "Match Score (%)": score,
            "Matched Skills": ", ".join(matched),
            "Missing Skills": ", ".join(missing)
        })

    # Display as DataFrame
    df = pd.DataFrame(results)
    st.subheader("📊 Resume Match Results")
    st.dataframe(df)

    # Download results
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Results as CSV", data=csv, file_name="resume_analysis_report.csv", mime="text/csv")

else:
    st.info("👆 Please upload both job description and resumes to begin.")
