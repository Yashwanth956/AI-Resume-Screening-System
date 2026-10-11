# =========================================================

# app.py

# AI RESUME SCREENING & JOB RECOMMENDATION SYSTEM

# =========================================================



from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)



import os

import re

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)



import pdfplumber



from werkzeug.utils import secure_filename





# =========================================================

# OPTIONAL PYMUPDF IMPORT

# =========================================================



try:

    import fitz

except ImportError:

    fitz = None





# =========================================================

# RESUME PARSER IMPORTS

# =========================================================



from resume_parser.parser import (

    extract_email,

    extract_phone

)



from resume_parser.skills import (

    extract_skills

)



from resume_parser.name_extractor import (

    extract_name

)



from resume_parser.education import (

    extract_education

)



from resume_parser.section_parser import (

    extract_section

)





# =========================================================

# PROJECT PARSER

# =========================================================



try:



    from resume_parser.project import (

        extract_projects

    )



except ImportError as e:



    print(

        "Project parser import error:",

        e

    )



    extract_projects = None





# =========================================================

# EXPERIENCE

# =========================================================



from resume_parser.experience import (

    extract_experience

)





# =========================================================

# JOB DESCRIPTION SKILLS

# =========================================================



from resume_parser.jd_skill_extractor import (

    extract_jd_skills

)





# =========================================================

# ATS

# =========================================================



from resume_parser.ats_scorer import (

    calculate_ats_score

)





# =========================================================

# JOB ROLE RECOMMENDER

# =========================================================



from resume_parser.role_recommender import (

    recommend_job_roles

)



# =========================================================

# RESUME IMPROVEMENT SUGGESTIONS

# =========================================================



from resume_parser.suggestions import (

    generate_suggestions

)



# =========================================================

# JOB MATCHER

# =========================================================



from resume_parser.job_matcher import (

    analyze_job_match

)



# =========================================================

# DATABASE STORAGE

# =========================================================



from database.db_manager import (

    save_analysis,
    list_analyses,
    get_analysis,
    delete_analysis

)





# =========================================================

# FLASK APP

# =========================================================



app = Flask(__name__)





# =========================================================

# UPLOAD CONFIGURATION

# =========================================================



UPLOAD_FOLDER = "uploads"



app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER





os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)





# =========================================================

# PDFPLUMBER TEXT EXTRACTION

# =========================================================



def extract_text_pdfplumber(filepath):



    text_parts = []



    try:



        with pdfplumber.open(

            filepath

        ) as pdf:



            for page in pdf.pages:



                try:



                    page_text = (

                        page.extract_text()

                    )



                    if page_text:



                        text_parts.append(

                            page_text

                        )



                except Exception as page_error:



                    print(

                        "pdfplumber page error:",

                        page_error

                    )



    except Exception as e:



        print(

            "pdfplumber extraction error:",

            e

        )



        return ""



    return "\n".join(

        text_parts

    ).strip()





def extract_text_pymupdf(filepath):



    if fitz is None:



        print(

            "PyMuPDF is not installed."

        )



        return ""



    document = None



    page_texts = []



    try:



        document = fitz.open(

            filepath

        )



        for page_number, page in enumerate(

            document,

            start=1

        ):



            try:



                # ==========================================

                # IMPORTANT

                #

                # Do NOT use:

                #

                # page.get_text("text")

                #

                # Some resumes are multi-column / positioned

                # PDFs, so PyMuPDF may return text in the

                # wrong logical order.

                #

                # Instead get blocks and sort them by their

                # position on the page.

                # ==========================================



                blocks = page.get_text(

                    "blocks"

                )



                if not blocks:

                    continue



                # block:

                #

                # (

                #   x0,

                #   y0,

                #   x1,

                #   y1,

                #   text,

                #   block_no,

                #   block_type

                # )

                #

                # Sort primarily from top -> bottom,

                # then left -> right.



                blocks = sorted(

                    blocks,

                    key=lambda block: (

                        round(

                            block[1],

                            1

                        ),

                        block[0]

                    )

                )



                page_parts = []



                for block in blocks:



                    if len(block) < 5:

                        continue



                    block_text = block[4]



                    if not block_text:

                        continue



                    block_text = str(

                        block_text

                    ).strip()



                    if not block_text:

                        continue



                    page_parts.append(

                        block_text

                    )



                page_text = "\n".join(

                    page_parts

                )



                if page_text:



                    page_texts.append(

                        page_text

                    )



            except Exception as page_error:



                print(

                    f"PyMuPDF page {page_number} error:",

                    page_error

                )



    except Exception as e:



        print(

            "PyMuPDF extraction error:",

            e

        )



        return ""



    finally:



        if document is not None:



            try:



                document.close()



            except Exception:



                pass



    final_text = "\n".join(

        page_texts

    )



    # ==========================================

    # BASIC CLEANUP

    # ==========================================



    final_text = final_text.replace(

        "\r\n",

        "\n"

    )



    final_text = final_text.replace(

        "\r",

        "\n"

    )



    final_text = re.sub(

        r"[ \t]+",

        " ",

        final_text

    )



    final_text = re.sub(

        r"\n{3,}",

        "\n\n",

        final_text

    )



    return final_text.strip()





# =========================================================

# NORMALIZE PROJECT

# =========================================================



def normalize_project(project):



    # =====================================================

    # CHECK PROJECT TYPE

    # =====================================================



    if not isinstance(

        project,

        dict

    ):

        return None





    # =====================================================

    # TITLE

    # =====================================================



    title = (

        project.get("title")

        or project.get("name")

        or ""

    )



    title = str(

        title

    ).strip()



    if not title:

        return None





    # =====================================================

    # REJECT OBVIOUS NON-PROJECT TITLES

    # =====================================================



    title_lower = title.lower()



    non_project_title_patterns = (

        "university",

        "college",

        "high school",

        "school",

        "board of intermediate",

        "board of secondary",

        "intermediate education",

        "secondary education",

        "bachelor of technology",

        "b.tech",

        "cgpa",

        "percentage",

    )



    if any(

        pattern in title_lower

        for pattern in non_project_title_patterns

    ):

        return None





    # =====================================================

    # REJECT SENTENCE FRAGMENTS

    # =====================================================



    if title.endswith(

        (

            ".",

            ",",

            ";",

            "!",

            "?",

        )

    ):

        return None





    # =====================================================

    # TECHNOLOGIES

    # =====================================================



    technologies = project.get(

        "technologies",

        []

    )



    if technologies is None:

        technologies = []



    if isinstance(

        technologies,

        str

    ):

        technologies = [

            technologies

        ]



    clean_technologies = []



    seen_technologies = set()



    for technology in technologies:



        if technology is None:

            continue



        value = str(

            technology

        ).strip()



        if not value:

            continue



        # GitHub is a link/tool,

        # not a project technology.

        if value.lower() == "github":

            continue



        key = value.lower()



        if key not in seen_technologies:



            seen_technologies.add(

                key

            )



            clean_technologies.append(

                value

            )





    # =====================================================

    # DESCRIPTIONS

    # =====================================================



    descriptions = project.get(

        "description",

        []

    )



    if descriptions is None:

        descriptions = []



    # Prevent character-by-character output

    # when description is a string.

    if isinstance(

        descriptions,

        str

    ):

        descriptions = [

            descriptions

        ]



    clean_descriptions = []



    seen_descriptions = set()



    for description in descriptions:



        if description is None:

            continue



        value = str(

            description

        ).strip()



        value = re.sub(

            r"\s+",

            " ",

            value

        )



        if not value:

            continue



        key = value.lower()



        if key not in seen_descriptions:



            seen_descriptions.add(

                key

            )



            clean_descriptions.append(

                value

            )





    # =====================================================

    # RETURN CLEAN PROJECT

    # =====================================================



    return {

        "title": title,

        "technologies": clean_technologies,

        "description": clean_descriptions

    }



    # -----------------------------------------------------

    # Title

    # -----------------------------------------------------



    title = (

        project.get("title")

        or project.get("name")

        or ""

    )



    title = str(

        title

    ).strip()



    if not title:



        return None



    # -----------------------------------------------------

    # Technologies

    # -----------------------------------------------------



    technologies = project.get(

        "technologies",

        []

    )



    if technologies is None:



        technologies = []



    if isinstance(

        technologies,

        str

    ):



        technologies = [

            technologies

        ]



    clean_technologies = []



    seen_technologies = set()



    for technology in technologies:



        if technology is None:

            continue



        value = str(

            technology

        ).strip()



        if not value:

            continue



        # GitHub is a link/tool, not normally

        # useful as a project technology.

        if value.lower() == "github":

            continue



        key = value.lower()



        if key not in seen_technologies:



            seen_technologies.add(

                key

            )



            clean_technologies.append(

                value

            )



    # -----------------------------------------------------

    # Descriptions

    # -----------------------------------------------------



    descriptions = project.get(

        "description",

        []

    )



    if descriptions is None:



        descriptions = []



    # Very important:

    # prevent result.html from iterating over

    # individual characters of a string.

    if isinstance(

        descriptions,

        str

    ):



        descriptions = [

            descriptions

        ]



    clean_descriptions = []



    seen_descriptions = set()



    for description in descriptions:



        if description is None:

            continue



        value = str(

            description

        ).strip()



        value = re.sub(

            r"\s+",

            " ",

            value

        )



        if not value:

            continue



        key = value.lower()



        if key not in seen_descriptions:



            seen_descriptions.add(

                key

            )



            clean_descriptions.append(

                value

            )



    return {

        "title": title,

        "technologies": clean_technologies,

        "description": clean_descriptions

    }





# =========================================================

# NORMALIZE PROJECT LIST

# =========================================================



def normalize_projects(projects):



    if not projects:



        return []



    normalized_projects = []



    seen_titles = set()



    for project in projects:



        normalized = normalize_project(

            project

        )



        if not normalized:

            continue



        title = normalized[

            "title"

        ]



        title_key = re.sub(

            r"[^a-z0-9]+",

            " ",

            title.lower()

        ).strip()



        if not title_key:

            continue



        if title_key in seen_titles:

            continue



        seen_titles.add(

            title_key

        )



        normalized_projects.append(

            normalized

        )



    return normalized_projects





# =========================================================

# PROJECT RESULT QUALITY SCORE

# =========================================================



def calculate_project_quality(

    projects

):



    if not projects:



        return 0



    score = 0



    for project in projects:



        title = project.get(

            "title",

            ""

        )



        technologies = project.get(

            "technologies",

            []

        )



        descriptions = project.get(

            "description",

            []

        )



        # -------------------------------------------------

        # Project itself

        # -------------------------------------------------



        score += 100



        # -------------------------------------------------

        # Good title

        # -------------------------------------------------



        if title:



            score += 20



        # Penalize obvious sentence fragments

        # accidentally detected as project titles.

        if title.endswith(

            (

                ".",

                ",",

                ";",

            )

        ):



            score -= 80



        # -------------------------------------------------

        # Descriptions

        # -------------------------------------------------



        score += (

            len(descriptions)

            * 20

        )



        for description in descriptions:



            if len(

                description.split()

            ) >= 5:



                score += 5



        # -------------------------------------------------

        # Technologies

        # -------------------------------------------------



        score += (

            len(technologies)

            * 5

        )



    return score





# =========================================================

# SAFE PROJECT EXTRACTION

# =========================================================



def safely_extract_projects(

    source_text,

    source_name

):



    if not source_text:



        return []



    if extract_projects is None:



        return []



    try:



        print()

        print(

            "========================================"

        )



        print(

            f"PROJECT PARSER SOURCE: {source_name}"

        )



        print(

            "========================================"

        )



        result = extract_projects(

            source_text

        )



        result = normalize_projects(

            result

        )



        print(

            f"{source_name} detected:",

            len(result),

            "projects"

        )



        print(

            f"{source_name} quality:",

            calculate_project_quality(

                result

            )

        )



        return result



    except Exception as e:



        print(

            f"{source_name} project extraction error:",

            e

        )



        return []





# =========================================================

# SELECT BEST PROJECT EXTRACTION

# =========================================================



def extract_best_projects(

    pdfplumber_text,

    pymupdf_text

):



    # -----------------------------------------------------

    # PDFPLUMBER

    # -----------------------------------------------------



    pdfplumber_projects = (

        safely_extract_projects(

            pdfplumber_text,

            "PDFPLUMBER"

        )

    )



    # -----------------------------------------------------

    # PYMUPDF

    # -----------------------------------------------------



    pymupdf_projects = []



    if pymupdf_text:



        pymupdf_projects = (

            safely_extract_projects(

                pymupdf_text,

                "PYMUPDF"

            )

        )



    # -----------------------------------------------------

    # Quality

    # -----------------------------------------------------



    pdfplumber_quality = (

        calculate_project_quality(

            pdfplumber_projects

        )

    )



    pymupdf_quality = (

        calculate_project_quality(

            pymupdf_projects

        )

    )



    print()

    print(

        "========== PROJECT SOURCE COMPARISON =========="

    )



    print(

        "PDFPlumber:",

        len(pdfplumber_projects),

        "projects | quality =",

        pdfplumber_quality

    )



    print(

        "PyMuPDF:",

        len(pymupdf_projects),

        "projects | quality =",

        pymupdf_quality

    )



    # -----------------------------------------------------

    # Choose best extraction.

    # -----------------------------------------------------



    if (

        pymupdf_projects

        and

        pymupdf_quality

        > pdfplumber_quality

    ):



        print(

            "Selected project source: PyMuPDF"

        )



        print(

            "==============================================="

        )



        return (

            pymupdf_projects,

            "PyMuPDF"

        )



    print(

        "Selected project source: PDFPlumber"

    )



    print(

        "==============================================="

    )



    return (

        pdfplumber_projects,

        "PDFPlumber"

    )





# =========================================================

# HOME

# =========================================================



@app.route("/")

def home():



    return render_template(

        "1_index.html"

    )





# =========================================================

# DASHBOARD

# =========================================================



@app.route("/dashboard")
def dashboard():



    try:



        analyses = list_analyses(
            limit=1000
        )



    except Exception as e:



        print(
            "Dashboard loading error:",
            e
        )



        analyses = []



    def safe_float(
        value
    ):



        try:



            return float(
                value or 0
            )



        except (
            TypeError,
            ValueError
        ):



            return 0.0



    total_analyses = len(
        analyses
    )



    ats_scores = [

        safe_float(
            analysis.get(
                "ats_score"
            )
        )

        for analysis in analyses

    ]



    job_match_scores = [

        safe_float(
            analysis.get(
                "job_match_score"
            )
        )

        for analysis in analyses

    ]



    if total_analyses > 0:



        average_ats = round(

            sum(
                ats_scores
            )
            / total_analyses,

            2

        )



        average_job_match = round(

            sum(
                job_match_scores
            )
            / total_analyses,

            2

        )



        highest_ats = round(
            max(
                ats_scores
            ),
            2
        )



        highest_job_match = round(
            max(
                job_match_scores
            ),
            2
        )



    else:



        average_ats = 0.0

        average_job_match = 0.0

        highest_ats = 0.0

        highest_job_match = 0.0



    category_counts = {}



    for analysis in analyses:



        category = (

            analysis.get(
                "match_category"
            )

            or "Uncategorized"

        )



        category = str(
            category
        ).strip()



        if not category:



            category = (
                "Uncategorized"
            )



        category_counts[
            category
        ] = (

            category_counts.get(
                category,
                0
            )

            + 1

        )



    category_stats = []



    for (
        category,
        count
    ) in sorted(

        category_counts.items(),

        key=lambda item: (
            -item[1],
            item[0]
        )

    ):



        if total_analyses > 0:



            percentage = round(

                (
                    count
                    / total_analyses
                )
                * 100,

                2

            )



        else:



            percentage = 0.0



        category_stats.append({

            "category": category,

            "count": count,

            "percentage": percentage

        })



    recent_analyses = (
        analyses[:10]
    )



    return render_template(

        "5_dashboard.html",

        total_analyses=total_analyses,

        average_ats=average_ats,

        average_job_match=average_job_match,

        highest_ats=highest_ats,

        highest_job_match=highest_job_match,

        category_stats=category_stats,

        recent_analyses=recent_analyses

    )





# =========================================================

# ANALYSIS HISTORY

# =========================================================



@app.route("/history")
def history():



    try:



        analyses = list_analyses(

            limit=100

        )



    except Exception as e:



        print(

            "History loading error:",

            e

        )



        analyses = []



    return render_template(

        "3_history.html",

        analyses=analyses

    )





# =========================================================

# SAVED ANALYSIS DETAIL

# =========================================================



@app.route("/analysis/<int:analysis_id>")
def analysis_detail(

    analysis_id

):



    try:



        analysis = get_analysis(

            analysis_id

        )



    except Exception as e:



        print(

            "Analysis loading error:",

            e

        )



        analysis = None



    if analysis is None:



        return (

            "Analysis not found.",

            404

        )



    # =====================================================
    # SAVED ANALYSIS IMPROVEMENT SUGGESTIONS
    # =====================================================



    saved_experience = {

        "total_years":
            analysis.get(
                "total_experience",
                0
            ),

        "stated_years":
            analysis.get(
                "stated_experience",
                0
            ),

        "calculated_years":
            analysis.get(
                "calculated_experience",
                0
            )

    }



    saved_ats_result = {

        "skill_score":
            analysis.get(
                "skill_score"
            ),

        "keyword_score":
            analysis.get(
                "keyword_score"
            ),

        "experience_score":
            analysis.get(
                "experience_score"
            ),

        "education_score":
            analysis.get(
                "education_score"
            ),

        "project_score":
            analysis.get(
                "project_score"
            ),

        "resume_quality_score":
            analysis.get(
                "resume_quality_score"
            )

    }



    try:



        suggestions = generate_suggestions(

            ats_score=analysis.get(
                "ats_score",
                0
            ),

            missing_skills=analysis.get(
                "missing_skills",
                []
            ),

            projects=analysis.get(
                "projects",
                []
            ),

            experience=saved_experience,

            ats_result=saved_ats_result,

            recommended_roles=analysis.get(
                "recommended_roles",
                []
            ),

            job_skills=analysis.get(
                "job_skills",
                []
            )

        )



    except Exception as e:



        print(

            "Saved suggestion generation error:",

            e

        )



        suggestions = []



    return render_template(

        "4_analysis_detail.html",

        analysis=analysis,

        suggestions=suggestions

    )





# =========================================================

# DOWNLOAD ANALYSIS PDF REPORT

# =========================================================



@app.route("/analysis/<int:analysis_id>/pdf")
def download_analysis_pdf(
    analysis_id
):



    try:



        analysis = get_analysis(
            analysis_id
        )



    except Exception as e:



        print(
            "PDF analysis loading error:",
            e
        )



        analysis = None



    if analysis is None:



        return (
            "Analysis not found.",
            404
        )



    # =====================================================
    # PDF IMPROVEMENT SUGGESTIONS
    # =====================================================



    pdf_experience = {

        "total_years":
            analysis.get(
                "total_experience",
                0
            ),

        "stated_years":
            analysis.get(
                "stated_experience",
                0
            ),

        "calculated_years":
            analysis.get(
                "calculated_experience",
                0
            )

    }



    pdf_ats_result = {

        "skill_score":
            analysis.get(
                "skill_score"
            ),

        "keyword_score":
            analysis.get(
                "keyword_score"
            ),

        "experience_score":
            analysis.get(
                "experience_score"
            ),

        "education_score":
            analysis.get(
                "education_score"
            ),

        "project_score":
            analysis.get(
                "project_score"
            ),

        "resume_quality_score":
            analysis.get(
                "resume_quality_score"
            )

    }



    try:



        pdf_suggestions = generate_suggestions(

            ats_score=analysis.get(
                "ats_score",
                0
            ),

            missing_skills=analysis.get(
                "missing_skills",
                []
            ),

            projects=analysis.get(
                "projects",
                []
            ),

            experience=pdf_experience,

            ats_result=pdf_ats_result,

            recommended_roles=analysis.get(
                "recommended_roles",
                []
            ),

            job_skills=analysis.get(
                "job_skills",
                []
            )

        )



    except Exception as e:



        print(

            "PDF suggestion generation error:",

            e

        )



        pdf_suggestions = []



    def safe_text(
        value,
        default="-"
    ):



        if value is None:



            return default



        value = str(
            value
        ).strip()



        if not value:



            return default



        return value



    def paragraph_text(
        value
    ):



        return escape(
            safe_text(
                value
            )
        )



    def format_list(
        values
    ):



        if not values:



            return "-"



        if isinstance(
            values,
            str
        ):



            return values



        if isinstance(
            values,
            (
                list,
                tuple,
                set
            )
        ):



            cleaned = [

                safe_text(
                    item,
                    ""
                )

                for item in values

                if safe_text(
                    item,
                    ""
                )

            ]



            return ", ".join(
                cleaned
            ) if cleaned else "-"



        return safe_text(
            values
        )



    buffer = BytesIO()



    doc = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,

        title="Resume Analysis Report",

        author="AI Resume Screening & Job Recommendation System"

    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontName="Helvetica-Bold",

        fontSize=20,

        leading=24,

        spaceAfter=12

    )



    section_style = ParagraphStyle(

        "SectionHeading",

        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=13,

        leading=16,

        spaceBefore=10,

        spaceAfter=7

    )



    normal_style = ParagraphStyle(

        "ReportNormal",

        parent=styles["BodyText"],

        fontName="Helvetica",

        fontSize=9.5,

        leading=13

    )



    small_style = ParagraphStyle(

        "SmallText",

        parent=normal_style,

        fontSize=8.5,

        leading=11

    )



    story = []



    def add_section_title(
        title
    ):



        story.append(
            Paragraph(
                escape(
                    title
                ),
                section_style
            )
        )



    def make_table(
        rows,
        widths=None
    ):



        prepared_rows = []



        for row in rows:



            prepared_rows.append([

                Paragraph(
                    paragraph_text(
                        cell
                    ),
                    small_style
                )

                for cell in row

            ])



        table = Table(

            prepared_rows,

            colWidths=widths,

            repeatRows=1

        )



        table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#E9EEF5"
                    )
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        "#BFC7D1"
                    )
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])

        )



        return table



    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------



    story.append(

        Paragraph(
            "AI Resume Screening &amp; Job Recommendation System",
            title_style
        )

    )



    story.append(

        Paragraph(
            "Resume Analysis Report",
            styles["Heading2"]
        )

    )



    story.append(
        Spacer(
            1,
            6
        )
    )



    # ---------------------------------------------------------
    # CANDIDATE DETAILS
    # ---------------------------------------------------------



    add_section_title(
        "Candidate Details"
    )



    candidate_rows = [

        [
            "Field",
            "Value"
        ],

        [
            "Analysis ID",
            analysis.get(
                "id",
                analysis_id
            )
        ],

        [
            "Candidate Name",
            analysis.get(
                "candidate_name"
            )
        ],

        [
            "Email",
            analysis.get(
                "email"
            )
        ],

        [
            "Phone",
            analysis.get(
                "phone"
            )
        ],

        [
            "Resume File",
            analysis.get(
                "resume_filename"
            )
        ],

        [
            "Created At",
            analysis.get(
                "created_at"
            )
        ]

    ]



    story.append(

        make_table(
            candidate_rows,
            widths=[
                48 * mm,
                128 * mm
            ]
        )

    )



    story.append(
        Spacer(
            1,
            9
        )
    )



    # ---------------------------------------------------------
    # SCORES
    # ---------------------------------------------------------



    add_section_title(
        "ATS and Job Match Summary"
    )



    score_rows = [

        [
            "Metric",
            "Score"
        ],

        [
            "ATS Score",
            f"{safe_text(analysis.get('ats_score'), '0')}%"
        ],

        [
            "Job Match",
            f"{safe_text(analysis.get('job_match_score'), '0')}%"
        ],

        [
            "Match Category",
            analysis.get(
                "match_category"
            )
        ],

        [
            "Skill Score",
            f"{safe_text(analysis.get('skill_score'), '0')}%"
        ],

        [
            "Keyword Score",
            f"{safe_text(analysis.get('keyword_score'), '0')}%"
        ],

        [
            "Experience Score",
            f"{safe_text(analysis.get('experience_score'), '0')}%"
        ],

        [
            "Education Score",
            f"{safe_text(analysis.get('education_score'), '0')}%"
        ],

        [
            "Project Score",
            f"{safe_text(analysis.get('project_score'), '0')}%"
        ],

        [
            "Resume Quality Score",
            f"{safe_text(analysis.get('resume_quality_score'), '0')}%"
        ]

    ]



    story.append(

        make_table(
            score_rows,
            widths=[
                80 * mm,
                96 * mm
            ]
        )

    )



    # ---------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------



    add_section_title(
        "Experience Summary"
    )



    experience_summary_rows = [

        [
            "Metric",
            "Value"
        ],

        [
            "Total Experience",
            f"{safe_text(analysis.get('total_experience'), '0')} years"
        ],

        [
            "Stated Experience",
            f"{safe_text(analysis.get('stated_experience'), '0')} years"
        ],

        [
            "Calculated Experience",
            f"{safe_text(analysis.get('calculated_experience'), '0')} years"
        ]

    ]



    story.append(

        make_table(
            experience_summary_rows,
            widths=[
                80 * mm,
                96 * mm
            ]
        )

    )



    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------



    add_section_title(
        "Skills"
    )



    skill_rows = [

        [
            "Category",
            "Skills"
        ],

        [
            "Resume Skills",
            format_list(
                analysis.get(
                    "resume_skills"
                )
            )
        ],

        [
            "Job Required Skills",
            format_list(
                analysis.get(
                    "job_skills"
                )
            )
        ],

        [
            "Matching Skills",
            format_list(
                analysis.get(
                    "matching_skills"
                )
            )
        ],

        [
            "Missing Skills",
            format_list(
                analysis.get(
                    "missing_skills"
                )
            )
        ]

    ]



    story.append(

        make_table(
            skill_rows,
            widths=[
                50 * mm,
                126 * mm
            ]
        )

    )



    # ---------------------------------------------------------
    # EDUCATION
    # ---------------------------------------------------------



    education = (
        analysis.get(
            "education"
        )
        or []
    )



    if education:



        add_section_title(
            "Education"
        )



        education_rows = [[
            "Degree",
            "Institution",
            "Score",
            "Duration"
        ]]



        for item in education:



            if isinstance(
                item,
                dict
            ):



                education_rows.append([

                    item.get(
                        "degree"
                    ),

                    item.get(
                        "institution"
                    ),

                    item.get(
                        "score"
                    ),

                    item.get(
                        "duration"
                    )

                ])



            else:



                education_rows.append([

                    item,
                    "-",
                    "-",
                    "-"

                ])



        story.append(

            make_table(
                education_rows,
                widths=[
                    46 * mm,
                    68 * mm,
                    26 * mm,
                    36 * mm
                ]
            )

        )



    # ---------------------------------------------------------
    # EXPERIENCE RECORDS
    # ---------------------------------------------------------



    experience_records = (
        analysis.get(
            "experience_records"
        )
        or []
    )



    if experience_records:



        add_section_title(
            "Work Experience"
        )



        experience_rows = [[
            "Role",
            "Company",
            "Duration / Date Range"
        ]]



        for item in experience_records:



            if isinstance(
                item,
                dict
            ):



                role = (

                    item.get(
                        "job_title"
                    )

                    or item.get(
                        "title"
                    )

                    or item.get(
                        "role"
                    )

                    or "-"

                )



                company = (

                    item.get(
                        "company"
                    )

                    or item.get(
                        "organization"
                    )

                    or "-"

                )



                duration = (

                    item.get(
                        "date_range"
                    )

                    or item.get(
                        "duration"
                    )

                    or "-"

                )



                experience_rows.append([

                    role,
                    company,
                    duration

                ])



            else:



                experience_rows.append([

                    item,
                    "-",
                    "-"

                ])



        story.append(

            make_table(
                experience_rows,
                widths=[
                    60 * mm,
                    60 * mm,
                    56 * mm
                ]
            )

        )



    # ---------------------------------------------------------
    # PROJECTS
    # ---------------------------------------------------------



    projects = (
        analysis.get(
            "projects"
        )
        or []
    )



    if projects:



        add_section_title(
            "Projects"
        )



        project_rows = [[
            "Project",
            "Technologies",
            "Description"
        ]]



        for item in projects:



            if isinstance(
                item,
                dict
            ):



                description = item.get(
                    "description"
                )



                if isinstance(
                    description,
                    (
                        list,
                        tuple
                    )
                ):



                    description = " ".join(
                        safe_text(
                            part,
                            ""
                        )

                        for part in description
                    )



                project_rows.append([

                    item.get(
                        "title"
                    ),

                    format_list(
                        item.get(
                            "technologies"
                        )
                    ),

                    description

                ])



            else:



                project_rows.append([

                    item,
                    "-",
                    "-"

                ])



        story.append(

            make_table(
                project_rows,
                widths=[
                    50 * mm,
                    52 * mm,
                    74 * mm
                ]
            )

        )



    # ---------------------------------------------------------
    # RECOMMENDED ROLES
    # ---------------------------------------------------------



    recommendations = (
        analysis.get(
            "recommended_roles"
        )
        or []
    )



    if recommendations:



        add_section_title(
            "Recommended Job Roles"
        )



        recommendation_rows = [[
            "Role",
            "Match Score",
            "Matched Skills",
            "Missing Skills"
        ]]



        for item in recommendations:



            if isinstance(
                item,
                dict
            ):



                role = (

                    item.get(
                        "role"
                    )

                    or item.get(
                        "job_role"
                    )

                    or item.get(
                        "title"
                    )

                    or "-"

                )



                match_score = (

                    item.get(
                        "match_score"
                    )

                    if item.get(
                        "match_score"
                    ) is not None

                    else item.get(
                        "score"
                    )

                )



                if match_score is None:



                    match_score = "-"



                else:



                    match_score = (
                        f"{match_score}%"
                    )



                recommendation_rows.append([

                    role,

                    match_score,

                    format_list(
                        item.get(
                            "matched_skills"
                        )
                    ),

                    format_list(
                        item.get(
                            "missing_skills"
                        )
                    )

                ])



            else:



                recommendation_rows.append([

                    item,
                    "-",
                    "-",
                    "-"

                ])



        story.append(

            make_table(
                recommendation_rows,
                widths=[
                    45 * mm,
                    30 * mm,
                    50 * mm,
                    51 * mm
                ]
            )

        )



    # ---------------------------------------------------------
    # RESUME IMPROVEMENT SUGGESTIONS
    # ---------------------------------------------------------



    if pdf_suggestions:



        add_section_title(
            "Resume Improvement Suggestions"
        )



        for suggestion in pdf_suggestions:



            story.append(

                Paragraph(

                    "&#8226; "
                    + escape(
                        str(
                            suggestion
                        )
                    ),

                    normal_style

                )

            )



            story.append(
                Spacer(
                    1,
                    4
                )
            )



    # ---------------------------------------------------------
    # JOB DESCRIPTION
    # ---------------------------------------------------------



    job_description = safe_text(

        analysis.get(
            "job_description"
        ),

        ""

    )



    if job_description:



        story.append(
            PageBreak()
        )



        add_section_title(
            "Job Description"
        )



        for line in job_description.splitlines():



            line = line.strip()



            if not line:



                continue



            story.append(

                Paragraph(
                    escape(
                        line
                    ),
                    normal_style
                )

            )



            story.append(
                Spacer(
                    1,
                    3
                )
            )



    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------



    try:



        doc.build(
            story
        )



    except Exception as e:



        print(
            "PDF generation error:",
            e
        )



        return (
            "Could not generate PDF report.",
            500
        )



    buffer.seek(
        0
    )



    candidate_name = safe_text(

        analysis.get(
            "candidate_name"
        ),

        "candidate"

    )



    filename = secure_filename(

        f"{candidate_name}_analysis_report.pdf"

    )



    if not filename:



        filename = (
            "resume_analysis_report.pdf"
        )



    return send_file(

        buffer,

        mimetype="application/pdf",

        as_attachment=True,

        download_name=filename

    )





# =========================================================

# DELETE SAVED ANALYSIS

# =========================================================



@app.route(
    "/analysis/<int:analysis_id>/delete",
    methods=["POST"]
)
def delete_saved_analysis(
    analysis_id
):



    try:



        deleted = delete_analysis(
            analysis_id
        )



    except Exception as e:



        print(
            "Delete analysis error:",
            e
        )



        return (
            "Could not delete analysis.",
            500
        )



    if not deleted:



        return (
            "Analysis not found.",
            404
        )



    return redirect(
        url_for("history")
    )





# =========================================================

# UPLOAD + ANALYSIS

# =========================================================



@app.route(

    "/upload",

    methods=["POST"]

)

def upload():



    # =====================================================

    # 1. CHECK RESUME FILE

    # =====================================================



    if "resume" not in request.files:



        return (

            "No resume file selected."

        )



    file = request.files[

        "resume"

    ]



    if file.filename == "":



        return (

            "Please choose a resume."

        )





    # =====================================================

    # 2. FILE TYPE

    # =====================================================



    filename = secure_filename(

        file.filename

    )



    if not filename.lower().endswith(

        ".pdf"

    ):



        return (

            "Currently only PDF resumes are supported."

        )





    # =====================================================

    # 3. JOB DESCRIPTION

    # =====================================================



    job_description = request.form.get(

        "job_description",

        ""

    ).strip()



    if not job_description:



        return (

            "Please enter a job description."

        )





    # =====================================================

    # 4. SAVE FILE

    # =====================================================



    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )



    try:



        file.save(

            filepath

        )



    except Exception as e:



        return (

            f"Could not save resume: {e}"

        )





    # =====================================================

    # 5. EXTRACT TEXT USING PDFPLUMBER

    # =====================================================



    text = extract_text_pdfplumber(

        filepath

    )



    if not text:



        return (

            "Could not extract text from this PDF. "

            "Please upload a text-based PDF."

        )





    # =====================================================

    # 6. EXTRACT SECOND COPY USING PYMUPDF

    # =====================================================



    pymupdf_text = (

        extract_text_pymupdf(

            filepath

        )

    )





    print()

    print(

        "========== PDF EXTRACTION =========="

    )



    print(

        "PDFPlumber characters:",

        len(text)

    )



    print(

        "PyMuPDF characters:",

        len(pymupdf_text)

    )



    print(

        "===================================="

    )





    # =====================================================

    # 7. EMAIL DEBUG

    # =====================================================



    print()

    print(

        "========== EMAIL DEBUG =========="

    )



    for line in text.splitlines():



        if (

            "@"

            in line

            or

            "mail"

            in line.lower()

        ):



            print(

                repr(line)

            )



    print(

        "================================="

    )





    # =====================================================

    # 8. BASIC CANDIDATE INFORMATION

    # =====================================================



    try:



        email = extract_email(

            text

        )



    except Exception as e:



        print(

            "Email extraction error:",

            e

        )



        email = ""





    try:



        phone = extract_phone(

            text

        )



    except Exception as e:



        print(

            "Phone extraction error:",

            e

        )



        phone = ""





    try:



        name = extract_name(

            text

        )



    except Exception as e:



        print(

            "Name extraction error:",

            e

        )



        name = "Unknown"





    # =====================================================

    # 9. RESUME SKILLS

    # =====================================================



    try:



        skills = extract_skills(

            text

        )



    except Exception as e:



        print(

            "Skills extraction error:",

            e

        )



        skills = []





    if skills is None:



        skills = []





    print()

    print(

        "========== RESUME SKILLS =========="

    )



    for skill in skills:



        print(

            "-",

            skill

        )



    print(

        "Total Resume Skills:",

        len(skills)

    )



    print(

        "===================================="

    )





    # =====================================================

    # 10. EDUCATION

    # =====================================================



    try:



        education = extract_education(

            text

        )



    except Exception as e:



        print(

            "Education extraction error:",

            e

        )



        education = []





    if education is None:



        education = []





    # =====================================================

    # 11. EDUCATION SECTION TEXT

    # =====================================================



    try:



        education_text = extract_section(



            text,



            "Education",



            [

                "Technical Skills",

                "Skills",

                "Projects",

                "Certificates",

                "Certificate",

                "Certifications",

                "Certification",

                "Experience",

                "Work Experience",

                "Internships",

                "Achievements",

                "Achievements & Certifications"

            ]

        )



    except Exception as e:



        print(

            "Education section extraction error:",

            e

        )



        education_text = ""





    # =====================================================

    # 12. PROJECT EXTRACTION

    # =====================================================



    print()

    print(

        "========== PROJECT EXTRACTION =========="

    )



    projects = []



    project_source = "None"



    try:



        projects, project_source = (

            extract_best_projects(

                pdfplumber_text=text,

                pymupdf_text=pymupdf_text

            )

        )



    except Exception as e:



        print(

            "Final project extraction error:",

            e

        )



        projects = []





    if projects is None:



        projects = []





    print()

    print(

        "========== FINAL PROJECT RESULT =========="

    )



    print(

        "Selected source:",

        project_source

    )



    print(

        "Number of projects:",

        len(projects)

    )



    for i, project in enumerate(

        projects,

        start=1

    ):



        print()

        print(

            f"Project #{i}"

        )



        print(

            "Title:",

            project.get(

                "title",

                ""

            )

        )



        print(

            "Technologies:",

            project.get(

                "technologies",

                []

            )

        )



        print(

            "Description:"

        )



        descriptions = project.get(

            "description",

            []

        )



        for description in descriptions:



            print(

                " -",

                description

            )



    print(

        "=========================================="

    )





    # =====================================================

    # 13. EXPERIENCE

    # =====================================================



    try:



        experience = extract_experience(

            text

        )



    except Exception as e:



        print(

            "Experience extraction error:",

            e

        )



        experience = {}





    if experience is None:



        experience = {}





    print()

    print(

        "========== EXPERIENCE =========="

    )



    print(

        "Total Years:",

        experience.get(

            "total_years",

            0

        )

    )



    print(

        "Stated Years:",

        experience.get(

            "stated_years",

            0

        )

    )



    print(

        "Calculated Years:",

        experience.get(

            "calculated_years",

            0

        )

    )



    print(

        "Job Titles:",

        experience.get(

            "job_titles",

            []

        )

    )



    print(

        "Date Ranges:",

        experience.get(

            "date_ranges",

            []

        )

    )



    print(

        "================================"

    )





    # =====================================================

    # 14. JOB REQUIRED SKILLS

    # =====================================================



    try:



        job_skills = extract_jd_skills(

            job_description

        )



    except Exception as e:



        print(

            "Job skill extraction error:",

            e

        )



        job_skills = []





    if job_skills is None:



        job_skills = []





    print()

    print(

        "========== JOB DESCRIPTION =========="

    )



    print(

        job_description

    )



    print(

        "======================================"

    )





    print()

    print(

        "========== JOB REQUIRED SKILLS =========="

    )



    for skill in job_skills:



        print(

            "-",

            skill

        )



    print(

        "Total Job Skills:",

        len(job_skills)

    )



    print(

        "=========================================="

    )





    # =====================================================

    # 15. ATS ANALYSIS

    # =====================================================



    try:



        ats_result = calculate_ats_score(



            resume_skills=skills,



            job_skills=job_skills,



            resume_text=text,



            job_description=job_description,



            candidate_experience=experience,



            education=education,



            projects=projects

        )



    except Exception as e:



        print(

            "ATS calculation error:",

            e

        )



        return (

            f"ATS analysis failed: {e}"

        )





    if ats_result is None:



        ats_result = {}





    # =====================================================

    # 16. ATS RESULTS

    # =====================================================



    ats_score = ats_result.get(

        "score",

        0

    )



    skill_score = ats_result.get(

        "skill_score",

        0

    )



    keyword_score = ats_result.get(

        "keyword_score",

        0

    )



    experience_score = ats_result.get(

        "experience_score",

        0

    )



    education_score = ats_result.get(

        "education_score",

        0

    )



    project_score = ats_result.get(

        "project_score",

        0

    )



    resume_quality_score = (

        ats_result.get(

            "resume_quality_score",

            0

        )

    )



    matching_skills = ats_result.get(

        "matching_skills",

        []

    )



    missing_skills = ats_result.get(

        "missing_skills",

        []

    )





    # =====================================================

    # 17. RECOMMENDED JOB ROLES

    # =====================================================



    try:



        recommended_roles = (

            recommend_job_roles(



                resume_skills=skills,



                top_n=5

            )

        )



    except Exception as e:



        print(

            "Role recommendation error:",

            e

        )



        recommended_roles = []





    if recommended_roles is None:



        recommended_roles = []


    # =====================================================

    # 17A. JOB MATCH ANALYSIS

    # =====================================================



    try:



        job_match_result = analyze_job_match(

            skills,

            job_skills

        )



    except Exception as e:



        print(

            "Job match analysis error:",

            e

        )



        job_match_result = {

            "match_score": 0,

            "match_category": ""

        }



    if job_match_result is None:



        job_match_result = {

            "match_score": 0,

            "match_category": ""

        }





    # =====================================================

    # 17B. RESUME IMPROVEMENT SUGGESTIONS

    # =====================================================



    try:



        suggestions = generate_suggestions(

            ats_score=ats_score,

            missing_skills=missing_skills,

            projects=projects,

            experience=experience,

            ats_result=ats_result,

            recommended_roles=recommended_roles,

            job_skills=job_skills

        )



    except Exception as e:



        print(

            "Suggestion generation error:",

            e

        )



        suggestions = []





    # =====================================================

    # 17C. SAVE ANALYSIS TO DATABASE

    # =====================================================



    analysis_id = None



    try:



        analysis_id = save_analysis(



            resume_filename=filename,



            candidate_name=name,



            email=email,



            phone=phone,



            resume_skills=skills,



            education=education,



            experience=experience,



            projects=projects,



            job_description=job_description,



            job_skills=job_skills,



            ats_result=ats_result,



            job_match_result=job_match_result,



            recommended_roles=recommended_roles

        )



        print()



        print(

            "========== DATABASE =========="

        )



        print(

            "Analysis saved successfully."

        )



        print(

            "Analysis ID:",

            analysis_id

        )



        print(

            "=============================="

        )



    except Exception as e:



        # A database failure must not block the result page.

        print()



        print(

            "Database save error:",

            e

        )






    # =====================================================

    # 18. FINAL DEBUG

    # =====================================================



    print()

    print(

        "======================================"

    )



    print(

        "        AI RESUME ANALYSIS"

    )



    print(

        "======================================"

    )





    print()

    print(

        "Extracted Name:"

    )



    print(

        name

    )





    print()

    print(

        "Extracted Email:"

    )



    print(

        email

    )





    print()

    print(

        "Extracted Phone:"

    )



    print(

        phone

    )





    print()

    print(

        "========== RESUME SKILLS =========="

    )



    print(

        skills

    )





    print()

    print(

        "========== JOB REQUIRED SKILLS =========="

    )



    print(

        job_skills

    )





    print()

    print(

        "========== MATCHING SKILLS =========="

    )



    print(

        matching_skills

    )





    print()

    print(

        "========== MISSING SKILLS =========="

    )



    print(

        missing_skills

    )





    print()

    print(

        "========== ATS SCORE =========="

    )



    print(

        "Skill Score:",

        skill_score

    )



    print(

        "Keyword Score:",

        keyword_score

    )



    print(

        "Experience Score:",

        experience_score

    )



    print(

        "Education Score:",

        education_score

    )



    print(

        "Project Score:",

        project_score

    )



    print(

        "Resume Quality Score:",

        resume_quality_score

    )



    print(

        "Final ATS Score:",

        ats_score

    )





    # =====================================================

    # 19. RECOMMENDED ROLES DEBUG

    # =====================================================



    print()

    print(

        "========== RECOMMENDED JOB ROLES =========="

    )



    if recommended_roles:



        for i, role in enumerate(

            recommended_roles,

            start=1

        ):



            print(

                f"#{i}",

                role.get(

                    "role",

                    "Unknown"

                ),

                "->",

                role.get(

                    "score",

                    0

                ),

                "%"

            )



            print(

                "Matching:",

                role.get(

                    "matching_skills",

                    []

                )

            )



            print(

                "Missing:",

                role.get(

                    "missing_skills",

                    []

                )

            )



    else:



        print(

            "No recommended roles."

        )



    print(

        "============================================"

    )





    # =====================================================

    # 20. EDUCATION DEBUG

    # =====================================================



    print()

    print(

        "========== EDUCATION SECTION =========="

    )



    print(

        education_text

    )





    # =====================================================

    # 21. PROJECT DEBUG

    # =====================================================



    print()

    print(

        "========== PROJECTS SECTION =========="

    )



    if projects:



        for i, project in enumerate(

            projects,

            start=1

        ):



            print()

            print(

                f"Project #{i}"

            )



            print(

                "Title:",

                project.get(

                    "title",

                    ""

                )

            )



            print(

                "Technologies:",

                project.get(

                    "technologies",

                    []

                )

            )



            print(

                "Description:"

            )



            descriptions = project.get(

                "description",

                []

            )



            if descriptions:



                for description in descriptions:



                    print(

                        " -",

                        description

                    )



            else:



                print(

                    " - No project description detected."

                )



    else:



        print(

            "No projects found."

        )



    print(

        "======================================"

    )





    # =====================================================

    # 22. ANALYSIS COMPLETE

    # =====================================================



    print()

    print(

        "======================================"

    )



    print(

        "        ANALYSIS COMPLETED"

    )



    print(

        "======================================"

    )





    # =====================================================

    # 23. RESULT PAGE

    # =====================================================



    return render_template(



        "2_result.html",



        # Candidate

        name=name,

        email=email,

        phone=phone,



        # Resume

        skills=skills,

        education=education,

        education_text=education_text,

        projects=projects,

        experience=experience,



        # Keep original pdfplumber text

        # for the Extracted Resume Text section.

        text=text,



        # Job

        job_description=job_description,

        job_skills=job_skills,

        matching_skills=matching_skills,

        missing_skills=missing_skills,



        # ATS

        ats_score=ats_score,

        skill_score=skill_score,

        keyword_score=keyword_score,

        experience_score=experience_score,

        education_score=education_score,

        project_score=project_score,

        resume_quality_score=resume_quality_score,



        # Roles

        recommended_roles=recommended_roles,



        # Resume improvement suggestions

        suggestions=suggestions,



        # Job match

        job_match_result=job_match_result,



        # Database

        analysis_id=analysis_id

    )





# =========================================================

# RUN APPLICATION

# =========================================================



if __name__ == "__main__":



    app.run(

        debug=True

    )