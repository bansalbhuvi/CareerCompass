# 🧭 CareerCompass

CareerCompass is an AI-powered resume analysis and job-matching application that helps users understand how well their resume aligns with a given job description.

The application combines traditional NLP techniques with Generative AI to analyze resumes, identify skill gaps, calculate textual similarity, and provide AI-powered resume improvement suggestions.

---

## 🚀 Features

### 1. Resume Upload

Users can upload their resume in PDF format.

The application extracts the text from the resume using **PyMuPDF**.

### 2. Job Description Input

Users can enter the job description they want to compare their resume against.

### 3. Resume Match Score

CareerCompass calculates the textual similarity between the resume and job description using:

* TF-IDF
* Cosine Similarity

The result is displayed as a percentage-based Resume Match Score.

> Note: The match score represents textual similarity between the resume and job description. It is not a probability of getting an interview.

### 4. Skill Gap Analysis

The application identifies skills present in the resume and compares them with skills mentioned in the job description.

This helps users understand which relevant skills may be missing from their resume.

### 5. Rule-Based Resume Improvement

CareerCompass provides rule-based suggestions for improving resume bullet points.

This part uses Python logic and predefined rules to improve the wording of resume content.

### 6. AI Resume Improvement

The application uses a local Large Language Model to improve resume bullet points.

The AI is integrated using:

* Ollama
* Qwen3 8B
* Prompt Engineering

The prompt is designed to prevent the AI from inventing achievements, numbers, technologies, or experience.

### 7. AI Resume Review

CareerCompass can analyze the complete resume against a job description and provide:

* Overall resume review
* Resume strengths
* Skill gaps
* Resume improvement suggestions
* Project suggestions
* Action plan

---

## 🛠️ Technologies Used

| Technology          | Purpose                                 |
| ------------------- | --------------------------------------- |
| Python              | Core programming language               |
| Streamlit           | Web application interface               |
| PyMuPDF             | Extracting text from PDF resumes        |
| Scikit-learn        | NLP and similarity calculation          |
| TF-IDF              | Converting text into numerical features |
| Cosine Similarity   | Measuring textual similarity            |
| Regular Expressions | Skill detection and text processing     |
| Ollama              | Running the LLM locally                 |
| Qwen3 8B            | Generative AI model                     |
| Prompt Engineering  | Controlling AI-generated output         |

---

## 🤖 AI and NLP Concepts Used

CareerCompass uses a combination of traditional NLP and Generative AI.

### Traditional NLP

The application uses **TF-IDF** to represent resume and job-description text numerically.

Cosine Similarity is then used to calculate how similar the two text representations are.

### Rule-Based NLP

Regular expressions and predefined skill lists are used for skill detection and rule-based resume improvement.

### Generative AI

A locally running Qwen3 8B model is integrated through Ollama.

The model is used for:

* Resume bullet improvement
* Complete resume review
* Skill-gap interpretation
* Resume improvement suggestions

---

## 🏗️ Project Architecture

```text
                    CareerCompass
                          │
                ┌─────────┴─────────┐
                │                   │
             Resume            Job Description
                │                   │
                ▼                   ▼
          PDF Extraction       Text Processing
             PyMuPDF                 │
                │                    │
                └──────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
          TF-IDF + Cosine       Skill Detection
           Similarity             Regex
                 │                   │
                 ▼                   ▼
          Match Score            Skill Gaps
                 │
                 ▼
        Resume Improvement
             │       │
             │       └── Rule-Based Python
             │
             └────────── Local LLM
                         │
                       Ollama
                         │
                      Qwen3 8B
                         │
                         ▼
                  AI Resume Review
```

---

## 📂 Project Structure

```text
CareerCompass/
│
├── app.py
├── README.md
├── app_backup.py
│
└── .venv/
```

### Main Files

**app.py**
Contains the Streamlit application, NLP processing, skill-gap analysis, resume improvement logic, and AI integration.

**README.md**
Project documentation.

**app_backup.py**
Backup copy of the application created before final project modifications.

**.venv/**
Python virtual environment containing the project's dependencies.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd CareerCompass
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install streamlit pymupdf scikit-learn pandas ollama
```

### 5. Install Ollama

Install Ollama separately and make sure the required Qwen3 model is available locally.

Check available models using:

```bash
ollama list
```

The project currently uses:

```text
qwen3:8b
```

### 6. Run the application

```bash
python3 -m streamlit run app.py
```

The Streamlit application will open in your browser.

---

## 🔄 How the Application Works

### Step 1

The user uploads a PDF resume.

### Step 2

PyMuPDF extracts the resume text.

### Step 3

The user enters a target job description.

### Step 4

CareerCompass calculates the Resume Match Score using TF-IDF and Cosine Similarity.

### Step 5

The application detects skills and identifies potential skill gaps.

### Step 6

The user can improve individual resume bullet points using rule-based logic or the local AI model.

### Step 7

The AI Resume Review analyzes the complete resume against the job description and provides structured feedback.

---

## 🔐 Responsible AI Considerations

The AI prompts include constraints designed to reduce hallucination.

The system instructs the model not to:

* Invent achievements
* Invent numbers or percentages
* Invent technologies
* Invent responsibilities
* Claim experience that the user does not have

AI-generated suggestions should still be reviewed by the user before being added to a resume.

---

## 🔮 Future Improvements

Possible future improvements include:

* Better semantic resume-job matching using embeddings
* Support for multiple resume formats
* Resume section classification
* Job recommendation based on resume skills
* More advanced skill extraction using NLP models
* Resume report generation and download
* Database storage for previous analyses
* User authentication
* Deployment to a cloud platform

---

## 📸 Screenshots

Screenshots of the CareerCompass application can be added here after capturing the final application interface.

Example:

```text
![CareerCompass Dashboard](screenshots/dashboard.png)
```

---

## 🎯 Learning Outcomes

Through this project, I worked with:

* Python application development
* Streamlit
* Natural Language Processing
* TF-IDF
* Cosine Similarity
* Regular Expressions
* Prompt Engineering
* Large Language Models
* Local AI model integration
* PDF text extraction
* AI-powered application development

---

## 👩‍💻 Author

**Bhuvi Bansal**

CareerCompass — AI-powered Resume Analysis and Job Matching Application
