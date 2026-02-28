from fpdf import FPDF
from app.models.user import User
from app.models.job_seeker_profile import JobSeekerProfile

class PDFResponse(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        # self.cell(0, 10, 'Resume', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    """Clean text for Latin-1 compatibility with core FPDF fonts"""
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    # Encode to latin-1 and ignore characters that can't be represented
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_resume_pdf(user: User, profile: JobSeekerProfile, options: dict = None) -> bytes:
    if options is None:
        options = {"template": "professional", "show_salary": True, "show_location": True, "show_department": True}
    
    template = options.get("template", "professional")
    
    pdf = PDFResponse()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    
    # Template specific header/styles
    if template == "modern":
        pdf.set_fill_color(15, 23, 42) # Dark background for name section
        pdf.rect(0, 0, 210, 60, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('helvetica', 'B', 28)
        pdf.set_y(20)
        pdf.cell(0, 10, clean_text(user.full_name), 0, 1, 'C')
        if profile.desired_job:
            pdf.set_font('helvetica', 'I', 14)
            pdf.cell(0, 8, clean_text(profile.desired_job), 0, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(65)
    elif template == "minimal":
        pdf.set_font('helvetica', 'B', 32)
        pdf.cell(0, 20, clean_text(user.full_name.upper()), 0, 1, 'L')
        pdf.ln(2)
        pdf.line(15, pdf.get_y(), 60, pdf.get_y())
        pdf.ln(8)
    else: # Professional (Default)
        pdf.set_font('helvetica', 'B', 26)
        pdf.set_text_color(37, 99, 235) # Blue color for name
        pdf.cell(0, 12, clean_text(user.full_name), 0, 1, 'L')
        if profile.desired_job:
            pdf.set_font('helvetica', 'I', 14)
            pdf.set_text_color(71, 85, 105) # Slate color for job title
            pdf.cell(0, 8, clean_text(profile.desired_job), 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(8)

    # Contact Info
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Email:', 0, 0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(70, 6, clean_text(user.email), 0, 0)
    
    if profile.phone:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(15, 6, 'Phone:', 0, 0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(45, 6, clean_text(profile.phone), 0, 0)
    
    if profile.linkedin_url:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(18, 6, 'LinkedIn:', 0, 0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(0, 6, clean_text(profile.linkedin_url), 0, 1)
    else:
        pdf.ln(6)
        
    if profile.location:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(18, 6, 'Location:', 0, 0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(42, 6, clean_text(profile.location), 0, 0)

    if profile.github_url:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(15, 6, 'GitHub:', 0, 0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(0, 6, clean_text(profile.github_url), 0, 1)
    else:
        pdf.ln(6)
    
    pdf.ln(6)

    # Helper function for section headers
    def add_section_header(title):
        pdf.set_font('helvetica', 'B', 14)
        if template == "modern":
            pdf.set_fill_color(241, 245, 249)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 10, f'  {title.upper()}', 0, 1, 'L', True)
        else:
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 10, title, 'B', 1)
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)

    # Summary (About Me)
    if profile.summary:
        add_section_header('Professional Summary')
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, clean_text(profile.summary))
        pdf.ln(6)

    # Skills
    if profile.skills:
        add_section_header('Key Skills')
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, clean_text(profile.skills))
        pdf.ln(6)

    # Projects
    if profile.projects:
        add_section_header('Projects')
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, clean_text(profile.projects))
        pdf.ln(6)

    # Experience
    if profile.experience:
        add_section_header('Work Experience')
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, f'{profile.experience} years of professional experience in developing impactful solutions and achieving organizational goals.')
        pdf.ln(6)

    # Education
    if profile.education:
        add_section_header('Education')
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, clean_text(profile.education))
        if options.get("show_department", True) and profile.department:
             pdf.set_font('helvetica', 'I', 10)
             pdf.set_text_color(100, 100, 100)
             pdf.cell(0, 6, f'Department: {clean_text(profile.department)}', 0, 1)
             pdf.set_text_color(0, 0, 0)
        pdf.ln(6)

    # Secondary Info
    show_salary = options.get("show_salary", True)
    show_loc = options.get("show_location", True)
    
    if (show_salary and profile.expected_salary) or (show_loc and profile.preferred_work_location):
        add_section_header('Additional Information')
        pdf.set_font('helvetica', '', 11)
        
        if show_salary and profile.expected_salary:
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(40, 6, 'Expected Salary:', 0, 0)
            pdf.set_font('helvetica', '', 11)
            pdf.cell(0, 6, clean_text(profile.expected_salary), 0, 1)
            
        if show_loc and profile.preferred_work_location:
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(40, 6, 'Preferred Location:', 0, 0)
            pdf.set_font('helvetica', '', 11)
            pdf.cell(0, 6, clean_text(profile.preferred_work_location), 0, 1)

    return pdf.output()
