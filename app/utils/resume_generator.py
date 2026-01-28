from fpdf import FPDF
from app.models.user import User
from app.models.job_seeker_profile import JobSeekerProfile

class PDFResponse(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        # self.cell(0, 10, 'Resume', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_resume_pdf(user: User, profile: JobSeekerProfile) -> bytes:
    pdf = PDFResponse()
    pdf.add_page()
    
    # Name and Role
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, user.full_name, 0, 1, 'L')
    
    if profile.desired_job:
        pdf.set_font('Arial', 'I', 14)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, profile.desired_job, 0, 1, 'L')
        pdf.set_text_color(0, 0, 0) # Reset color

    pdf.line(10, 35, 200, 35)
    pdf.ln(10)

    # Contact Info
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f'Email: {user.email}', 0, 1)
    if profile.phone:
        pdf.cell(0, 5, f'Phone: {profile.phone}', 0, 1)
    if profile.location:
        pdf.cell(0, 5, f'Location: {profile.location}', 0, 1)
    
    pdf.ln(10)

    # Summary
    if profile.skills:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Skills', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, profile.skills)
        pdf.ln(5)

    # Experience (Simple representation as we just have 'experience' integer in model for now)
    if profile.experience:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Experience', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f'{profile.experience} Years of Experience', 0, 1)
        pdf.ln(5)

    # Education
    if profile.education:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Education', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, profile.education)
        if profile.department:
             pdf.cell(0, 5, f'Department: {profile.department}', 0, 1)
        pdf.ln(5)

    # Additional Details
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Additional Information', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    if profile.expected_salary:
        pdf.cell(0, 5, f'Expected Salary: {profile.expected_salary}', 0, 1)
    if profile.preferred_work_location:
         pdf.cell(0, 5, f'Preferred Work Location: {profile.preferred_work_location}', 0, 1)

    return pdf.output(dest='S')
