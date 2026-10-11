# resume_parser/job_roles.py


# =========================================================
# JOB ROLE SKILL DEFINITIONS
# =========================================================
#
# These skills represent the expected skills for each role.
#
# The role_recommender.py file uses these skills to:
#
# 1. Compare resume skills
# 2. Calculate matching skills
# 3. Identify missing skills
# 4. Calculate role score
# 5. Recommend suitable career roles
#
# =========================================================


JOB_ROLES = {

    # =====================================================
    # SOFTWARE DEVELOPMENT
    # =====================================================

    "Python Developer": [

        "Python",
        "Flask",
        "Django",
        "FastAPI",
        "REST API",
        "SQL",
        "Git",
        "GitHub",

    ],


    "Java Developer": [

        "Java",
        "Spring",
        "Spring Boot",
        "REST API",
        "SQL",
        "Git",

    ],


    "C++ Developer": [

        "C++",
        "C",
        "Data Structures",
        "Algorithms",
        "SQL",
        "Git",

    ],


    "C# Developer": [

        "C#",
        ".NET",
        "ASP.NET",
        "REST API",
        "SQL",

    ],


    "Backend Developer": [

        "Python",
        "Java",
        "Node.js",
        "Express.js",
        "Flask",
        "Django",
        "FastAPI",
        "REST API",
        "SQL",
        "MongoDB",
        "Git",

    ],


    "Frontend Developer": [

        "JavaScript",
        "React",
        "Angular",
        "Vue.js",
        "HTML",
        "CSS",
        "Git",

    ],


    "Full Stack Developer": [

        "JavaScript",
        "React",
        "Node.js",
        "Express.js",
        "MongoDB",
        "REST API",
        "HTML",
        "CSS",
        "SQL",
        "Git",

    ],


    # =====================================================
    # AI / MACHINE LEARNING
    # =====================================================

    "AI/ML Engineer": [

        "Python",
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Computer Vision",

    ],


    "Machine Learning Engineer": [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "XGBoost",
        "Feature Engineering",
        "Data Preprocessing",

    ],


    "Data Scientist": [

        "Python",
        "Machine Learning",
        "Statistics",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Data Analysis",
        "Data Visualization",
        "Matplotlib",

    ],


    "Data Analyst": [

        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Microsoft Excel",
        "Statistics",
        "Data Analysis",
        "Data Visualization",
        "Matplotlib",

    ],


    "NLP Engineer": [

        "Python",
        "NLP",
        "Natural Language Processing",
        "Machine Learning",
        "Deep Learning",
        "Transformers",
        "BERT",
        "GPT",
        "Hugging Face",

    ],


    "Computer Vision Engineer": [

        "Python",
        "Computer Vision",
        "Deep Learning",
        "OpenCV",
        "TensorFlow",
        "PyTorch",
        "CNN",
        "YOLO",

    ],


    "Generative AI Engineer": [

        "Python",
        "Generative AI",
        "Large Language Models",
        "LLM",
        "Transformers",
        "NLP",
        "GPT",
        "Hugging Face",

    ],


    # =====================================================
    # CLOUD / DEVOPS
    # =====================================================

    "Cloud Engineer": [

        "AWS",
        "Azure",
        "Google Cloud",
        "GCP",
        "Docker",
        "Kubernetes",
        "Linux",

    ],


    "DevOps Engineer": [

        "AWS",
        "Docker",
        "Kubernetes",
        "Jenkins",
        "CI/CD",
        "Linux",
        "Git",

    ],


    # =====================================================
    # CYBERSECURITY
    # =====================================================

    "Cybersecurity Analyst": [

        "Cybersecurity",
        "Network Security",
        "Information Security",
        "SIEM",
        "Firewall",
        "IDS",
        "IPS",
        "Linux",

    ],


    "Security Engineer": [

        "Cybersecurity",
        "Network Security",
        "Information Security",
        "Penetration Testing",
        "Firewall",
        "IDS",
        "IPS",
        "Linux",

    ],


    "Ethical Hacker": [

        "Cybersecurity",
        "Ethical Hacking",
        "Penetration Testing",
        "Network Security",
        "Linux",

    ],


    # =====================================================
    # DATABASE
    # =====================================================

    "Database Developer": [

        "SQL",
        "MySQL",
        "PostgreSQL",
        "Oracle",
        "MongoDB",

    ],


    "Database Administrator": [

        "SQL",
        "MySQL",
        "PostgreSQL",
        "Oracle",
        "MongoDB",
        "Linux",

    ],


    # =====================================================
    # SOFTWARE TESTING
    # =====================================================

    "Software Tester": [

        "Software Testing",
        "Manual Testing",
        "Test Cases",
        "Bug Tracking",
        "SQL",

    ],


    "Automation Test Engineer": [

        "Software Testing",
        "Automation Testing",
        "Selenium",
        "Python",
        "Java",
        "SQL",

    ],


    # =====================================================
    # MOBILE DEVELOPMENT
    # =====================================================

    "Android Developer": [

        "Android",
        "Android Studio",
        "Java",
        "Kotlin",

    ],


    "Flutter Developer": [

        "Flutter",
        "Dart",
        "Android",

    ],


    # =====================================================
    # DIGITAL MARKETING
    # =====================================================

    "Digital Marketing Specialist": [

        "SEO",
        "Google Ads",
        "Meta Ads Manager",
        "Content Strategy",
        "Email Marketing",
        "Google Analytics",
        "Marketing Automation",
        "HubSpot",
        "A/B Testing",
        "Copywriting",

    ],


    "SEO Specialist": [

        "SEO",
        "Google Analytics",
        "Content Strategy",
        "Copywriting",

    ],


    "Performance Marketing Specialist": [

        "Google Ads",
        "Meta Ads Manager",
        "Google Analytics",
        "A/B Testing",
        "Marketing Automation",

    ],


    "Content Marketing Specialist": [

        "Content Strategy",
        "Content Marketing",
        "Copywriting",
        "SEO",
        "Canva",

    ],


    # =====================================================
    # MECHANICAL
    # =====================================================

    "Mechanical Design Engineer": [

        "Mechanical Design",
        "CAD",
        "SolidWorks",
        "CATIA",
        "AutoCAD",
        "GD&T",

    ],


    "Automotive Design Engineer": [

        "Mechanical Design",
        "Automotive Design",
        "SolidWorks",
        "CATIA",
        "AutoCAD",
        "GD&T",
        "DFMEA",

    ],


    "FEA Engineer": [

        "FEA",
        "ANSYS",
        "Mechanical Design",
        "CAD",
        "GD&T",

    ],


    "Manufacturing Engineer": [

        "Manufacturing",
        "Mechanical Design",
        "CAD",
        "Tooling",
        "GD&T",
        "DFMEA",

    ],
}