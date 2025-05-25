import datetime
import io
import zipfile
import tempfile
import pandas as pd
import PyPDF2
import streamlit as st
from utils.resume_parser import analyze_resume
from utils.jitsi_scheduler import schedule_jitsi_interview
from utils.email_sender import send_email
from utils.config import roles
from utils.rag_resume import build_job_db, match_resume_to_jobs

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text.lower()

st.set_page_config(page_title="Resume Analyzer + Interview Scheduler", layout="wide")
st.title("📄 AI-Powered Resume Analyzer & Interview Scheduler")

st.sidebar.title("📂 Navigation")
app_mode = st.sidebar.radio("Go to", ["Resume Analyzer", "Schedule Interview", "About"])

job_index, job_keys, job_embeddings = build_job_db(roles)

if app_mode == "Resume Analyzer":
    st.subheader("📑 Analyze Resume(s) using RAG and Auto-Schedule Interview")

    analyze_mode = st.radio("Select Analysis Mode", ["Single Resume", "Bulk Resumes"])

    if analyze_mode == "Single Resume":
        uploaded_resume = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])
        selected_role = st.selectbox("Select Job Role", list(roles.keys()))
        rag_score = None
        rag_suggested_role = None
        match_percentage = None

        if st.button("Analyze Resume"):
            if not uploaded_resume:
                st.warning("Please provide the resume.")
            else:
                with st.spinner("Analyzing resume with RAG..."):
                    resume_text = extract_text_from_pdf(uploaded_resume)
                    matches = match_resume_to_jobs(resume_text, job_index, job_keys, job_embeddings, top_k=1)
                    rag_suggested_role, rag_score = matches[0]
                    st.write(f"**RAG Suggested Role:** {rag_suggested_role}")
                    st.write(f"**RAG Similarity Score:** {rag_score:.2f}")

                    # Use the selected role for skill matching
                    role_data = roles[selected_role]
                    mandatory_skills = role_data["mandatory_skills"]
                    role_skills = role_data["skills"]
                    all_skills = mandatory_skills + role_skills
                    missing_all_skills = [skill for skill in all_skills if skill not in resume_text]
                    missing_mandatory_skills = [skill for skill in mandatory_skills if skill not in resume_text]
                    total_skills_found = [skill for skill in all_skills if skill in resume_text]
                    total_skills_count = len(all_skills)
                    match_percentage = (len(total_skills_found) / total_skills_count) * 100 if total_skills_count > 0 else 0

                    eligible = len(missing_mandatory_skills) == 0 and match_percentage >= 60

                    if eligible:
                        st.success(f"✅ Candidate is eligible for the role of {selected_role}.")
                    else:
                        st.error(f"❌ Candidate does not meet all mandatory requirements or minimum match percentage for {selected_role}.")

                    st.write(f"**Skills Found**: {', '.join(total_skills_found) if total_skills_found else 'None'}")
                    st.write(f"**Missing Mandatory Skills**: {', '.join(missing_mandatory_skills) if missing_mandatory_skills else 'None'}")
                    st.write(f"**Missing Skills (All)**: {', '.join(missing_all_skills) if missing_all_skills else 'None'}")
                    st.write(f"**Total Skills Matched**: {len(total_skills_found)} out of {total_skills_count}")
                    st.write(f"**Match Percentage**: {match_percentage:.2f}%")

        if rag_score is not None and rag_score * 100 >= 60 and selected_role is not None and match_percentage is not None and match_percentage >= 60:
            st.markdown("---")
            st.subheader("📅 Schedule Jitsi Interview")

            email_input = st.text_input("Enter Candidate Email")
            sender_email = st.text_input("Your Gmail Address")
            sender_password = st.text_input("Your Gmail Password", type="password")
            company_name = st.text_input("Company Name")
            job_role = st.text_input("Job Role", value=selected_role)

            if st.button("Schedule Now"):
                if not email_input or not sender_email or not sender_password or not company_name or not job_role:
                    st.warning("Please fill in all the fields.")
                else:
                    jitsi_link = schedule_jitsi_interview(email_input)
                    interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")

                    subject = f"Interview Invitation: {job_role}"
                    body = f"""
Interview Details:

Company: {company_name}
Position: {job_role}
Date & Time (UTC): {interview_time}
Meeting Link: {jitsi_link}

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}

Please join the meeting on time. We look forward to speaking with you.

Best Regards,
{company_name} Recruitment Team
"""

                    result = send_email(subject, body, email_input, sender_email, sender_password)

                    success_details = f"""
✅ Interview scheduled successfully!

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}
"""
                    st.success(success_details)
                    st.info(result)
        elif rag_score is not None and (rag_score * 100 < 60 or match_percentage is not None and match_percentage < 60):
            st.warning("RAG score and/or skill match percentage is not sufficient for interview scheduling (must be 60 or above).")

    elif analyze_mode == "Bulk Resumes":
        selected_role = st.selectbox("Select Job Role for Bulk Analysis", list(roles.keys()))
        st.info(f"All uploaded resumes will be analyzed for the role: **{selected_role}**")
        st.caption("💡 You can upload a ZIP file containing PDFs (recommended, up to 1GB) or select multiple PDF files directly.")
        uploaded_zip = st.file_uploader("Upload a ZIP file containing candidate resumes (PDFs, up to 1GB)", type=["zip"])
        uploaded_pdfs = st.file_uploader("Or upload multiple PDF files directly (hold Ctrl/Cmd to select multiple)", type=["pdf"], accept_multiple_files=True)

        if st.button("Analyze All Resumes"):
            if not uploaded_zip and not uploaded_pdfs:
                st.warning("Please upload a ZIP file or multiple PDF files.")
            else:
                results = []
                with st.spinner("Extracting and analyzing resumes..."):
                    pdf_streams = []
                    if uploaded_zip:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            zip_path = f"{tmpdir}/resumes.zip"
                            with open(zip_path, "wb") as f:
                                f.write(uploaded_zip.read())
                            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                pdf_files = [f for f in zip_ref.namelist() if f.lower().endswith(".pdf")]
                                for pdf_file in pdf_files:
                                    with zip_ref.open(pdf_file) as pdf_fp:
                                        pdf_streams.append((pdf_file, pdf_fp.read()))
                    else:
                        for pdf_file in uploaded_pdfs:
                            pdf_streams.append((pdf_file.name, pdf_file.read()))

                    for pdf_name, pdf_bytes in pdf_streams:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                            temp_pdf.write(pdf_bytes)
                            temp_pdf.flush()
                            resume_text = extract_text_from_pdf(temp_pdf.name)

                        rag_suggested_role, rag_score = match_resume_to_jobs(
                            resume_text, job_index, job_keys, job_embeddings, top_k=1
                        )[0]

                        role_data = roles[selected_role]
                        mandatory_skills = role_data["mandatory_skills"]
                        role_skills = role_data["skills"]
                        all_skills = mandatory_skills + role_skills
                        missing_all_skills = [skill for skill in all_skills if skill not in resume_text]
                        missing_mandatory_skills = [skill for skill in mandatory_skills if skill not in resume_text]
                        total_skills_found = [skill for skill in all_skills if skill in resume_text]
                        total_skills_count = len(all_skills)
                        match_percentage = (len(total_skills_found) / total_skills_count) * 100 if total_skills_count > 0 else 0
                        eligible = len(missing_mandatory_skills) == 0 and match_percentage >= 60

                        results.append({
                            "Candidate File": pdf_name,
                            "Analyzed Role": selected_role,
                            "RAG Suggested Role": rag_suggested_role,
                            "RAG Score": f"{rag_score:.2f}",
                            "Eligible": "Yes" if eligible else "No",
                            "Skills Found": ", ".join(total_skills_found),
                            "Missing Mandatory Skills": ", ".join(missing_mandatory_skills) if missing_mandatory_skills else "None",
                            "Missing All Skills": ", ".join(missing_all_skills) if missing_all_skills else "None",
                            "Total Skills Matched": f"{len(total_skills_found)}/{total_skills_count}",
                            "Match Percentage": f"{match_percentage:.2f}%"
                        })

                st.markdown(f"### Results for Role: **{selected_role}**")
                df = pd.DataFrame(results)
                st.dataframe(df)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="resume_analysis_results.csv",
                    mime="text/csv"
                )

elif app_mode == "Schedule Interview":
    st.subheader("📅 Schedule Jitsi Interview Manually")

    email_input = st.text_input("Enter Candidate Email")
    sender_email = st.text_input("Your Gmail Address")
    sender_password = st.text_input("Your Gmail Password", type="password")
    company_name = st.text_input("Company Name")
    job_role = st.text_input("Job Role")

    if st.button("Schedule Now"):
        if not email_input or not sender_email or not sender_password or not company_name or not job_role:
            st.warning("Please fill in all the fields.")
        else:
            jitsi_link = schedule_jitsi_interview(email_input)
            interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")

            subject = f"Interview Invitation: {job_role}"
            body = f"""
Interview Details:

Company: {company_name}
Position: {job_role}
Date & Time (UTC): {interview_time}
Meeting Link: {jitsi_link}

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}

Please join the meeting on time. We look forward to speaking with you.

Best Regards,
{company_name} Recruitment Team
"""

            result = send_email(subject, body, email_input, sender_email, sender_password)

            success_details = f"""
✅ Interview scheduled successfully!

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}
"""
            st.success(success_details)
            st.info(result)

elif app_mode == "About":
    st.header("About This App")
    st.markdown("""
**AI-Powered Resume Analyzer & Interview Scheduler**  
This platform leverages advanced AI (RAG) to analyze resumes, match candidates to job roles, and automate interview scheduling with Jitsi integration.  
- Analyze single or bulk resumes  
- Get RAG role suggestions and skill match breakdown  
- Schedule interviews automatically  
- Export results for bulk analysis  
- Streamline your recruitment process!
""")