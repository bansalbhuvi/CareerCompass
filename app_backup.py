
import streamlit as st
import fitz
import re
import ollama

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------
# PAGE SETUP
# ---------------------------------

st.set_page_config(
    page_title="CareerCompass",
    page_icon="🧭",
    layout="wide"
)
st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }

    .block-container {
        max-width: 1200px;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    h1 {
        font-size: 3rem;
    }

    h2 {
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧭 CareerCompass")

st.subheader(
    "AI-Powered Resume Intelligence & Career Readiness"
)

st.write(
    "Analyze your resume against a job description, "
    "identify skill gaps, improve resume bullets, "
    "and receive AI-powered career feedback."
)

st.caption(
    "Powered by Python • NLP • Machine Learning • Local LLM"
)

st.divider()


# ---------------------------------
# SKILL DICTIONARY
# ---------------------------------

SKILLS = {
    "Python": ["python"],
    "C++": ["c++"],
    "C": ["c programming"],
    "Java": ["java"],
    "SQL": ["sql"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Excel": ["excel", "microsoft excel"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Communication": ["communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Git": ["git"],
    "GitHub": ["github"],
    "OOP": ["oop", "object oriented programming"],
    "Data Structures": ["data structures", "data structure"],
    "Algorithms": ["algorithms", "algorithm"],
    "Linux": ["linux"],
    "AWS": ["aws", "amazon web services"],
    "Docker": ["docker"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Streamlit": ["streamlit"]
}


# ---------------------------------
# SKILL DETECTION
# ---------------------------------

def find_skills(text):
    found_skills = []
    text = text.lower()

    for skill, variations in SKILLS.items():
        for variation in variations:
            pattern = (
                r"(?<!\w)"
                + re.escape(variation)
                + r"(?!\w)"
            )

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


# ---------------------------------
# DAY 5: RESUME BULLET IMPROVER
# ---------------------------------

def improve_resume_bullet(bullet, job_description):
    """
    Improves wording using simple Python rules.
    This is a free, rule-based feature, not a
    generative AI model.
    """

    original = bullet.strip()

    # Remove bullet symbols at the beginning
    original = re.sub(r"^[•\-*]+\s*", "", original)

    if not original:
        return None, []

    improved = original
    suggestions = []

    # 1. Replace common weak phrases
    replacements = {
        r"\bi made\b": "Developed",
        r"\bi created\b": "Created",
        r"\bi worked on\b": "Contributed to",
        r"\bi helped\b": "Supported",
        r"\bi did\b": "Completed",
        r"\bi used\b": "Applied",
        r"\bmade\b": "Developed",
        r"\bworked on\b": "Contributed to",
        r"\bhelped\b": "Supported",
        r"\bused\b": "Applied"
    }

    for pattern, replacement in replacements.items():
        new_text = re.sub(
            pattern,
            replacement,
            improved,
            flags=re.IGNORECASE
        )

        if new_text != improved:
            improved = new_text
            suggestions.append(
                f"Replaced a weak phrase with '{replacement}'."
            )

    # 2. Capitalize the first character
    if improved:
        improved = improved[0].upper() + improved[1:]

    # 3. Remove unnecessary spaces
    improved = re.sub(r"\s+", " ", improved).strip()

    # 4. Add a period if needed
    if improved and improved[-1] not in ".!?":
        improved += "."

    # 5. Find relevant skills from the job description
    job_skills = find_skills(job_description)
    bullet_skills = find_skills(original)

    relevant_skills = [
        skill for skill in job_skills
        if skill in bullet_skills
    ]

    if relevant_skills:
        suggestions.append(
            "This bullet already mentions relevant job skills: "
            + ", ".join(relevant_skills)
            + "."
        )
    else:
        suggestions.append(
            "Check whether you can accurately include a relevant "
            "skill from the job description."
        )

    # 6. Encourage evidence instead of invented achievements
    if not re.search(r"\d", improved):
        suggestions.append(
            "If you have real results, consider adding a number, "
            "such as users, time saved, or test cases completed."
        )

    # 7. Encourage specific tools and outcomes
    if len(original.split()) < 8:
        suggestions.append(
            "Consider adding more detail about what you built, "
            "how you built it, and the result."
        )

    return improved, suggestions

def improve_resume_bullet_with_ai(bullet, job_description):

    prompt = f"""
You are an expert resume assistant.

Analyze the user's resume bullet according to the job description.

Your task is to improve the bullet while being completely truthful.

IMPORTANT RULES:
1. Do not invent achievements.
2. Do not invent numbers or percentages.
3. Do not invent technologies.
4. Do not invent responsibilities.
5. Do not add skills that the user has not mentioned.
6. Do not claim experience that is not provided.
7. Keep the meaning of the original bullet.
8. Make the bullet professional and concise.

Return the response in exactly this format:

IMPROVED_BULLET:
<improved resume bullet>

WHY_IT_IS_BETTER:
<short explanation>

RELEVANT_SKILLS:
<comma-separated skills found in the bullet that are relevant to the job>

MISSING_INFORMATION:
<information that could make the bullet stronger if the user genuinely has it>

Original Resume Bullet:
{bullet}

Job Description:
{job_description}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()

def analyze_resume_with_ai(resume_text, job_description):

    prompt = f"""
You are an expert resume reviewer.

Analyze the candidate's resume against the job description.

Your goal is to provide useful, truthful and actionable feedback.

IMPORTANT RULES:
1. Use only information provided in the resume.
2. Do not invent skills, experience, projects or achievements.
3. Do not assume the candidate has a skill just because it appears
   in the job description.
4. Clearly distinguish between skills present in the resume and
   skills requested by the job description.
5. Do not make hiring predictions.
6. Keep the feedback concise and professional.

Return your response using exactly these sections:

OVERALL_REVIEW:
Give a short summary of how well the resume aligns with the job description.

RESUME_STRENGTHS:
List 3 strengths based only on the resume and job description.

SKILL_GAPS:
List important skills from the job description that are not detected
in the resume.

RESUME_IMPROVEMENTS:
Give 3 specific suggestions for improving the resume.

PROJECT_SUGGESTIONS:
Suggest how the candidate could better describe existing projects
to make them more relevant to the job.

ACTION_PLAN:
Give 3 practical next steps for the candidate.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()
# ---------------------------------
# RESUME UPLOAD
# ---------------------------------

st.header("1. Upload Your Resume")

resume_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

resume_text = ""

if resume_file is not None:
    try:
        pdf_document = fitz.open(
            stream=resume_file.getvalue(),
            filetype="pdf"
        )

        for page in pdf_document:
            resume_text += page.get_text()

        pdf_document.close()

        st.success("Resume uploaded and text extracted!")

        with st.expander("View extracted resume text"):
            st.text(resume_text)

    except Exception as error:
        st.error("Could not read this PDF.")
        st.caption(str(error))


# ---------------------------------
# JOB DESCRIPTION
# ---------------------------------

st.header("2. Enter the Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Paste the job requirements..."
)


# ---------------------------------
# DAY 3: RESUME MATCHING
# ---------------------------------

st.header("3. Resume Match Score")

if st.button("Analyze Resume", type="primary"):

    if not resume_text.strip():
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            documents = [
                resume_text,
                job_description
            ]

            vectorizer = TfidfVectorizer(
                stop_words="english"
            )

            vectors = vectorizer.fit_transform(documents)

            similarity = cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )[0][0]

            score = round(similarity * 100, 2)

            st.metric(
                "📊 Resume Match Score",
                f"{score}%"
            )

            st.progress(int(score))

            if score >= 70:
                st.success(
                    "Good textual alignment between the resume "
                    "and job description."
                )

            elif score >= 40:
                st.warning(
                    "Moderate textual alignment. Review the "
                    "job requirements and skill gaps."
                )

            else:
                st.info(
                    "The resume has relatively low textual similarity. "
                    "Review the job requirements and skill gaps carefully."
                )

            st.caption(
                "This is a text similarity score, not a "
                "probability of getting an interview."
            )

        except ValueError:
            st.warning(
                "Not enough meaningful text to calculate "
                "similarity. Please add more resume or job "
                "description text."
            )

# ---------------------------------
# DAY 4: SKILL GAP ANALYSIS
# ---------------------------------

st.header("4. Skill Gap Analysis")

if st.button("Find Skill Gaps"):

    if not resume_text.strip():
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description above.")

    else:
        resume_skills = find_skills(resume_text)
        job_skills = find_skills(job_description)

        matched_skills = [
            skill for skill in job_skills
            if skill in resume_skills
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_skills
        ]

        total_job_skills = len(job_skills)

        if total_job_skills > 0:
            skill_coverage = round(
                len(matched_skills) / total_job_skills * 100,
                2
            )
        else:
            skill_coverage = 0

        st.metric(
            "🎯 Skill Coverage",
            f"{skill_coverage}%"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.success(skill)
            else:
                st.write("No matching skills detected.")

        with col2:
            st.subheader("⚠️ Skill Gaps")

            if missing_skills:
                for skill in missing_skills:
                    st.warning(skill)
            else:
                st.success("No skill gaps detected.")

        st.caption(
            "A skill not detected in your resume does not "
            "necessarily mean you lack that skill."
        )

        st.divider()

st.header("📈 Resume Statistics")

word_count = len(resume_text.split())
character_count = len(resume_text)

# Detect resume skills independently
resume_skills = find_skills(resume_text)

stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.metric(
        "Words",
        word_count
    )

with stat2:
    st.metric(
        "Characters",
        character_count
    )

with stat3:
    st.metric(
        "Detected Skills",
        len(resume_skills)
    )


# ---------------------------------
# DAY 5: RESUME IMPROVEMENT UI
# ---------------------------------

st.divider()

st.header("5. AI-Style Resume Improvement")

st.write(
    "Enter one resume bullet point. CareerCompass will "
    "suggest clearer wording and give you tips for tailoring "
    "it to the job description."
)

resume_bullet = st.text_area(
    "Your current resume bullet",
    height=120,
    placeholder=(
        "Example: I made a website using HTML and CSS."
    ),
    key="resume_bullet"
)

if st.button("Improve My Resume Bullet"):

    if not resume_bullet.strip():
        st.warning("Please enter a resume bullet point.")

    elif not job_description.strip():
        st.warning(
            "Please enter a job description above "
            "so the tool can identify relevant skills."
        )

    else:
        improved_bullet, suggestions = improve_resume_bullet(
            resume_bullet,
            job_description
        )

        if improved_bullet:
            st.success("Suggested Resume Bullet")

            st.write(improved_bullet)

            st.button(
                "Copying tip: Select the text above "
                "and copy it into your resume.",
                disabled=True
            )

            st.subheader("Suggestions")

            for suggestion in suggestions:
                st.write("• " + suggestion)

            st.info(
                "Review the suggested wording carefully. "
                "Do not add skills, tools, responsibilities, "
                "or achievements that you did not actually have."
            )


# ---------------------------------
# FOOTER
# ---------------------------------
st.divider()

st.header("6. AI Resume Improvement")

st.write(
    "Use a local AI model to improve your resume bullet "
    "according to the job description."
)

ai_resume_bullet = st.text_area(
    "Enter a resume bullet for AI improvement",
    height=120,
    placeholder=(
        "Example: I made a website using HTML and CSS."
    ),
    key="ai_resume_bullet"
)

if st.button("Improve with Local AI"):

    if not ai_resume_bullet.strip():
        st.warning("Please enter a resume bullet.")

    elif not job_description.strip():
        st.warning(
            "Please enter a job description above."
        )

    else:

        with st.spinner(
            "CareerCompass AI is analyzing your resume bullet..."
        ):

            try:

                ai_result = improve_resume_bullet_with_ai(
                    ai_resume_bullet,
                    job_description
                )

                st.success("AI Analysis Complete")

                st.subheader("🤖 AI Result")

                st.write(ai_result)

                st.info(
                    "Always verify the AI-generated suggestion "
                    "before using it in your resume."
                )

            except Exception as error:

                st.error(
                    "Could not connect to the local AI model."
                )

                st.caption(str(error))

st.divider()

st.header("7. AI Resume Review")

st.write(
    "Get an AI-powered review of your complete resume "
    "based on the job description."
)

if st.button("Review My Resume with AI"):

    if not resume_text.strip():
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning(
            "Please enter a job description above."
        )

    else:

        with st.spinner(
            "CareerCompass AI is reviewing your resume..."
        ):

            try:

                ai_resume_review = analyze_resume_with_ai(
                    resume_text,
                    job_description
                )

                st.success("Resume Review Complete")

                st.subheader("🤖 AI Resume Review")

                with st.expander(
                    "View AI-generated resume review",
                    expanded=True
                ):
                    st.write(ai_resume_review)

                    st.info(
                        "This review is generated from the resume "
                        "and job description provided. Verify all "
                        "suggestions before making changes."
                    )

            except Exception as error:

                st.error(
                    "Could not generate the AI resume review."
                )

                st.caption(str(error))

st.divider()

st.caption(
    "CareerCompass is a resume-analysis prototype. "
    "AI-generated suggestions should be reviewed and verified "
    "before being added to a resume."
)