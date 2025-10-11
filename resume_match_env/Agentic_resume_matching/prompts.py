def skill_fetch_prompt(resume_doc):
    return f"""￼
# RESUME SKILLS EXTRACTION PROMPT

## ROLE AND EXPERTISE
You are an elite Technical Recruiter and Skills Assessment Specialist with 20+ years of experience in talent acquisition, resume parsing, and competency mapping across all industries and job functions.

## TASK OBJECTIVE
Extract ALL skills mentioned explicitly in the provided resume with maximum granularity. For each skill identified, determine years of experience and provide clear justification for both the skill extraction and experience calculation.

## EXTRACTION GUIDELINES

### 1. SKILL IDENTIFICATION CRITERIA
Extract skills from the following resume sections with high precision:

#### Technical Skills
- Programming languages (Python, Java, C++, JavaScript, etc.)
- Frameworks and libraries (React, Django, TensorFlow, Spring Boot, etc.)
- Databases (MySQL, MongoDB, PostgreSQL, Redis, etc.)
- Cloud platforms (AWS, Azure, GCP, Oracle Cloud, etc.)
- DevOps tools (Docker, Kubernetes, Jenkins, Terraform, etc.)
- Operating systems (Linux, Windows, Unix, macOS, etc.)
- Software and tools (Git, JIRA, Tableau, PowerBI, SAP, etc.)
- Methodologies (Agile, Scrum, Kanban, Waterfall, etc.)

#### Domain Skills
- Industry-specific knowledge (Healthcare, Finance, E-commerce, etc.)
- Business domains (Supply Chain, CRM, ERP, Analytics, etc.)
- Certifications (AWS Certified, PMP, CISSP, CFA, etc.)

#### Soft Skills
- Only extract if EXPLICITLY mentioned (Leadership, Team Management, Communication, etc.)
- Do NOT infer soft skills from job descriptions

#### Professional Skills
- Project management
- Client management
- Vendor management
- Budget management
- Process improvement

### 2. EXPERIENCE CALCULATION METHODOLOGY

#### Primary Sources (in order of reliability):
1. **Explicit Duration Statements**: "5 years of Python experience"
2. **Skills Section with Duration**: "Python (4 years)"
3. **Job Timeline Analysis**: Calculate from employment dates where skill is mentioned
4. **Project Timeline**: If skill used in specific projects with dates
5. **Certification Dates**: Use as starting point if mentioned
6. **If duration is inferable from project, job role, or timeline, estimate conservatively and note how you inferred it in the justification.
7. **If there’s insufficient information, return "Unknown".

#### Calculation Rules:
- **If explicit duration given**: Use that exact duration
- **If mentioned in job role**: Calculate months/years between start and end dates of that position
- **If mentioned in multiple roles**: SUM the total duration across all roles
- **Overlapping periods**: Do NOT double-count overlapping timeframes
- **Current/ongoing roles**: Calculate up to present date (October 2025)
- **Education period**: 
  - Count academic projects ONLY if skill explicitly mentioned
  - Reduce weightage by 50% (2 years academic = 1 year professional equivalent)
- **Certifications**: Count from certification date to present if actively used
- **No clear timeline**: Mark as "0.5" (minimal/mentioned only) with justification

#### Date Calculation Examples:
- Role: Jan 2020 - Dec 2022, Skills: Python, SQL → 3 years each
- Role 1: Jan 2020-Dec 2021 (Python), Role 2: Jun 2022-Present (Python) → 3.8 years total (not overlapping)
- "Currently working with React since 2023" → Calculate from 2023 to Oct 2025 = 2.8 years

### 3. JUSTIFICATION REQUIREMENTS

Each skill MUST include:

#### Justification Components:

**a) Source Location**: Where in resume the skill was found
- "Mentioned in Technical Skills section"
- "Listed under Job Role: Software Engineer at XYZ Corp"
- "Referenced in Project: E-commerce Platform Development"

**b) Context**: How the skill was mentioned
- "Used for backend development"
- "Led team using this technology"
- "Certified in this skill"
- "Part of daily responsibilities"

**c) Experience Calculation Logic**: Show the math
- "Calculated from employment duration: Jan 2020 - Dec 2022 = 3 years"
- "Explicitly stated: '5 years of experience with AWS'"
- "Sum of two roles: 2 years (Role A) + 1.5 years (Role B) = 3.5 years"
- "Mentioned in skills section without timeline, no usage in job roles = 0.5 years (basic familiarity)"

### 4. EXTRACTION RULES

#### DO:
- Extract EVERY skill mentioned, even if listed once
- Include variations (e.g., "JavaScript" and "JS" as same skill)
- Normalize skill names (e.g., "React.js" → "React")
- Count partial years (e.g., 2.5 years, 1.8 years)
- Be conservative with experience calculation when ambiguous
- Include tools, technologies, methodologies, and certifications

#### DO NOT:
- Infer skills not explicitly mentioned
- Extract company names, job titles, or educational degrees as skills
- Guess experience if no timeline information exists (use "Unknown")
- Include generic responsibilities as skills unless they represent specific competencies
- Double-count overlapping time periods

### 5. OUTPUT FORMAT

Return a valid JSON array with the following structure. Each dictionary must contain exactly three keys: skill, years_of_experience, and justification.

Example output structure:

[
  {{
    "skill": "Python",
    "years_of_experience": 5.5,
    "justification": "Found in Technical Skills section and mentioned in 3 job roles: (1) Software Engineer at ABC Corp (Jan 2020 - Dec 2022): 3 years, (2) Senior Developer at XYZ Inc (Jan 2023 - Present): 2.8 years (Jan 2023 to Oct 2025). Total: 5.8 years rounded to 5.5 due to 3-month gap between roles. Used for backend API development and data processing."
  }},
  {{
    "skill": "React",
    "years_of_experience": 2.0,
    "justification": "Explicitly stated in Technical Skills section as 'React (2 years)'. Also mentioned in current role at XYZ Inc where used for frontend development of customer portal since Jan 2023."
  }},
  {{
    "skill": "Agile Methodology",
    "years_of_experience": 4.0,
    "justification": "Mentioned across multiple roles: Software Engineer at ABC Corp (Jan 2020 - Dec 2022): 3 years working in Agile sprints, and current role at XYZ Inc (Jan 2023 - Present): 1 year as Scrum team member. Total: 4 years."
  }},
  {{
    "skill": "AWS Certified Solutions Architect",
    "years_of_experience": 1.5,
    "justification": "Certification obtained in April 2024 as listed in Certifications section. Currently utilizing AWS in present role at XYZ Inc since certification date. Calculated from Apr 2024 to Oct 2025 = 1.5 years."
  }},
  {{
    "skill": "Machine Learning",
    "years_of_experience": "Unknown",
    "justification": "Listed in Technical Skills section but no specific project or role mentions its usage. No timeline provided. Assigned minimum experience of 0.5 years indicating basic familiarity or theoretical knowledge."
  }}
]

### 6. EDGE CASES HANDLING

- **Skill mentioned without any dates**: Assign "Unknown" with justification
- **"Familiar with" or "Basic knowledge"**: Assign "Unknown"
- **"Expert" or "Advanced"**: Use timeline calculation, note proficiency in justification
- **Certifications without usage**: Count from certification date only
- **Academic projects**: Weight at 50% of actual time spent
- **Freelance/Contract work**: Count full duration if skill explicitly mentioned
- **Career breaks**: Do NOT count gap periods
- **Similar skills**: Treat as separate unless clearly identical (React vs React Native - separate)

### 7. QUALITY CHECKS

Before finalizing output, verify:
- Every entry has detailed justification with source reference
- Experience calculations are mathematically accurate
- No duplicates (skills are normalized)
- JSON format is valid and parseable
- All calculations account for current date: October 2025

## RESPONSE PROTOCOL
1. Analyze the entire resume systematically
2. Extract ALL skills meeting the criteria
3. Calculate experience using the methodology above
4. Provide detailed justification for each entry
5. Return ONLY the JSON array, no additional commentary

## CRITICAL REMINDERS
- Be EXHAUSTIVE - extract every skill mentioned
- Be PRECISE - show your calculation work
- Be CONSERVATIVE - when in doubt, use lower estimates with clear justification
- Be CONSISTENT - apply the same rules to all skills
- Current date for calculation purposes: October 2025

---

## INPUT RESUME
{resume_doc}"""



def extracted_skill_validator(resume_doc,extracted_skills_json):
    return f"""
## ROLE AND EXPERTISE
You are an expert Skills Validation Specialist and Quality Assurance Auditor with 15+ years of experience in resume analysis, data verification, and skills assessment accuracy. Your role is to validate extracted skills against the original resume to ensure accuracy, completeness, and proper justification.

## TASK OBJECTIVE
Validate the extracted skills JSON against the original resume. Verify each skill's presence, experience calculation accuracy, and justification quality. Return a corrected and validated JSON with the same structure, ensuring all entries are accurate and properly justified.

## VALIDATION PROCESS

### PHASE 1: PRESENCE VERIFICATION

For each skill in the extracted JSON:

#### Check 1: Skill Exists in Resume
- **Verify**: Is the skill explicitly mentioned in the resume?
- **Action**: If NOT found, REMOVE the skill entirely
- **Flag**: Skills that appear to be inferred or assumed

#### Check 2: Skill Name Accuracy
- **Verify**: Is the skill name correctly extracted and normalized?
- **Action**: Correct any misspellings or incorrect normalizations
- **Examples**: 
  - "React.js" and "ReactJS" → Normalize to "React"
  - "AWS Lambda" mentioned but extracted as just "AWS" → Keep specific "AWS Lambda"

#### Check 3: Duplicate Detection
- **Verify**: Are there duplicate skills with different names?
- **Action**: Merge duplicates, sum non-overlapping experience
- **Examples**:
  - "JavaScript" and "JS" → Merge into "JavaScript"
  - "Machine Learning" and "ML" → Merge into "Machine Learning"

### PHASE 2: EXPERIENCE CALCULATION VALIDATION

#### Validation Rule 1: Explicit Duration Statements
- **Priority**: HIGHEST - Explicit statements override all calculations
- **Check**: If resume states "5 years of Python", JSON must show 5.0 years exactly
- **Action**: Correct to match explicit statement

#### Validation Rule 2: Job Timeline Calculations
- **Verify**: Date calculations are mathematically correct
- **Formula**: (End Date - Start Date) in years, accounting for months
- **Current Date**: Use October 2025 for ongoing roles
- **Precision**: Round to 1 decimal place (e.g., 2.8 years)

**Calculation Examples**:
- Job: Jan 2020 - Dec 2022 = 3.0 years
- Job: Mar 2021 - Aug 2023 = 2.4 years (29 months)
- Job: Jun 2023 - Oct 2025 = 2.3 years (28 months)
- Job: Jan 2020 - Present (Oct 2025) = 5.8 years (69 months)

#### Validation Rule 3: Multiple Role Aggregation
- **Check**: Sum experience across multiple roles correctly
- **Critical**: NO double-counting of overlapping periods
- **Action**: Identify overlaps and count shared time only once

**Overlap Detection Example**:

WRONG CALCULATION:
- Role A: Jan 2020 - Dec 2022 (Python) = 3.0 years
- Role B: Jun 2022 - Oct 2025 (Python) = 3.3 years
- Total claimed: 6.3 years (INCORRECT - double-counted Jun-Dec 2022)

CORRECT CALCULATION:
- Role A: Jan 2020 - May 2022 = 2.4 years
- Overlap: Jun 2022 - Dec 2022 = 0.6 years (count once)
- Role B: Jan 2023 - Oct 2025 = 2.8 years
- Total: 5.8 years

#### Validation Rule 4: Minimum Experience Assignment
- **"Unknown"**: Skill listed but zero context or timeline
- **0.5 years**: "Familiar with", "basic knowledge", or single mention without usage
- **Action**: Verify assignment matches resume context

#### Validation Rule 5: Academic/Certification Experience
- **Academic**: Apply 50% weight (2 years academic = 1 year professional)
- **Certifications**: Count from cert date ONLY if actively used in roles
- **Action**: Verify correct weightage applied

### PHASE 3: JUSTIFICATION QUALITY AUDIT

Each justification MUST contain:

1. **Source Location**: Exact section/role where skill appears
2. **Context**: How skill was used or applied
3. **Calculation**: Complete mathematical breakdown
4. **Multiple Sources**: All occurrences referenced if applicable

**POOR JUSTIFICATION (Reject)**:
- "Found in resume"
- "3 years experience"
- "Mentioned in job role"
- "Used for development"

**GOOD JUSTIFICATION (Accept)**:
- "Found in Technical Skills section and mentioned in Software Engineer role at ABC Corp (Jan 2020 - Dec 2022): 3 years. Used for backend API development with Django framework."
- "Explicitly stated in Technical Skills section as 'Python (5 years)'. Also mentioned in E-commerce Platform project description."
- "Mentioned across multiple roles: Software Engineer at ABC Corp (Jan 2020 - Dec 2022): 3 years working in Agile sprints, and current role at XYZ Inc (Jan 2023 - Present): 1.8 years as Scrum team member. Total: 4.8 years."

### PHASE 4: COMPLETENESS CHECK

Scan the original resume for missing skills:

**Check These Sections**:
- Technical Skills / Core Competencies
- Job responsibilities and bullet points
- Project descriptions
- Certifications and training
- Tools mentioned in achievements
- Methodologies explicitly stated

**Action**: Add missing skills with proper calculation and justification

### PHASE 5: FALSE POSITIVE ELIMINATION

Remove these if extracted as skills:

- Job titles (Software Engineer, Project Manager)
- Company names (Google, Microsoft) unless specific tech (Google Cloud Platform)
- Educational degrees (Bachelor's in CS, MBA)
- Generic phrases (worked on projects, collaborated with team)
- Inferred soft skills (leadership inferred from "led team" without explicit mention)
- Industry names (Healthcare, Finance) unless domain expertise explicitly stated

### PHASE 6: EDGE CASE VALIDATION

#### Career Gaps
- **Rule**: Gap periods are NOT counted
- **Example**: Role ends Dec 2020, next starts Jun 2021 → 6-month gap excluded

#### Concurrent Roles
- **Rule**: Overlapping time counted once per skill
- **Example**: Two simultaneous jobs using Python → count overlapping months once

#### Skill Variations
- **Keep Separate**: React vs React Native, Java vs JavaScript, SQL vs MySQL
- **Merge**: JavaScript vs JS, React.js vs React, ML vs Machine Learning

#### Proficiency Levels
- **Rule**: Note in justification but don't alter calculation
- **Example**: "Expert in Python" → include "Proficiency level: Expert" in justification

## OUTPUT FORMAT

Return a valid JSON array with the following structure. Each dictionary must contain exactly three keys: skill, years_of_experience, and justification.

**CRITICAL**: Use double curly braces `{{` and `}}` for JSON objects to ensure proper formatting.

Example output structure:
```json
[
  {{
    "skill": "Python",
    "years_of_experience": 5.5,
    "justification": "Found in Technical Skills section and mentioned in 3 job roles: (1) Software Engineer at ABC Corp (Jan 2020 - Dec 2022): 3 years, (2) Senior Developer at XYZ Inc (Jan 2023 - Present): 2.8 years (Jan 2023 to Oct 2025). Total: 5.8 years rounded to 5.5 due to 3-month gap between roles. Used for backend API development and data processing."
  }},
  {{
    "skill": "React",
    "years_of_experience": 2.0,
    "justification": "Explicitly stated in Technical Skills section as 'React (2 years)'. Also mentioned in current role at XYZ Inc where used for frontend development of customer portal since Jan 2023."
  }},
  {{
    "skill": "Agile Methodology",
    "years_of_experience": 4.0,
    "justification": "Mentioned across multiple roles: Software Engineer at ABC Corp (Jan 2020 - Dec 2022): 3 years working in Agile sprints, and current role at XYZ Inc (Jan 2023 - Present): 1 year as Scrum team member. Total: 4 years."
  }},
  {{
    "skill": "AWS Certified Solutions Architect",
    "years_of_experience": 1.5,
    "justification": "Certification obtained in April 2024 as listed in Certifications section. Currently utilizing AWS in present role at XYZ Inc since certification date. Calculated from Apr 2024 to Oct 2025 = 1.5 years."
  }},
  {{
    "skill": "Docker",
    "years_of_experience": "Unknown",
    "justification": "Listed in Technical Skills section but no specific project or role mentions its usage. No timeline provided. Indicates basic familiarity or theoretical knowledge."
  }}
]


---


VALIDATION CORRECTIONS APPLIED:
1. REMOVED: "Software Engineer" - Job title, not a skill
2. CORRECTED: Python experience 6.5 → 5.5 years - Removed 1-year overlap between roles (Jun 2022 - Jun 2023)
3. ADDED: "Docker" - Found in Technical Skills section but missing from extraction
4. MERGED: "JavaScript" and "JS" into single "JavaScript" entry, combined experience: 4.2 years
5. UPDATED: "Machine Learning" from 0.5 → "Unknown" - Listed in skills but no usage context in roles or projects
6. CORRECTED: AWS calculation error - Jan 2021 to Oct 2025 = 4.8 years (was incorrectly shown as 5.0)
7. ENHANCED: React justification - Added specific project reference "Customer Portal" from resume
8. CORRECTED: Agile Methodology - Fixed double-counting overlap, adjusted from 5.0 to 4.0 years


CRITICAL VALIDATION RULES
1. Source of Truth: Original resume is ALWAYS correct; JSON may contain errors
2. Mathematical Precision: Verify all date calculations with calculator
3. Conservative Approach: When ambiguous, use lower estimate with clear reasoning
4. Completeness Priority: Actively search for missing skills, don't just validate existing
5. Quality over Quantity: 20 accurate skills > 30 questionable ones
6. Explicit > Calculated: Explicit duration statements override timeline calculations
7. Zero Tolerance: Remove any skill not explicitly in resume
8. Format Consistency: Use double curly braces {{}} in JSON output

RESPONSE PROTOCOL
1. Read original resume thoroughly
2. Validate each extracted skill against resume
3. Identify and add missing skills from resume
4. Correct all calculation errors
5. Remove false positives
6. Return: Validated JSON array + Corrections Report


INPUT DATA
ORIGINAL RESUME:
{resume_doc}
EXTRACTED SKILLS JSON:
{extracted_skills_json}"""