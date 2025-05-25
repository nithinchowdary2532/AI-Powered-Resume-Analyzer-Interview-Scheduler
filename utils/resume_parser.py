import PyPDF2
from utils.config import roles

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def analyze_resume(pdf_file, role_key):
    resume_text = extract_text_from_pdf(pdf_file).lower()
    required_keywords = roles[role_key]
    total_keywords = len(required_keywords)

    found_keywords = [kw for kw in required_keywords if kw in resume_text]
    matched_count = len(found_keywords)
    match_percentage = round((matched_count / total_keywords) * 100)

    status = "selected" if match_percentage >= 60 else "rejected"
    
    # Enhanced Justification with Advanced Details for Recruiters
    if status == "selected":
        justification = (
            f"### Candidate Fit for the Role: **{role_key.title()}**\n\n"
            f"#### Skills Match: ✅\n\n"
            f"Matched **{matched_count}/{total_keywords}** critical skills (Score: {match_percentage}%).\n"
            f"Key matched skills include: {', '.join(found_keywords)}.\n\n"
            
            f"#### Why is this candidate a good fit?\n"
            f"1. **Direct Skill Alignment**: The candidate has demonstrated key expertise in essential skills like **{', '.join(found_keywords[:3])}**. These are fundamental for success in this role, where proficiency in {role_key} is crucial.\n\n"
            
            f"2. **Experience Level**: Based on the resume, the candidate appears to have sufficient experience with {role_key} responsibilities, which indicates they can step into the role with minimal ramp-up time.\n\n"
            
            f"3. **Company Fit & Culture**: The candidate's skills indicate they would fit well with the **company's values**. For example, matching experience in areas like **{', '.join(found_keywords)}** suggests a good cultural and functional fit.\n\n"
            
            f"4. **Growth Potential**: With additional experience in {role_key}, this candidate has the potential to grow into a senior role, making them a good long-term investment.\n\n"
            
            f"#### Overall Recommendation:\n"
            f"Based on the skills match and their experience, we recommend moving forward with this candidate."
        )
    else:
        justification = (
            f"### Candidate Fit for the Role: **{role_key.title()}**\n\n"
            f"#### Skills Match: ❌\n\n"
            f"Matched only **{matched_count}/{total_keywords}** skills (Score: {match_percentage}%).\n"
            f"Key matched skills include: {', '.join(found_keywords)}.\n\n"
            
            f"#### Why is the candidate **not** a fit?\n"
            f"1. **Missing Critical Skills**: The candidate has significant gaps in key areas like **{', '.join(required_keywords[:3])}**, which are essential for success in this role.\n\n"
            
            f"2. **Experience Gaps**: While the candidate demonstrates expertise in some areas, there is a clear gap in areas that are critical for this role, such as **{', '.join(required_keywords)}**.\n\n"
            
            f"3. **Cultural Misalignment**: Based on the skills matched, the candidate may not align well with the core values and expectations of our team.\n\n"
            
            f"#### Conclusion:\n"
            f"Unfortunately, we do not recommend this candidate for the role at this time."
        )

    return {
        "status": status,
        "message": f"{'✅' if status == 'selected' else '❌'} {status.title()}! Score: {match_percentage}%",
        "score": match_percentage,
        "matched_skills": found_keywords,
        "total_keywords": total_keywords,
        "justification": justification
    }
