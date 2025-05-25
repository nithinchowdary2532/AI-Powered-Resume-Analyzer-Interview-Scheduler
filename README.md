# AI-Powered Resume Analyzer & Interview Scheduler

A comprehensive AI-driven platform to streamline your recruitment process. Analyze single or bulk resumes, match candidates to job roles using advanced RAG (Retrieval-Augmented Generation), and automate interview scheduling with Jitsi integration—all in one place.

---

## Features

- **Single Resume Analysis**

  - Upload a PDF resume and select a job role.
  - Get a RAG-suggested role and similarity score.
  - See detailed skill matching for your selected role.
  - **Candidate is automatically marked as "Shortlisted" if the RAG score is 60 or above.**
  - Eligibility check based on mandatory skills and ≥60% skill match.
  - Schedule interviews for eligible candidates with automated Jitsi meeting links and email notifications.

- **Bulk Resume Analysis**

  - Upload a ZIP file or multiple PDF resumes.
  - Select a job role for all resumes.
  - For each candidate, see:
    - RAG-suggested role and RAG score.
    - **Shortlisted status if RAG score is 60 or above.**
    - Skill match breakdown for the selected role.
    - Eligibility status (mandatory skills + ≥60% match).
  - Download results as a CSV file.

- **Automated Interview Scheduling**

  - Instantly generate Jitsi meeting links for eligible candidates.
  - Send interview invitations via email directly from the app.
  - Manual scheduling option for custom interviews.

- **Skill Insights**

  - View found and missing skills, missing mandatory skills, and match percentage for each candidate.
  - Clear eligibility status for every analysis.

- **Export & Reporting**

  - Download bulk analysis results as CSV for further review or reporting.

- **User-Friendly Interface**
  - Intuitive Streamlit dashboard for easy navigation.
  - Sidebar navigation for quick access to all features.
  - About section with app overview.

---

## How It Works

1. **Select Mode:** Choose between Single Resume or Bulk Resume analysis.
2. **Upload Resumes:** Upload a PDF (single) or ZIP/multiple PDFs (bulk).
3. **Select Job Role:** Pick the role for skill matching.
4. **Analyze:** View RAG suggestions, skill match, eligibility, and "Shortlisted" status if RAG score ≥ 60.
5. **Schedule Interview:** If eligible, schedule and send interview invites with Jitsi links.
6. **Export Results:** Download bulk results as CSV.

---

## Requirements

- Python 3.10 or 3.11
- See `requirements.txt` for dependencies

---

## Quick Start

```sh
git clone <your-repo-url>
cd AI-Powered-Recruitment-Assistant-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
├── app.py
├── utils/
│   ├── rag_resume.py
│   ├── resume_parser.py
│   ├── jitsi_scheduler.py
│   ├── email_sender.py
│   └── config.py
├── requirements.txt
└── README.md
```

---

## License

MIT License

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Jitsi Meet](https://meet.jit.si/)
- [HuggingFace Transformers](https://huggingface.co/transformers/)

---

**Automate, analyze, and schedule—smarter recruitment starts here!**
