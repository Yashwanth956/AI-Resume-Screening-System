# AI Resume Screening & Job Recommendation System

An AI-assisted resume analysis web application built with Python and Flask.

The system extracts information from PDF resumes, analyzes a candidate against a job description, calculates an ATS-style score, identifies skill gaps, recommends suitable IT job roles, generates improvement suggestions, stores previous analyses, and produces downloadable PDF reports.

---

## Project Overview

Recruiters and job seekers often need to compare resumes with job descriptions manually.

This project automates major parts of that process by extracting structured information from resumes and comparing it with the requirements of a target job.

The application performs:

- Resume parsing
- Candidate information extraction
- Resume skill extraction
- Education extraction
- Experience analysis
- Project extraction
- Job description skill extraction
- ATS scoring
- Resume-to-job matching
- Missing skill identification
- IT job role recommendation
- Resume improvement suggestions
- Analysis history storage
- Dashboard analytics
- PDF report generation

The current system is designed primarily for software and IT-related roles.

---

# Features

## 1. PDF Resume Upload

Users can upload a resume in PDF format.

The system extracts text from the uploaded document and processes the resume automatically.

---

## 2. Candidate Information Extraction

The application extracts information such as:

- Candidate name
- Email address
- Phone number

---

## 3. Resume Skill Extraction

The system identifies technical skills from the resume and normalizes common variations.

Examples include:

- Python
- Java
- C / C++
- JavaScript
- React
- Node.js
- Flask
- FastAPI
- SQL
- MongoDB
- Git
- Machine Learning
- Deep Learning
- NLP
- TensorFlow
- PyTorch
- Cybersecurity
- Cloud technologies

A centralized master skill database is used for normalization and matching.

---

## 4. Education Extraction

Education records are converted into structured information containing:

- Degree
- Institution
- Score / CGPA / Percentage
- Duration

Example:

```python
{
    "degree": "Bachelor of Technology",
    "institution": "Example University",
    "score": "CGPA: 8.4",
    "duration": "2022 - 2026"
}
```

---

## 5. Experience Analysis

The experience parser detects professional employment history and calculates total work experience.

It supports:

- Month-year ranges
- Year-only ranges
- Present / Current / Now
- Multiple employment periods
- Overlapping experience ranges
- Structured experience records
- Job title extraction

The parser attempts to avoid counting unrelated periods such as education or career breaks as professional experience.

---

## 6. Project Extraction

Projects are extracted into structured records.

Example:

```python
{
    "title": "AI Resume Screening System",
    "technologies": [
        "Python",
        "Flask",
        "NLP"
    ],
    "description": [
        "Built a resume screening application.",
        "Implemented skill-based job matching."
    ]
}
```

---

# Job Description Analysis

Users paste a target job description into the application.

The system detects technical skills mentioned in the JD and compares them with the candidate's resume.

Example:

```text
Job Description
       ↓
JD Skill Extraction
       ↓
Required Skills
       ↓
Resume Comparison
```

---

# Skill Matching

The application divides job skills into:

## Matching Skills

Skills present in both the resume and job description.

Example:

```text
Python
Git
SQL
Flask
```

## Missing Skills

Job-required skills that were not detected in the candidate's resume.

Example:

```text
Docker
AWS
FastAPI
PyTorch
```

---

# Job Match Score

The basic job skill match is calculated using:

```text
Matching Required Skills
------------------------- × 100
Total Required Skills
```

Example:

```text
Required Skills = 10
Matching Skills = 7

Job Match Score = 70%
```

The result is also represented using match categories such as:

- Strong Match
- Moderate Match
- Low Match

---

# ATS Scoring System

The ATS score evaluates multiple parts of the resume instead of relying only on skill overlap.

Current weighting:

| Component | Weight |
|---|---:|
| Skill Match | 40% |
| Keyword Match | 20% |
| Experience | 15% |
| Education | 10% |
| Projects | 10% |
| Resume Quality | 5% |

The final score is calculated as:

```text
Final ATS Score =

Skill Score × 0.40
+
Keyword Score × 0.20
+
Experience Score × 0.15
+
Education Score × 0.10
+
Project Score × 0.10
+
Resume Quality Score × 0.05
```

This creates a more balanced evaluation than using keyword matching alone.

---

# Job Role Recommendation

The system also recommends job roles independently from the entered job description.

This answers a different question:

```text
ATS / Job Match
Resume + Job Description
        ↓
How suitable is the candidate for this specific job?


Job Recommendation
Resume Skills
        ↓
Which IT roles best match the candidate's profile?
```

Possible recommendation areas include:

- AI / ML
- Data Science
- Python Development
- Backend Development
- Frontend Development
- Full Stack Development
- Java Development
- Database roles
- Cloud
- DevOps
- Cybersecurity
- Networking
- Testing
- Mobile Development

The application returns the top recommended roles with:

- Match score
- Matching skills
- Missing skills

---

# Resume Improvement Suggestions

The system generates practical suggestions based on the analysis.

Suggestions can include:

- Improving skill alignment
- Adding important job-related keywords
- Strengthening relevant projects
- Developing missing technical skills
- Improving alignment with recommended roles

The suggestion engine does not simply recommend keyword stuffing.

---

# Unsupported Job Description Detection

The project is focused primarily on IT and software-related job descriptions.

If a job description contains no supported IT skills, the result page displays a warning.

For example, a job description focused entirely on:

```text
Supply Chain
Lean Manufacturing
Kaizen
DMAIC
Plant Operations
```

may be outside the intended project scope.

The application warns the user that the resulting ATS/job-match score should not be considered reliable for that job description.

---

# Analysis History

Completed analyses are stored in a SQLite database.

Users can:

- View previous analyses
- Search analysis history
- Open an individual analysis
- Delete an analysis
- Revisit previous ATS results

---

# Dashboard

The dashboard provides an overview of stored analyses.

It includes information such as:

- Total analyses
- Average ATS score
- Average job match score
- Highest ATS score
- Highest job match score
- Match category distribution
- Recent analyses

---

# PDF Report Generation

Users can download a PDF report for saved analyses.

The report may include:

- Candidate information
- ATS score
- ATS component scores
- Job match
- Resume skills
- Required job skills
- Matching skills
- Missing skills
- Education
- Experience
- Projects
- Recommended roles
- Job description
- Resume suggestions

---

# Technology Stack

## Backend

- Python
- Flask

## Frontend

- HTML
- CSS
- Jinja2

## Resume Processing

- pdfplumber
- PyPDF2
- PyMuPDF

## Database

- SQLite

## PDF Reporting

- ReportLab

## Other Tools

- Git
- GitHub
- VS Code

---

# Project Architecture

```text
                   USER
                    │
                    ▼
             Upload Resume PDF
                    │
                    ▼
             Flask Application
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
   Resume Parser        Job Description
         │               Skill Extractor
         │                     │
         ▼                     ▼
 Candidate Details       Required Skills
 Skills
 Education
 Experience
 Projects
         │                     │
         └──────────┬──────────┘
                    ▼
             Matching Engine
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
    ATS Score   Job Match    Missing Skills
        │
        ▼
 Role Recommendation
        │
        ▼
 Suggestions Engine
        │
        ▼
      Results
        │
   ┌────┴────┐
   ▼         ▼
SQLite     PDF Report
Database
```

---

# Project Structure

```text
AI-Resume-Screening-System/
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py
│   ├── init_db.py
│   └── resume_screening.db
│
├── datasets/
│   └── skills.csv
│
├── models/
│
├── recommendation/
│
├── resume_parser/
│   ├── ats_scorer.py
│   ├── education.py
│   ├── experience.py
│   ├── jd_skill_extractor.py
│   ├── job_matcher.py
│   ├── job_roles.py
│   ├── keyword_matcher.py
│   ├── master_skills.py
│   ├── name_extractor.py
│   ├── parser.py
│   ├── project.py
│   ├── role_recommender.py
│   ├── section_parser.py
│   ├── sections.py
│   ├── skills.py
│   └── suggestions.py
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── home.css
│   │   ├── result.css
│   │   ├── history.css
│   │   ├── dashboard.css
│   │   └── analysis_detail.css
│   │
│   ├── images/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── 1_index.html
│   ├── 2_result.html
│   ├── 3_history.html
│   ├── 4_analysis_detail.html
│   └── 5_dashboard.html
│
├── trained_models/
│
├── uploads/
│
├── utils/
│
├── app.py
├── requirements.txt
├── README.md
│
├── test_ats.py
├── test_education.py
├── test_experience.py
├── test_full_pipeline.py
├── test_jd_skill_extractor.py
├── test_job_matcher.py
├── test_job_roles.py
├── test_job_skills.py
├── test_projects.py
├── test_recommender.py
├── test_sections.py
├── test_skills.py
├── test_all_resumes.py
├── test_database.py
├── test_experience_matrix.py
└── test_suggestions.py
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd AI-Resume-Screening-System
```

---

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

Or:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

# Running the Application

Start Flask:

```powershell
.\venv\Scripts\python.exe app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# Application Workflow

```text
1. Open Home Page

2. Upload Resume PDF

3. Paste Job Description

4. Click Analyze Resume

5. Resume information is extracted

6. Job skills are extracted

7. ATS score is calculated

8. Matching and missing skills are identified

9. Suitable job roles are recommended

10. Resume suggestions are generated

11. Analysis is saved to SQLite

12. Results are displayed

13. User can download a PDF report

14. Previous analyses are available through History

15. Aggregate results are available through Dashboard
```

---

# Testing

The project contains multiple test files for individual modules and full-pipeline validation.

Run individual tests using:

```powershell
.\venv\Scripts\python.exe test_skills.py
```

```powershell
.\venv\Scripts\python.exe test_education.py
```

```powershell
.\venv\Scripts\python.exe test_experience.py
```

```powershell
.\venv\Scripts\python.exe test_projects.py
```

```powershell
.\venv\Scripts\python.exe test_job_matcher.py
```

```powershell
.\venv\Scripts\python.exe test_recommender.py
```

```powershell
.\venv\Scripts\python.exe test_suggestions.py
```

For the full resume regression test:

```powershell
.\venv\Scripts\python.exe test_all_resumes.py
```

The regression suite is used to ensure that improvements for one resume do not break previously supported resume formats.

---

# Database

The project uses SQLite for persistent storage.

Database file:

```text
database/resume_screening.db
```

Main stored information includes:

- Analysis information
- Resume skills
- Job skills
- Matching skills
- Missing skills
- Education records
- Experience records
- Projects
- Job recommendations

---

# Main Pages

## Home

```text
/
```

Upload resume and enter job description.

## Result

Displays the current analysis.

## History

```text
/history
```

Displays saved resume analyses.

## Dashboard

```text
/dashboard
```

Displays aggregate analysis statistics.

## Analysis Detail

```text
/analysis/<analysis_id>
```

Displays a saved analysis.

## PDF Report

```text
/analysis/<analysis_id>/pdf
```

Downloads the saved analysis as a PDF report.

---

# Current Scope

The system currently focuses mainly on technical and IT-related profiles such as:

```text
Software Development
AI / Machine Learning
Data Science
Data Analytics
Frontend
Backend
Full Stack
Python
Java
Databases
Cloud
DevOps
Cybersecurity
Networking
Testing
```

It is not intended to provide reliable ATS analysis for every profession.

Examples of domains that may currently fall outside its supported skill catalog include:

```text
Manufacturing
Supply Chain Operations
Civil Engineering
Medical Roles
Finance-specialized Roles
Legal Roles
Non-technical Management
```

---

# Limitations

The project currently has several limitations:

- Only text-based PDF resumes are reliably supported.
- Scanned image resumes may require OCR.
- Skill detection depends on the maintained master skill database.
- Resume layouts vary widely and may affect extraction.
- ATS scoring is a project-defined scoring model and is not the scoring algorithm of any specific commercial ATS.
- Job role recommendations are limited to configured IT roles.
- Non-IT job descriptions may not produce meaningful skill-match scores.
- Semantic understanding is currently more limited than large language model-based resume analysis.

---

# Future Enhancements

Possible future improvements include:

- DOCX resume support
- OCR for scanned resumes
- Semantic skill matching
- Sentence-transformer embeddings
- Resume-to-JD similarity models
- Machine learning-based ranking
- LLM-powered resume feedback
- Dynamic job role database
- User accounts
- Recruiter login
- Candidate ranking
- Multi-resume batch upload
- Job posting management
- Cloud deployment
- REST API
- Export to Excel / CSV
- Interactive analytics charts

---

# Project Objective

The main objective of this project is to demonstrate how NLP-style text processing, structured resume parsing, skill normalization, scoring algorithms, recommendation systems, databases, and web development can be combined into a practical recruitment application.

---

# Disclaimer

This project is intended for academic, learning and demonstration purposes.

The ATS score is generated using the scoring logic implemented in this project and should not be considered identical to the scoring system used by commercial Applicant Tracking Systems.

Job recommendations and improvement suggestions should be treated as decision-support information rather than guaranteed hiring outcomes.

---

# Author

**Yashwanth**

B.Tech — Artificial Intelligence and Machine Learning

---

# Project Title

**AI Resume Screening & Job Recommendation System**