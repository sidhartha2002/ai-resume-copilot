# 📄 AI Resume Copilot

> **Turn a resume into actionable, role-specific feedback with Gemini AI.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pydantic](https://img.shields.io/badge/Structured_Output-Pydantic-E92063)](https://docs.pydantic.dev/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-6A4EFC)](https://docs.astral.sh/uv/)

<!-- Replace this placeholder with your deployed Streamlit URL -->
[🚀 **Live Demo**](YOUR_STREAMLIT_APP_URL)

---

## 🎯 What is AI Resume Copilot?

**AI Resume Copilot** is a Streamlit-based application that reviews a resume against a target role and, optionally, a specific job description.

Instead of returning a generic AI paragraph, the application produces structured feedback covering:

- ✅ Strengths
- ⚠️ Areas to improve
- 🎯 Relevant skills
- 🧩 Missing or weakly demonstrated skills
- 🔑 Keyword gaps
- 💡 Actionable recommendations
- ✍️ Example rewritten resume bullets
- 📊 Estimated role-alignment score

The goal is to help users understand **how their current resume aligns with a specific opportunity and what they can improve next**.

> **Note:** The alignment score is an AI-generated estimate for this application. It is **not an official ATS score** and should not be treated as a hiring prediction.

---

## ✨ Why this project?

Most resume tools stop at:

```text
Upload Resume
      ↓
AI Feedback
```

This project goes one step further by combining:

```text
Resume PDF
     +
Target Role
     +
Optional Job Description
     ↓
PDF Text Extraction
     ↓
Gemini AI Analysis
     ↓
Structured Pydantic Output
     ↓
Actionable Resume Feedback
     ↓
Downloadable Report
```

This makes the application useful not only as an AI demo, but also as a practical example of building a complete AI-powered workflow.

---

## 🚀 Quick Demo

A typical interaction looks like this:

### Input

**Target Role**

```text
Python Developer
```

**Resume**

```text
resume.pdf
```

**Optional Job Description**

```text
We are looking for a Python Developer with experience
in Python, REST APIs, SQL, Git and software development.
Experience with FastAPI, testing and cloud technologies
is a plus.
```

### Output

```text
Estimated Role Alignment
82 / 100

Strengths
• Python development
• REST API experience
• Git

Missing / Weak Skills
• FastAPI
• Automated testing
• Cloud experience

Keyword Gaps
• CI/CD
• Docker
• FastAPI
```

The application then provides recommendations and example rewrites based only on information that already exists in the uploaded resume.

---

# 🧠 How It Works

The application follows a deterministic → AI → structured-output pipeline.

```text
                           USER
                             │
                             ▼
                    ┌────────────────┐
                    │  Streamlit UI  │
                    └───────┬────────┘
                            │
            ┌───────────────┼────────────────┐
            │               │                │
            ▼               ▼                ▼
        Resume PDF      Target Role     Job Description
            │               │                │
            ▼               │                │
        pypdf               │                │
            │               │                │
            ▼               └───────┬────────┘
       Resume Text                  │
            │                       │
            └──────────────┬────────┘
                           ▼
                  ┌──────────────────┐
                  │   Gemini Flash   │
                  └────────┬─────────┘
                           │
                           ▼
                  Structured JSON
                           │
                           ▼
                  ┌──────────────────┐
                  │ Pydantic Schema  │
                  │  ResumeReview    │
                  └────────┬─────────┘
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
         Strengths      Skill Gaps   Recommendations
             │             │              │
             └─────────────┼──────────────┘
                           ▼
                    Streamlit Results
                           │
                           ▼
                  Downloadable Report
```

---

# 🔍 Core Components

## 1. PDF Text Extraction

The uploaded PDF is processed locally using `pypdf`.

```text
PDF
 ↓
PdfReader
 ↓
Page text
 ↓
Combined resume text
```

This separation keeps document processing deterministic and independent from the AI layer.

### Important limitation

The current parser works best with **text-based PDFs**.

A scanned resume that contains only images may not produce useful text through `pypdf`. OCR/multimodal fallback is a possible future enhancement.

---

## 2. Gemini Resume Analysis

The extracted resume text is combined with:

- Target role
- Optional job description

and sent to Gemini for analysis.

The prompt explicitly instructs the model:

- Do not invent experience
- Do not invent technologies
- Do not invent certifications
- Do not invent achievements
- Base conclusions on supplied information
- Treat the alignment score as an estimate

---

## 3. Structured AI Output

Instead of depending on free-form text, the application defines a Pydantic schema:

```python
class ResumeReview(BaseModel):
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    keyword_gaps: list[str]
    recommendations: list[str]
    rewritten_bullets: list[str]
    estimated_match_score: int
```

This gives the application a predictable contract between the AI model and the UI.

---

## 4. Streamlit Interface

Streamlit provides the user-facing application.

The UI allows users to:

1. Enter a target role
2. Upload a PDF resume
3. Paste an optional job description
4. Run the analysis
5. Explore structured feedback
6. View extracted resume text
7. Download a Markdown analysis report

---

# ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Accepts resume PDFs |
| 🔎 Resume Extraction | Extracts text using `pypdf` |
| 🤖 Gemini Analysis | AI-powered resume review |
| 🎯 Role Alignment | Evaluates fit against a target role |
| 📋 Job Description Matching | Provides more targeted analysis when a JD is supplied |
| ✅ Strength Analysis | Highlights relevant strengths |
| 🧩 Skill Gap Analysis | Identifies missing or weakly demonstrated skills |
| 🔑 Keyword Gap Analysis | Surfaces potentially useful missing terms |
| 💡 Recommendations | Provides actionable improvement ideas |
| ✍️ Bullet Rewriting | Suggests stronger versions of existing bullets |
| 📊 Alignment Indicator | Generates an estimated 0–100 alignment score |
| ⬇️ Report Download | Download the analysis as Markdown |
| 🔐 Secret-safe Setup | API keys kept outside source control |

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core application |
| **Google Gen AI SDK** | Gemini API integration |
| **Gemini Flash** | Resume analysis |
| **Pydantic** | Structured AI output |
| **pypdf** | PDF text extraction |
| **Streamlit** | Web UI and deployment |
| **python-dotenv** | Local environment variables |
| **uv** | Environment and dependency management |
| **Git / GitHub** | Source control |

---

# 📁 Project Structure

```text
ai-resume-copilot/
│
├── app.py                    # Streamlit application
├── test_gemini.py            # Gemini API smoke test
├── test_parser.py            # PDF extraction test
├── test_review.py            # End-to-end AI review test
│
├── requirements.txt          # Deployment dependencies
├── pyproject.toml            # Python project configuration
├── uv.lock                   # Locked dependency graph
├── README.md
├── .gitignore
│
└── src/
    └── resume_critiquer/
        ├── __init__.py
        ├── resume_parser.py   # PDF → text
        ├── schemas.py         # Pydantic response schema
        ├── gemini_client.py   # Gemini analysis
        └── report_builder.py  # Downloadable report
```

---

# ⚙️ Local Development

## Prerequisites

Make sure you have:

- Python 3.12+
- Git
- `uv`
- A Gemini API key

---

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-copilot.git
cd ai-resume-copilot
```

---

## 2. Create the virtual environment

```bash
uv venv
```

---

## 3. Install dependencies

```bash
uv sync
```

---

## 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit this file.

---

## 5. Verify Gemini

Run:

```bash
uv run python test_gemini.py
```

Expected output:

```text
Gemini connection successful.
```

---

## 6. Verify PDF extraction

Place a text-based resume at:

```text
sample_resume.pdf
```

Then run:

```bash
uv run python test_parser.py
```

This should print the extracted resume text.

---

## 7. Verify AI review

Run:

```bash
uv run python test_review.py
```

This validates the pipeline:

```text
Resume PDF
    ↓
Text extraction
    ↓
Gemini
    ↓
Structured ResumeReview
```

---

## 8. Start the Streamlit application

```bash
uv run streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# ☁️ Deployment

The application is designed for deployment with **Streamlit Community Cloud**.

### Deployment flow

```text
Local Development
       │
       ▼
     GitHub
       │
       ▼
Streamlit Community Cloud
       │
       ▼
   Public Web App
```

### Entry point

```text
app.py
```

### Dependencies

```text
requirements.txt
```

### Secret

Configure the Gemini key through Streamlit Secrets:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

Do **not** commit `.env` or API keys to the repository.

---

# 🔐 Security & Privacy

## API keys

The Gemini API key is intentionally kept outside source control.

Local development:

```text
.env
```

Cloud deployment:

```text
Streamlit Secrets
```

The repository's `.gitignore` excludes:

```text
.env
.venv/
.streamlit/secrets.toml
```

## Resume data

This application processes resumes in order to generate the requested analysis. Users should avoid uploading confidential material unless they understand and accept the data-handling policies of the AI/API provider and deployment platform.

This project is a learning/portfolio application and should not be treated as a secure enterprise document-processing system.

---

# 🧪 Validation Strategy

The project deliberately separates testing into small checkpoints.

```text
test_gemini.py
      ↓
Gemini API works
```

```text
test_parser.py
      ↓
PDF extraction works
```

```text
test_review.py
      ↓
PDF → Gemini → structured output works
```

```text
app.py
      ↓
Full interactive application
```

This makes failures easier to isolate and debug.

---

# 🧱 Design Principles

### 1. Deterministic work stays deterministic

PDF extraction is handled by Python instead of asking an LLM to perform a task that a parser can handle directly.

### 2. AI is used for interpretation

Gemini is responsible for:

- Understanding resume content
- Comparing it with role context
- Identifying gaps
- Generating recommendations
- Rewriting existing bullets

### 3. AI output is structured

Pydantic provides a predictable schema between Gemini and the UI.

### 4. No fabricated experience

The prompt explicitly asks the model not to invent qualifications, technologies, achievements, or experience.

### 5. Evidence over a single number

The alignment score is only a summary indicator. The actionable information is in:

```text
Matched Skills
Missing Skills
Keyword Gaps
Recommendations
```

---

# 🧠 What I Learned

This project expands on the concepts from the first AI Agent project.

## AI / LLM concepts

- LLM API integration
- Prompt design
- Role-specific prompting
- Structured output
- Schema-constrained generation
- AI-assisted information extraction
- Practical limitations of LLM-generated scores

## Application engineering

- PDF processing
- File uploads
- Separating deterministic processing from AI reasoning
- Pydantic data models
- Streamlit state management
- Downloadable generated reports
- Error handling
- Environment variables and secrets

## Developer workflow

- `uv` project management
- Virtual environments
- Git
- GitHub
- Streamlit deployment
- Cloud secrets

---

# 🔬 Project Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                     Streamlit UI                         │
│                                                          │
│  Target Role │ Resume PDF │ Job Description             │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
               ┌───────────────┐
               │  PDF Parser   │
               │    pypdf      │
               └───────┬───────┘
                       │
                       ▼
                  Resume Text
                       │
                       ├────────────────────┐
                       │                    │
                       ▼                    ▼
                Target Role          Job Description
                       │                    │
                       └─────────┬──────────┘
                                 ▼
                       ┌─────────────────┐
                       │  Gemini Flash   │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Pydantic Model  │
                       │  ResumeReview   │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Streamlit UI    │
                       └────────┬────────┘
                                │
                                ▼
                      Downloadable Report
```

---

# ⚠️ Current Limitations

The current version intentionally keeps the scope focused.

### PDF limitations

- Text-based PDFs work best.
- Scanned/image-only resumes may produce little or no extractable text.
- Complex PDF layouts may not preserve visual formatting perfectly.

### AI limitations

- AI-generated recommendations can be imperfect.
- The alignment score is an estimate, not an actual ATS score.
- The application should not invent information that is not present in the resume.
- Recommendations should be reviewed by the user before applying them.

### Production limitations

This project currently does not include:

- Authentication
- Database storage
- Usage quotas
- Enterprise-grade document retention controls
- OCR fallback
- Automated evaluation benchmarks
- Full observability/tracing

---

# 🚧 Future Improvements

Planned enhancements:

- [ ] Add OCR support for scanned resumes
- [ ] Add DOCX support
- [ ] Add multiple job-description comparisons
- [ ] Add skill-gap visualization
- [ ] Add downloadable PDF report
- [ ] Add resume section scoring
- [ ] Add interview-question generation
- [ ] Add cover-letter assistance
- [ ] Add automated evaluation tests
- [ ] Add authentication
- [ ] Add usage/rate limiting
- [ ] Add observability and analytics
- [ ] Improve UI/UX for mobile users

---

# 🎓 Part of an Applied AI Learning Series

This is **Project 2** in a hands-on applied AI development journey.

```text
Project 1
🤖 Tool-Using AI Agent
        │
        ▼
Project 2
📄 AI Resume Copilot
        │
        ▼
Project 3
🖼️ AI Image Classifier
```

Each project intentionally introduces a different AI/application pattern:

| Project | Primary Concepts |
|---|---|
| 🤖 AI Agent | LLMs, tools, agents, orchestration |
| 📄 Resume Copilot | Document processing, structured output, LLM applications |
| 🖼️ Image Classifier | Computer vision, pretrained models, inference |

The objective is to learn **how to build practical AI-powered applications**, not just how to call an AI API.

---

# 👨‍💻 Author

**Sidhartha Mohanty**

B.Tech in Computer Science & Engineering  
Software Engineer | Frontend & UI/UX | Applied AI Learner

---

# ⭐ Feedback & Contributions

This is primarily a hands-on learning and portfolio project.

Ideas, feedback and improvements are welcome.

If you found the project useful, consider giving the repository a ⭐.
