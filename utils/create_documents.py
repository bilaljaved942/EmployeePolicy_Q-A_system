"""Script to create realistic company policy documents with all values filled"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os

# Ensure documents directory exists
os.makedirs("documents", exist_ok=True)

def create_employment_contract():
    """Create a realistic employment contract with all values filled"""
    doc = SimpleDocTemplate("documents/Employment_Contract_XCorp.pdf", pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    # Realistic values
    contract_date = "January 15, 2024"
    employee_name = "Ahmed Hassan"
    employee_address = "House No. 45, Block C, Gulshan-e-Iqbal, Karachi, Pakistan"
    job_title = "Senior Software Engineer"
    department = "Software Development"
    supervisor_name = "Sarah Malik"
    base_salary = "150,000"
    start_date = "February 1, 2024"
    
    # Title
    story.append(Paragraph("EMPLOYMENT CONTRACT", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Introduction
    intro_text = f"""
    This Employment Contract ("Contract") is entered into on <b>{contract_date}</b> between 
    <b>XCorp Technologies Private Limited</b>, a company incorporated under the Companies Act, 
    2017 of Pakistan, having its registered office at 123 Business District, Karachi, Pakistan 
    ("Company" or "Employer"), and <b>{employee_name}</b>, residing at {employee_address} 
    ("Employee").
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Section 1: Position and Duties
    story.append(Paragraph("1. POSITION AND DUTIES", heading_style))
    story.append(Paragraph(
        f"The Employee is hereby employed in the position of <b>{job_title}</b> in the "
        f"<b>{department}</b> department. The Employee agrees to perform all duties assigned "
        "by the Company, including but not limited to those described in the job description "
        f"provided at the time of offer. The Employee shall report to <b>{supervisor_name}</b> "
        "or such other person as the Company may designate from time to time.",
        normal_style
    ))
    story.append(Paragraph(
        "The Employee agrees to devote full time and attention to the business of the Company "
        "and shall not engage in any other employment or business activity without the prior "
        "written consent of the Company.",
        normal_style
    ))
    
    # Section 2: Compensation
    story.append(Paragraph("2. COMPENSATION", heading_style))
    story.append(Paragraph(
        f"2.1 <b>Base Salary:</b> The Employee shall receive a monthly base salary of "
        f"<b>PKR {base_salary}</b>, payable on the last working day of each month, subject to "
        "applicable tax deductions and statutory contributions.",
        normal_style
    ))
    story.append(Paragraph(
        "2.2 <b>Performance Bonus:</b> The Employee may be eligible for performance-based "
        "bonuses as determined by the Company's management, subject to individual and company "
        "performance metrics.",
        normal_style
    ))
    story.append(Paragraph(
        "2.3 <b>Benefits:</b> The Employee shall be entitled to benefits as per the Company's "
        "HR Policy Handbook, including but not limited to health insurance, provident fund, "
        "and annual leave.",
        normal_style
    ))
    
    # Section 3: Probation Period
    story.append(Paragraph("3. PROBATION PERIOD", heading_style))
    story.append(Paragraph(
        f"3.1 The Employee shall be on probation for a period of <b>six (6) months</b> "
        f"commencing from the date of joining, which is <b>{start_date}</b>.",
        normal_style
    ))
    story.append(Paragraph(
        "3.2 During the probation period, the Employee's performance shall be evaluated "
        "monthly by the immediate supervisor. The evaluation shall assess technical "
        "competence, work quality, attendance, punctuality, and adherence to company policies.",
        normal_style
    ))
    story.append(Paragraph(
        "3.3 The probation period may be extended by up to three (3) months at the Company's "
        "discretion if performance requires further assessment. The Employee will be notified "
        "in writing of any extension.",
        normal_style
    ))
    story.append(Paragraph(
        "3.4 Either party may terminate this Contract during the probation period by providing "
        "seven (7) days written notice without assigning any reason.",
        normal_style
    ))
    
    # Section 4: Confirmation and Increment
    story.append(Paragraph("4. CONFIRMATION AND INCREMENT", heading_style))
    story.append(Paragraph(
        "4.1 Upon successful completion of the probation period with satisfactory performance "
        "ratings, the Employee shall be confirmed in writing by the Company.",
        normal_style
    ))
    story.append(Paragraph(
        "4.2 Confirmed employees shall be eligible for a salary increment as defined in the "
        "Company's Increment & Probation Policy (Clause 5.2), typically ranging from 8% to "
        "12% of base salary, subject to performance evaluation and management approval.",
        normal_style
    ))
    story.append(Paragraph(
        "4.3 The increment, if approved, shall be effective from the first day of the month "
        "following confirmation.",
        normal_style
    ))
    
    # Section 5: Working Hours
    story.append(Paragraph("5. WORKING HOURS", heading_style))
    story.append(Paragraph(
        "5.1 The Employee's standard working hours are <b>9:00 AM to 6:00 PM</b>, Monday "
        "through Friday, with a one-hour lunch break.",
        normal_style
    ))
    story.append(Paragraph(
        "5.2 The Employee may be required to work additional hours, including evenings and "
        "weekends, as business needs require. Overtime compensation shall be provided as per "
        "applicable labor laws and company policy.",
        normal_style
    ))
    
    # Section 6: Leave Entitlements
    story.append(Paragraph("6. LEAVE ENTITLEMENTS", heading_style))
    story.append(Paragraph(
        "6.1 The Employee shall be entitled to leave benefits as per the Company's HR Policy "
        "Handbook, including annual leave, sick leave, and casual leave.",
        normal_style
    ))
    story.append(Paragraph(
        "6.2 All leave requests must be submitted in advance through the Company's leave "
        "management system and require approval from the immediate supervisor.",
        normal_style
    ))
    
    # Section 7: Confidentiality
    story.append(Paragraph("7. CONFIDENTIALITY AND NON-DISCLOSURE", heading_style))
    story.append(Paragraph(
        "7.1 The Employee acknowledges that during employment, they will have access to "
        "confidential and proprietary information, including but not limited to trade secrets, "
        "customer lists, business strategies, financial information, and technical data.",
        normal_style
    ))
    story.append(Paragraph(
        "7.2 The Employee agrees to maintain strict confidentiality of all such information "
        "during and after employment, and shall not disclose, use, or exploit such information "
        "for personal benefit or to the detriment of the Company.",
        normal_style
    ))
    story.append(Paragraph(
        "7.3 This obligation shall survive termination of employment and shall remain in effect "
        "indefinitely with respect to trade secrets and for a period of two (2) years with "
        "respect to other confidential information.",
        normal_style
    ))
    
    # Section 8: Intellectual Property
    story.append(Paragraph("8. INTELLECTUAL PROPERTY", heading_style))
    story.append(Paragraph(
        "8.1 All inventions, discoveries, improvements, works of authorship, and other "
        "intellectual property created by the Employee during the course of employment, "
        "whether or not during working hours, shall be the exclusive property of the Company.",
        normal_style
    ))
    story.append(Paragraph(
        "8.2 The Employee agrees to assign all rights, title, and interest in such intellectual "
        "property to the Company and to execute any documents necessary to perfect such assignment.",
        normal_style
    ))
    
    # Section 9: Non-Compete
    story.append(Paragraph("9. NON-COMPETE AND NON-SOLICITATION", heading_style))
    story.append(Paragraph(
        "9.1 During employment and for a period of <b>six (6) months</b> after termination, "
        "the Employee shall not, directly or indirectly, engage in any business that competes "
        "with the Company's business within Pakistan.",
        normal_style
    ))
    story.append(Paragraph(
        "9.2 The Employee agrees not to solicit, recruit, or hire any employee of the Company "
        "for a period of twelve (12) months after termination of employment.",
        normal_style
    ))
    
    # Section 10: Termination
    story.append(Paragraph("10. TERMINATION", heading_style))
    story.append(Paragraph(
        "10.1 <b>Termination by Employee:</b> After confirmation, the Employee may terminate "
        "this Contract by providing thirty (30) days written notice to the Company.",
        normal_style
    ))
    story.append(Paragraph(
        "10.2 <b>Termination by Company:</b> After confirmation, the Company may terminate "
        "this Contract by providing thirty (30) days written notice or payment in lieu of notice.",
        normal_style
    ))
    story.append(Paragraph(
        "10.3 <b>Termination for Cause:</b> Either party may terminate this Contract immediately "
        "for cause, including but not limited to gross misconduct, breach of confidentiality, "
        "fraud, or violation of company policies.",
        normal_style
    ))
    story.append(Paragraph(
        "10.4 Upon termination, the Employee shall return all company property, including "
        "laptops, access cards, documents, and any confidential materials.",
        normal_style
    ))
    
    # Section 11: Governing Law
    story.append(Paragraph("11. GOVERNING LAW AND DISPUTE RESOLUTION", heading_style))
    story.append(Paragraph(
        "11.1 This Contract shall be governed by and construed in accordance with the laws of "
        "Pakistan.",
        normal_style
    ))
    story.append(Paragraph(
        "11.2 Any disputes arising out of or relating to this Contract shall first be resolved "
        "through good faith negotiation. If unresolved, disputes shall be referred to "
        "arbitration in accordance with the Arbitration Act of Pakistan.",
        normal_style
    ))
    
    # Section 12: General Provisions
    story.append(Paragraph("12. GENERAL PROVISIONS", heading_style))
    story.append(Paragraph(
        "12.1 This Contract constitutes the entire agreement between the parties and supersedes "
        "all prior agreements and understandings.",
        normal_style
    ))
    story.append(Paragraph(
        "12.2 Any modification to this Contract must be in writing and signed by both parties.",
        normal_style
    ))
    story.append(Paragraph(
        "12.3 If any provision of this Contract is found to be invalid or unenforceable, the "
        "remaining provisions shall remain in full force and effect.",
        normal_style
    ))
    
    # Signatures
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("IN WITNESS WHEREOF, the parties have executed this Contract:", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>XCorp Technologies Private Limited</b>", normal_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("_________________________", normal_style))
    story.append(Paragraph("Muhammad Ali Khan", normal_style))
    story.append(Paragraph("Chief Human Resources Officer", normal_style))
    story.append(Paragraph("Date: " + contract_date, normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>{employee_name}</b>", normal_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("_________________________", normal_style))
    story.append(Paragraph("Employee Signature", normal_style))
    story.append(Paragraph("Date: " + contract_date, normal_style))
    
    doc.build(story)
    print("Created Employment_Contract_XCorp.pdf")

def create_hr_policy_handbook():
    """Create a realistic HR Policy Handbook"""
    doc = SimpleDocTemplate("documents/HR_Policy_Handbook_XCorp.pdf", pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#34495e',
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    # Title
    story.append(Paragraph("HR POLICY HANDBOOK", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("XCorp Technologies Private Limited", ParagraphStyle('Subtitle', parent=normal_style, alignment=TA_CENTER, fontSize=12)))
    story.append(Paragraph("Effective Date: January 1, 2024", ParagraphStyle('Date', parent=normal_style, alignment=TA_CENTER, fontSize=9)))
    story.append(Paragraph("Document Version: 3.1 | Last Updated: January 1, 2024", ParagraphStyle('Date', parent=normal_style, alignment=TA_CENTER, fontSize=9)))
    story.append(Spacer(1, 0.2*inch))
    
    # Introduction
    intro_text = """
    This Human Resources Policy Handbook ("Handbook") outlines the policies, procedures, and 
    guidelines applicable to all employees of XCorp Technologies Private Limited ("Company" 
    or "XCorp"). This Handbook is designed to provide employees with a clear understanding of 
    their rights, responsibilities, and the Company's expectations.
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(Paragraph(
        "<b>Note:</b> This Handbook is not a contract of employment and may be modified by "
        "the Company at any time. Employees will be notified of significant policy changes.",
        normal_style
    ))
    story.append(PageBreak())
    
    # Section 1: Company Overview
    story.append(Paragraph("1. COMPANY OVERVIEW", heading_style))
    story.append(Paragraph(
        "XCorp Technologies Private Limited is a leading technology solutions provider "
        "specializing in software development, IT consulting, and digital transformation "
        "services. Founded in 2015, the Company is committed to innovation, excellence, and "
        "employee development.",
        normal_style
    ))
    story.append(Paragraph(
        "Our mission is to deliver cutting-edge technology solutions while fostering a "
        "collaborative, inclusive, and growth-oriented work environment.",
        normal_style
    ))
    story.append(Paragraph(
        "<b>Company Contact Information:</b><br/>"
        "Address: 123 Business District, Karachi, Pakistan<br/>"
        "Phone: +92-21-1234-5678<br/>"
        "Email: hr@xcorp.com.pk<br/>"
        "Website: www.xcorp.com.pk",
        normal_style
    ))
    
    # Section 2: Code of Conduct
    story.append(Paragraph("2. CODE OF CONDUCT", heading_style))
    story.append(Paragraph(
        "All employees are expected to maintain the highest standards of professional conduct "
        "and ethics. The following principles guide our behavior:",
        normal_style
    ))
    story.append(Paragraph("<b>2.1 Professionalism:</b>", subheading_style))
    story.append(Paragraph(
        "Employees must conduct themselves professionally at all times, treating colleagues, "
        "clients, and stakeholders with respect and dignity.",
        normal_style
    ))
    story.append(Paragraph("<b>2.2 Integrity:</b>", subheading_style))
    story.append(Paragraph(
        "Honesty, transparency, and ethical behavior are fundamental to our operations. "
        "Employees must avoid conflicts of interest and report any unethical conduct.",
        normal_style
    ))
    story.append(Paragraph("<b>2.3 Compliance:</b>", subheading_style))
    story.append(Paragraph(
        "All employees must comply with applicable laws, regulations, and company policies. "
        "Violations may result in disciplinary action, including termination.",
        normal_style
    ))
    
    # Section 3: Working Hours
    story.append(Paragraph("3. WORKING HOURS", heading_style))
    story.append(Paragraph(
        "3.1 <b>Standard Hours:</b> The standard working hours are 9:00 AM to 6:00 PM, "
        "Monday through Friday, with a one-hour lunch break from 1:00 PM to 2:00 PM.",
        normal_style
    ))
    story.append(Paragraph(
        "3.2 <b>Flexible Hours:</b> Employees may request flexible working hours with prior "
        "approval from their supervisor, provided core hours (10:00 AM to 4:00 PM) are covered.",
        normal_style
    ))
    story.append(Paragraph(
        "3.3 <b>Remote Work:</b> Remote work arrangements may be available based on job "
        "requirements and performance. Requests must be approved by department heads.",
        normal_style
    ))
    story.append(Paragraph(
        "3.4 <b>Overtime:</b> Overtime work requires prior approval. Compensatory time off or "
        "overtime pay will be provided as per applicable labor laws.",
        normal_style
    ))
    
    # Section 4: Attendance and Punctuality
    story.append(Paragraph("4. ATTENDANCE AND PUNCTUALITY", heading_style))
    story.append(Paragraph(
        "4.1 Employees are expected to be punctual and maintain regular attendance. Late "
        "arrivals and early departures must be communicated to supervisors in advance.",
        normal_style
    ))
    story.append(Paragraph(
        "4.2 Excessive absenteeism or tardiness may result in disciplinary action. Employees "
        "with three or more unexcused absences in a month may be subject to a performance "
        "improvement plan.",
        normal_style
    ))
    story.append(Paragraph(
        "4.3 All employees must use the Company's attendance management system to record "
        "check-in and check-out times.",
        normal_style
    ))
    
    # Section 5: Leave Policy
    story.append(Paragraph("5. LEAVE POLICY", heading_style))
    story.append(Paragraph("<b>5.1 Annual Leave:</b>", subheading_style))
    story.append(Paragraph(
        "After confirmation, employees are entitled to 20 paid annual leave days per calendar "
        "year. Annual leave accrues monthly at a rate of 1.67 days per month.",
        normal_style
    ))
    story.append(Paragraph(
        "Annual leave must be requested at least 7 days in advance for planned absences. "
        "Approval is subject to business needs and team coverage.",
        normal_style
    ))
    story.append(Paragraph(
        "Unused annual leave may be carried forward up to 10 days to the next calendar year, "
        "subject to management approval.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.2 Sick Leave:</b>", subheading_style))
    story.append(Paragraph(
        "Employees are entitled to 10 paid sick leave days per calendar year. Sick leave "
        "requires a medical certificate for absences exceeding 3 consecutive days.",
        normal_style
    ))
    story.append(Paragraph(
        "Employees must notify their supervisor as soon as possible, preferably before the "
        "start of the workday, when taking sick leave.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.3 Casual Leave:</b>", subheading_style))
    story.append(Paragraph(
        "Employees may take up to 5 casual leave days per calendar year for personal matters. "
        "Casual leave requests should be submitted at least 2 days in advance.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.4 Public Holidays:</b>", subheading_style))
    story.append(Paragraph(
        "The Company observes all national public holidays as declared by the Government of "
        "Pakistan. Additional holidays may be declared by the Company for special occasions.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.5 Maternity/Paternity Leave:</b>", subheading_style))
    story.append(Paragraph(
        "Female employees are entitled to 90 days of paid maternity leave as per applicable "
        "laws. Male employees are entitled to 5 days of paid paternity leave.",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Section 6: Performance Reviews
    story.append(Paragraph("6. PERFORMANCE REVIEWS", heading_style))
    story.append(Paragraph(
        "6.1 <b>Review Frequency:</b> Performance reviews are conducted bi-annually (mid-year "
        "and year-end) for all confirmed employees.",
        normal_style
    ))
    story.append(Paragraph(
        "6.2 <b>Review Process:</b> Reviews assess technical skills, work quality, "
        "productivity, teamwork, communication, and adherence to company values. Employees "
        "receive written feedback and performance ratings.",
        normal_style
    ))
    story.append(Paragraph(
        "6.3 <b>Performance Ratings:</b> Ratings range from 'Exceeds Expectations' to 'Needs "
        "Improvement'. Ratings directly impact increment eligibility, promotions, and bonus "
        "consideration.",
        normal_style
    ))
    story.append(Paragraph(
        "6.4 <b>Performance Improvement Plans:</b> Employees with 'Needs Improvement' ratings "
        "may be placed on a Performance Improvement Plan (PIP) with specific goals and "
        "timelines.",
        normal_style
    ))
    
    # Section 7: Compensation and Benefits
    story.append(Paragraph("7. COMPENSATION AND BENEFITS", heading_style))
    story.append(Paragraph("<b>7.1 Salary:</b>", subheading_style))
    story.append(Paragraph(
        "Salaries are paid monthly on the last working day. Salary increments are based on "
        "performance reviews and company policies.",
        normal_style
    ))
    story.append(Paragraph("<b>7.2 Health Insurance:</b>", subheading_style))
    story.append(Paragraph(
        "The Company provides comprehensive health insurance coverage for employees and their "
        "dependents (spouse and children) after confirmation. Coverage includes hospitalization, "
        "outpatient services, and emergency care up to PKR 500,000 per annum.",
        normal_style
    ))
    story.append(Paragraph("<b>7.3 Provident Fund:</b>", subheading_style))
    story.append(Paragraph(
        "Employees contribute 8% of their basic salary to the Provident Fund, matched by an "
        "equal contribution from the Company, as per applicable laws.",
        normal_style
    ))
    story.append(Paragraph("<b>7.4 Professional Development:</b>", subheading_style))
    story.append(Paragraph(
        "The Company encourages continuous learning and provides training opportunities, "
        "conference attendance, and certification support based on job requirements and "
        "performance. Annual training budget of up to PKR 50,000 per employee is available.",
        normal_style
    ))
    
    # Section 8: IT and Security Policies
    story.append(Paragraph("8. IT AND SECURITY POLICIES", heading_style))
    story.append(Paragraph(
        "8.1 All company IT resources, including computers, software, and network access, are "
        "provided for business purposes only.",
        normal_style
    ))
    story.append(Paragraph(
        "8.2 Employees must maintain strong passwords and follow cybersecurity best practices. "
        "Sharing passwords or unauthorized access is strictly prohibited.",
        normal_style
    ))
    story.append(Paragraph(
        "8.3 Personal use of company IT resources should be minimal and must not interfere "
        "with work responsibilities.",
        normal_style
    ))
    story.append(Paragraph(
        "8.4 All company data must be backed up regularly, and sensitive information must be "
        "handled in accordance with data protection policies.",
        normal_style
    ))
    
    # Section 9: Grievance Procedure
    story.append(Paragraph("9. GRIEVANCE PROCEDURE", heading_style))
    story.append(Paragraph(
        "9.1 Employees who have concerns or grievances should first discuss them with their "
        "immediate supervisor.",
        normal_style
    ))
    story.append(Paragraph(
        "9.2 If unresolved, employees may escalate to the HR department or department head. "
        "All grievances will be handled confidentially and investigated promptly.",
        normal_style
    ))
    story.append(Paragraph(
        "9.3 The Company prohibits retaliation against employees who raise concerns in good faith.",
        normal_style
    ))
    story.append(Paragraph(
        "9.4 Grievances can be submitted via email to hr@xcorp.com.pk or through the HR portal.",
        normal_style
    ))
    
    # Section 10: Disciplinary Action
    story.append(Paragraph("10. DISCIPLINARY ACTION", heading_style))
    story.append(Paragraph(
        "Violations of company policies may result in disciplinary action, including verbal "
        "warnings, written warnings, suspension, or termination, depending on the severity "
        "of the offense.",
        normal_style
    ))
    story.append(Paragraph(
        "Serious violations, including fraud, theft, harassment, or breach of confidentiality, "
        "may result in immediate termination.",
        normal_style
    ))
    
    # Section 11: Health and Safety
    story.append(Paragraph("11. HEALTH AND SAFETY", heading_style))
    story.append(Paragraph(
        "11.1 The Company is committed to providing a safe and healthy work environment. "
        "Employees must follow all safety protocols and report any hazards immediately.",
        normal_style
    ))
    story.append(Paragraph(
        "11.2 Fire drills and safety training are conducted regularly. Employees must "
        "participate in all safety programs.",
        normal_style
    ))
    
    # Section 12: Dress Code
    story.append(Paragraph("12. DRESS CODE", heading_style))
    story.append(Paragraph(
        "Employees are expected to dress in business casual attire. Clothing should be neat, "
        "clean, and appropriate for a professional work environment. Client-facing roles may "
        "require formal business attire.",
        normal_style
    ))
    
    # Acknowledgment
    story.append(PageBreak())
    story.append(Paragraph("ACKNOWLEDGMENT", heading_style))
    story.append(Paragraph(
        "I acknowledge that I have received, read, and understood the HR Policy Handbook. "
        "I agree to comply with all policies and procedures outlined herein.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Employee Name: _________________________", normal_style))
    story.append(Paragraph("Employee ID: _________________________", normal_style))
    story.append(Paragraph("Designation: _________________________", normal_style))
    story.append(Paragraph("Department: _________________________", normal_style))
    story.append(Paragraph("Signature: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    doc.build(story)
    print("Created HR_Policy_Handbook_XCorp.pdf")

def create_increment_policy():
    """Create a realistic Increment and Probation Policy"""
    doc = SimpleDocTemplate("documents/Increment_and_Probation_Policy_XCorp.pdf", pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#34495e',
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    # Title
    story.append(Paragraph("INCREMENT & PROBATION POLICY", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("XCorp Technologies Private Limited", ParagraphStyle('Subtitle', parent=normal_style, alignment=TA_CENTER, fontSize=12)))
    story.append(Paragraph("Policy Version: 2.0 | Effective Date: January 1, 2024", ParagraphStyle('Date', parent=normal_style, alignment=TA_CENTER, fontSize=9)))
    story.append(Spacer(1, 0.2*inch))
    
    # Introduction
    intro_text = """
    This policy document defines the rules, procedures, and guidelines related to employee 
    probation periods, confirmation processes, and salary increments at XCorp Technologies 
    Private Limited. This policy applies to all employees and supersedes all previous 
    versions.
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(PageBreak())
    
    # Section 5.1: Probation Period
    story.append(Paragraph("CLAUSE 5.1 - PROBATION PERIOD", heading_style))
    story.append(Paragraph("<b>5.1.1 Duration:</b>", subheading_style))
    story.append(Paragraph(
        "All new employees shall serve a probation period of six (6) months from the date "
        "of joining. This period allows both the employee and the Company to assess mutual "
        "fit and performance.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.1.2 Probation Evaluation Criteria:</b>", subheading_style))
    story.append(Paragraph(
        "Performance during probation shall be evaluated based on the following criteria:",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Technical Competence:</b> Demonstrated ability to perform job responsibilities "
        "and meet technical requirements",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Work Quality:</b> Accuracy, attention to detail, and adherence to quality standards",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Productivity:</b> Ability to complete tasks within deadlines and manage workload effectively",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Attendance and Punctuality:</b> Regular attendance and adherence to working hours",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Teamwork and Communication:</b> Collaboration with colleagues and effective "
        "communication skills",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Adaptability:</b> Ability to learn, adapt to company culture, and respond to feedback",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.1.3 Evaluation Schedule:</b>", subheading_style))
    story.append(Paragraph(
        "Formal evaluations shall be conducted at the end of months 1, 3, and 6. Monthly "
        "informal check-ins are also conducted to provide ongoing feedback.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.1.4 Probation Extension:</b>", subheading_style))
    story.append(Paragraph(
        "The probation period may be extended by up to three (3) months if:",
        normal_style
    ))
    story.append(Paragraph(
        "• Performance requires further assessment but shows potential for improvement",
        normal_style
    ))
    story.append(Paragraph(
        "• The employee has been absent for more than 15 days during probation",
        normal_style
    ))
    story.append(Paragraph(
        "• Additional training or support is needed to meet performance standards",
        normal_style
    ))
    story.append(Paragraph(
        "The employee will be notified in writing at least 7 days before the original "
        "probation end date if an extension is required.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.1.5 Probation Completion Requirements:</b>", subheading_style))
    story.append(Paragraph(
        "To successfully complete probation, employees must:",
        normal_style
    ))
    story.append(Paragraph(
        "• Receive 'Meets Expectations' or higher ratings in all evaluation criteria",
        normal_style
    ))
    story.append(Paragraph(
        "• Complete all mandatory training programs",
        normal_style
    ))
    story.append(Paragraph(
        "• Maintain satisfactory attendance (minimum 90% attendance rate)",
        normal_style
    ))
    story.append(Paragraph(
        "• Demonstrate alignment with company values and culture",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Section 5.2: Increment After Probation
    story.append(Paragraph("CLAUSE 5.2 - INCREMENT AFTER PROBATION", heading_style))
    story.append(Paragraph("<b>5.2.1 Eligibility:</b>", subheading_style))
    story.append(Paragraph(
        "Permanent employees who successfully complete their probation period are eligible "
        "for a salary increment upon confirmation. The increment is subject to:",
        normal_style
    ))
    story.append(Paragraph(
        "• Satisfactory performance ratings during probation",
        normal_style
    ))
    story.append(Paragraph(
        "• Completion of all probation requirements",
        normal_style
    ))
    story.append(Paragraph(
        "• Management approval and budget availability",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.2.2 Increment Range:</b>", subheading_style))
    story.append(Paragraph(
        "The increment percentage is determined based on performance evaluation and typically "
        "ranges from 8% to 12% of the base salary:",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>8% - 9%:</b> Meets Expectations - Satisfactory performance meeting all basic requirements",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>10% - 11%:</b> Exceeds Expectations - Strong performance exceeding basic requirements",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>12%:</b> Outstanding Performance - Exceptional performance with significant contributions",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.2.3 Increment Calculation:</b>", subheading_style))
    story.append(Paragraph(
        "The increment is calculated on the base salary (excluding allowances and bonuses). "
        "The final increment percentage is determined by:",
        normal_style
    ))
    story.append(Paragraph(
        "• Overall performance rating (60% weight)",
        normal_style
    ))
    story.append(Paragraph(
        "• Technical competence and skill development (25% weight)",
        normal_style
    ))
    story.append(Paragraph(
        "• Team contribution and cultural fit (15% weight)",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.2.4 Effective Date:</b>", subheading_style))
    story.append(Paragraph(
        "The increment, if approved, shall be effective from the first day of the month "
        "following the confirmation date. For example, if confirmed on March 15, the "
        "increment will be effective from April 1.",
        normal_style
    ))
    
    story.append(Paragraph("<b>5.2.5 Increment Approval Process:</b>", subheading_style))
    story.append(Paragraph(
        "1. Immediate supervisor completes probation evaluation form",
        normal_style
    ))
    story.append(Paragraph(
        "2. HR department reviews evaluation and compliance with policy",
        normal_style
    ))
    story.append(Paragraph(
        "3. Department head approves increment percentage",
        normal_style
    ))
    story.append(Paragraph(
        "4. Final approval from Chief Human Resources Officer or CEO",
        normal_style
    ))
    story.append(Paragraph(
        "5. Employee receives written confirmation letter with increment details",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Section 5.3: Annual Increments
    story.append(Paragraph("CLAUSE 5.3 - ANNUAL INCREMENTS", heading_style))
    story.append(Paragraph(
        "5.3.1 Confirmed employees are eligible for annual increments based on performance "
        "reviews conducted bi-annually. Annual increment percentages range from 5% to 15%, "
        "based on performance ratings and market conditions.",
        normal_style
    ))
    story.append(Paragraph(
        "5.3.2 Annual increments are typically effective from January 1st of each year, "
        "subject to performance review completion and budget approval.",
        normal_style
    ))
    
    # Section 5.4: Promotion Policy
    story.append(Paragraph("CLAUSE 5.4 - PROMOTION POLICY", heading_style))
    story.append(Paragraph(
        "5.4.1 Promotions are based on performance, skill development, and business needs. "
        "Employees must have completed at least 12 months in their current role to be "
        "eligible for promotion.",
        normal_style
    ))
    story.append(Paragraph(
        "5.4.2 Promotions typically include a salary increase of 15% to 25% above the "
        "increment percentage, depending on the new role's responsibilities and market rates.",
        normal_style
    ))
    
    # Section 5.5: Performance Improvement Plans
    story.append(Paragraph("CLAUSE 5.5 - PERFORMANCE IMPROVEMENT PLANS", heading_style))
    story.append(Paragraph(
        "5.5.1 Employees who do not meet performance expectations during probation may be "
        "placed on a Performance Improvement Plan (PIP) instead of immediate termination.",
        normal_style
    ))
    story.append(Paragraph(
        "5.5.2 A PIP includes specific, measurable goals, timelines (typically 30-60 days), "
        "and support resources. Regular check-ins are conducted to monitor progress.",
        normal_style
    ))
    story.append(Paragraph(
        "5.5.3 Successful completion of a PIP may result in confirmation with a standard "
        "increment. Failure to meet PIP goals may result in termination.",
        normal_style
    ))
    
    # Section 5.6: Appeals Process
    story.append(Paragraph("CLAUSE 5.6 - APPEALS PROCESS", heading_style))
    story.append(Paragraph(
        "5.6.1 Employees who disagree with their probation evaluation or increment decision "
        "may submit a written appeal to the HR department within 7 days of receiving the decision.",
        normal_style
    ))
    story.append(Paragraph(
        "5.6.2 Appeals will be reviewed by a committee including HR, department head, and "
        "an independent reviewer. The decision of the appeals committee is final.",
        normal_style
    ))
    story.append(Paragraph(
        "5.6.3 Appeals should be submitted via email to hr@xcorp.com.pk with subject line "
        "'Appeal - [Employee ID] - [Date]'.",
        normal_style
    ))
    
    # Section 5.7: Effective Date and Amendments
    story.append(Paragraph("CLAUSE 5.7 - EFFECTIVE DATE AND AMENDMENTS", heading_style))
    story.append(Paragraph(
        "5.7.1 This policy is effective from January 1st, 2024, and supersedes all previous "
        "versions of the Increment & Probation Policy.",
        normal_style
    ))
    story.append(Paragraph(
        "5.7.2 The Company reserves the right to amend this policy at any time. Employees "
        "will be notified of significant changes at least 30 days in advance.",
        normal_style
    ))
    story.append(Paragraph(
        "5.7.3 In case of any conflict between this policy and the Employment Contract, the "
        "Employment Contract shall prevail.",
        normal_style
    ))
    
    # Approval
    story.append(PageBreak())
    story.append(Paragraph("APPROVAL", heading_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("This policy has been reviewed and approved by:", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("_________________________", normal_style))
    story.append(Paragraph("Muhammad Ali Khan", normal_style))
    story.append(Paragraph("Chief Human Resources Officer", normal_style))
    story.append(Paragraph("Date: January 1, 2024", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("_________________________", normal_style))
    story.append(Paragraph("Fatima Sheikh", normal_style))
    story.append(Paragraph("Chief Executive Officer", normal_style))
    story.append(Paragraph("Date: January 1, 2024", normal_style))
    
    doc.build(story)
    print("Created Increment_and_Probation_Policy_XCorp.pdf")

if __name__ == "__main__":
    print("Creating realistic company documents with all values filled...")
    create_employment_contract()
    create_hr_policy_handbook()
    create_increment_policy()
    print("\nAll documents created successfully in the 'documents' folder!")
