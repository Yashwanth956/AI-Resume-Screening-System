# ============================================================
# resume_parser/master_skills.py
# CENTRAL MASTER SKILLS DATABASE
# ============================================================

"""
Central skill database for resume extraction, JD extraction,
ATS scoring, job matching, role recommendation and normalization.

This is broad practical IT coverage, not a claim that a static list can
contain every technology that will ever exist. Add new canonical skills
or aliases here only; other modules should import from this file.
"""

SKILL_GROUPS = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
        "PHP", "Ruby", "Go", "Rust", "Kotlin", "Swift", "Dart", "R",
        "Scala", "Bash", "PowerShell", "Perl", "MATLAB", "Groovy", "Lua",
        "Objective-C", "Solidity", "ABAP", "Apex",
    ],
    "Software Engineering": [
        "Data Structures", "Algorithms", "Object-Oriented Programming",
        "Functional Programming", "Problem Solving", "Software Engineering",
        "Software Development", "System Design", "Design Patterns",
        "SOLID Principles", "Clean Architecture", "Domain-Driven Design",
        "Distributed Systems", "Event-Driven Architecture", "Microservices",
        "Monolithic Architecture", "API Design", "Code Review", "Debugging",
        "Performance Optimization", "Concurrency", "Multithreading",
        "Memory Management", "SDLC", "Agile", "Scrum", "Kanban",
    ],
    "Frontend Development": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular",
        "Vue.js", "Next.js", "Nuxt.js", "Svelte", "SvelteKit", "Redux",
        "Redux Toolkit", "Zustand", "RxJS", "Tailwind CSS", "Bootstrap",
        "Material UI", "Sass", "SCSS", "Responsive Design",
        "Web Accessibility", "Web Performance", "Webpack", "Vite", "Babel",
    ],
    "Backend Development": [
        "Node.js", "Express.js", "NestJS", "Flask", "Django", "FastAPI",
        "Spring", "Spring Boot", "Spring Security", "Hibernate", "JPA",
        ".NET", "ASP.NET Core", "Entity Framework", "Laravel", "Symfony",
        "Ruby on Rails", "REST API", "GraphQL", "gRPC", "WebSockets",
        "OpenAPI", "Swagger", "JWT Authentication", "OAuth 2.0",
        "OpenID Connect", "Authentication", "Authorization", "API Development",
        "API Integration", "CRUD", "Maven", "Gradle", "LINQ", "Blazor",
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "Microsoft SQL Server", "Oracle",
        "SQLite", "MariaDB", "MongoDB", "Redis", "Cassandra", "DynamoDB",
        "Firebase", "Firestore", "CouchDB", "Neo4j", "Elasticsearch",
        "OpenSearch", "Snowflake", "BigQuery", "Amazon Redshift", "NoSQL",
        "PL/SQL", "T-SQL", "Stored Procedures", "Database Design",
        "Database Management", "Database Administration", "Data Modeling",
        "Query Optimization", "Indexing", "Replication", "Backup and Recovery",
    ],
    "Data Analytics & BI": [
        "Data Analysis", "Data Analytics", "Data Visualization",
        "Business Intelligence", "Microsoft Excel", "Advanced Excel", "Power BI",
        "Tableau", "Looker", "Looker Studio", "Qlik Sense", "DAX",
        "Power Query", "Google Analytics", "SPSS", "SAS", "Statistics",
        "Statistical Analysis", "Hypothesis Testing", "A/B Testing",
    ],
    "Data Engineering": [
        "Data Engineering", "ETL", "ELT", "Data Pipelines", "Apache Spark",
        "PySpark", "Hadoop", "Hive", "HBase", "Apache Kafka",
        "Apache Airflow", "dbt", "Databricks", "Delta Lake", "Data Lake",
        "Data Lakehouse", "Data Warehouse", "Data Warehousing",
        "Batch Processing", "Stream Processing", "Apache Flink", "Apache Beam",
        "Talend", "Informatica", "Azure Data Factory", "AWS Glue",
        "Google Dataflow", "Snowflake", "BigQuery", "Amazon Redshift",
    ],
    "AI & Machine Learning": [
        "Artificial Intelligence", "Machine Learning", "Deep Learning",
        "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning",
        "Classification", "Regression", "Clustering", "Feature Engineering",
        "Feature Selection", "Data Preprocessing", "Model Evaluation",
        "Hyperparameter Tuning", "Cross Validation", "Time Series",
        "Forecasting", "Predictive Analytics", "Recommendation Systems",
        "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost",
        "LightGBM", "CatBoost", "NumPy", "Pandas", "SciPy", "Matplotlib",
        "Seaborn", "Jupyter", "Google Colab",
    ],
    "NLP & Generative AI": [
        "NLP", "Natural Language Processing", "Transformers", "BERT", "GPT",
        "LLM", "Large Language Models", "Generative AI", "Agentic AI",
        "AI Agents", "RAG", "Retrieval-Augmented Generation", "LangChain",
        "LlamaIndex", "Hugging Face", "Sentence Transformers",
        "Sentence Embeddings", "Embeddings", "Semantic Search", "Vector Search",
        "Vector Database", "FAISS", "ChromaDB", "Pinecone", "Weaviate",
        "Milvus", "Qdrant", "Prompt Engineering", "Prompt Design",
        "Fine-Tuning", "LoRA", "PEFT", "RLHF", "Reranking",
        "Function Calling", "Tool Calling", "OpenAI API", "Anthropic API",
        "Gemini API", "Ollama", "vLLM", "Tokenization",
        "Named Entity Recognition", "Text Classification", "Sentiment Analysis",
        "Text Generation", "Question Answering", "Information Retrieval",
    ],
    "Computer Vision": [
        "Computer Vision", "OpenCV", "CNN", "YOLO", "Image Classification",
        "Object Detection", "Image Segmentation", "OCR", "Face Recognition",
        "Pose Estimation", "Image Processing", "Transfer Learning", "ResNet",
        "UNet", "Vision Transformers",
    ],
    "MLOps": [
        "MLOps", "MLflow", "DVC", "Kubeflow", "Model Deployment",
        "Model Serving", "Model Monitoring", "Model Registry",
        "Experiment Tracking", "Feature Store", "BentoML", "ONNX", "Ray",
        "AWS SageMaker", "Azure Machine Learning", "Vertex AI",
    ],
    "Cloud Computing": [
        "AWS", "Azure", "Google Cloud", "Cloud Computing", "AWS EC2", "AWS S3",
        "AWS Lambda", "AWS RDS", "AWS ECS", "AWS EKS", "AWS IAM",
        "AWS CloudWatch", "AWS CloudFormation", "AWS API Gateway", "AWS Glue",
        "AWS SageMaker", "Amazon Redshift", "Azure Functions",
        "Azure App Service", "Azure Blob Storage", "Azure SQL", "Azure DevOps",
        "Azure Kubernetes Service", "Azure Data Factory", "Azure Synapse",
        "Azure Machine Learning", "Google Compute Engine", "Google Cloud Storage",
        "Google Cloud Functions", "Google Kubernetes Engine", "BigQuery",
        "Pub/Sub", "Google Dataflow", "Vertex AI", "Serverless",
    ],
    "DevOps & SRE": [
        "DevOps", "Site Reliability Engineering", "Platform Engineering",
        "Docker", "Kubernetes", "OpenShift", "Helm", "Jenkins",
        "GitHub Actions", "GitLab CI/CD", "CircleCI", "CI/CD", "Terraform",
        "Ansible", "Puppet", "Chef", "Argo CD", "FluxCD", "Nginx",
        "Apache HTTP Server", "Linux", "Bash", "Shell Scripting",
        "Infrastructure as Code", "Configuration Management", "Containerization",
        "Orchestration", "Blue-Green Deployment", "Canary Deployment",
        "Prometheus", "Grafana", "ELK Stack", "Elastic Stack", "Logstash",
        "Kibana", "Datadog", "New Relic", "Splunk", "PagerDuty",
        "Observability", "Monitoring", "Logging",
    ],
    "Developer Tools & Collaboration": [
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "VS Code",
        "Visual Studio", "IntelliJ IDEA", "Eclipse", "PyCharm", "Postman",
        "Jira", "Confluence",
    ],
    "Cybersecurity": [
        "Cybersecurity", "Network Security", "Information Security",
        "Application Security", "Cloud Security", "SIEM", "SOC", "Firewall",
        "IDS", "IPS", "Incident Response", "Threat Hunting",
        "Threat Intelligence", "Vulnerability Assessment",
        "Vulnerability Management", "Penetration Testing", "Ethical Hacking",
        "Security Testing", "Digital Forensics", "Cryptography",
        "Identity and Access Management", "IAM", "Zero Trust", "EDR", "XDR",
        "DLP", "WAF", "SAST", "DAST", "OWASP", "OWASP Top 10",
        "Burp Suite", "Nmap", "Wireshark", "Nessus", "Metasploit",
        "Kali Linux", "Microsoft Sentinel", "CrowdStrike", "Qualys", "TLS",
        "SSL", "PKI", "ISO 27001", "SOC 2", "PCI DSS",
    ],
    "Networking": [
        "Computer Networks", "Networking", "TCP/IP", "DNS", "DHCP", "HTTP",
        "HTTPS", "VPN", "LAN", "WAN", "VLAN", "Routing", "Switching", "BGP",
        "OSPF", "Cisco", "Cisco IOS", "Load Balancing", "Proxy",
        "Reverse Proxy", "Network Troubleshooting",
    ],
    "System & IT Administration": [
        "Linux Administration", "Windows Server", "Active Directory",
        "Microsoft Entra ID", "Azure Active Directory", "Microsoft 365", "Intune",
        "SCCM", "VMware", "Hyper-V", "Virtualization", "System Administration",
        "Server Administration", "Patch Management", "IT Support",
        "Technical Support", "Service Desk", "Help Desk", "ITIL",
        "Troubleshooting", "Remote Desktop", "Ticketing Systems",
    ],
    "Testing & QA": [
        "Software Testing", "Manual Testing", "Automation Testing",
        "Test Automation", "Unit Testing", "Integration Testing", "System Testing",
        "Regression Testing", "Smoke Testing", "API Testing", "Performance Testing",
        "Load Testing", "End-to-End Testing", "Selenium", "Cypress", "Playwright",
        "Appium", "Pytest", "JUnit", "TestNG", "Mockito", "Cucumber", "BDD",
        "JMeter", "Test Cases", "Test Plans", "Bug Tracking", "Quality Assurance",
    ],
    "Mobile Development": [
        "Android", "Android Studio", "Kotlin", "Jetpack Compose", "iOS", "Swift",
        "SwiftUI", "Xcode", "Flutter", "Dart", "React Native", "Firebase",
        "Mobile App Development",
    ],
    "UI UX": [
        "UI Design", "UX Design", "UI/UX", "Figma", "Adobe XD", "Wireframing",
        "Prototyping", "User Research", "Design Systems", "Usability Testing",
    ],
    "Enterprise Platforms": [
        "Salesforce", "Salesforce Apex", "Lightning Web Components", "SAP",
        "SAP ABAP", "SAP HANA", "ServiceNow", "Oracle Fusion", "Workday", "CRM", "ERP",
    ],
    "Automation & Low Code": [
        "RPA", "UiPath", "Automation Anywhere", "Blue Prism", "Power Automate",
        "Power Apps", "Zapier", "Workflow Automation",
    ],
    "Blockchain": [
        "Blockchain", "Ethereum", "Solidity", "Smart Contracts", "Web3",
        "Web3.js", "Ethers.js", "Hardhat", "Truffle",
    ],
    "IoT & Embedded": [
        "IoT", "Internet of Things", "Embedded Systems", "Arduino", "Raspberry Pi",
        "ESP32", "Microcontrollers", "MQTT", "GSM", "RTOS", "UART", "I2C",
        "SPI", "CAN Bus", "Sensors",
    ],
    "Game Development": [
        "Unity", "Unreal Engine", "Game Development",
    ],
    "Digital Marketing & MarTech": [
        "SEO", "SEM", "Google Ads", "Meta Ads Manager", "Google Analytics", "GA4",
        "Content Strategy", "Content Marketing", "Email Marketing",
        "Marketing Automation", "HubSpot", "A/B Testing", "Copywriting", "Canva",
    ],
}


# ============================================================
# FLATTEN CANONICAL SKILLS
# ============================================================

ALL_SKILLS = []
_seen = set()

for _category_skills in SKILL_GROUPS.values():
    for _skill in _category_skills:
        _key = _skill.strip().lower()
        if _key not in _seen:
            _seen.add(_key)
            ALL_SKILLS.append(_skill)


# ============================================================
# ALIASES
# ============================================================

SKILL_ALIASES = {
    # Compatibility aliases from the existing project
    "html5": "HTML", "html 5": "HTML",
    "css3": "CSS", "css 3": "CSS",
    "javascript es6": "JavaScript",
    "javascript es6+": "JavaScript",
    "javascript (es6+)": "JavaScript",
    "typescript basics": "TypeScript",
    "python basics": "Python",
    "tensor flow": "TensorFlow",
    "restful": "REST API",
    "colab": "Google Colab",
    "hugging face": "Hugging Face",

    # Languages / frameworks
    "python3": "Python", "python 3": "Python",
    "js": "JavaScript", "ts": "TypeScript", "golang": "Go",
    "c sharp": "C#", "csharp": "C#", "cpp": "C++", "c plus plus": "C++",
    "react.js": "React", "reactjs": "React", "react js": "React",
    "nextjs": "Next.js", "next js": "Next.js", "vue": "Vue.js",
    "vuejs": "Vue.js", "tailwind": "Tailwind CSS", "mui": "Material UI",
    "nodejs": "Node.js", "node js": "Node.js", "expressjs": "Express.js",
    "express js": "Express.js", "nest.js": "NestJS", "springboot": "Spring Boot",
    "dotnet": ".NET", "asp.net": "ASP.NET Core", "asp net core": "ASP.NET Core",

    # APIs / auth
    "rest api": "REST API", "rest apis": "REST API", "restful api": "REST API",
    "restful apis": "REST API", "jwt": "JWT Authentication", "jwt auth": "JWT Authentication",
    "oauth": "OAuth 2.0", "oauth2": "OAuth 2.0", "oauth 2": "OAuth 2.0",
    "openid": "OpenID Connect", "oidc": "OpenID Connect",

    # Databases
    "postgres": "PostgreSQL", "postgres db": "PostgreSQL", "mongo": "MongoDB",
    "mongo db": "MongoDB", "mssql": "Microsoft SQL Server", "ms sql": "Microsoft SQL Server",
    "sql server": "Microsoft SQL Server", "plsql": "PL/SQL", "tsql": "T-SQL",
    "elastic search": "Elasticsearch", "dynamo db": "DynamoDB", "no sql": "NoSQL",

    # AI/ML
    "ai": "Artificial Intelligence", "a.i": "Artificial Intelligence",
    "ml": "Machine Learning", "m.l": "Machine Learning", "dl": "Deep Learning",
    "sklearn": "Scikit-learn", "scikit learn": "Scikit-learn", "tf": "TensorFlow",
    "torch": "PyTorch", "xg boost": "XGBoost", "light gbm": "LightGBM",
    "cross-validation": "Cross Validation", "hyper parameter tuning": "Hyperparameter Tuning",

    # NLP / GenAI
    "natural-language processing": "NLP", "natural language processing": "NLP",
    "llms": "LLM", "large language model": "LLM", "large language models": "LLM",
    "genai": "Generative AI", "gen ai": "Generative AI", "generative-ai": "Generative AI",
    "ai agent": "AI Agents", "ai agents": "AI Agents",
    "retrieval augmented generation": "RAG", "retrieval-augmented generation": "RAG",
    "lang chain": "LangChain", "llama index": "LlamaIndex",
    "huggingface": "Hugging Face", "hugging face transformers": "Hugging Face",
    "sentence-transformers": "Sentence Transformers", "sentence transformer": "Sentence Transformers",
    "sentence embedding": "Sentence Embeddings", "vector db": "Vector Database",
    "vector databases": "Vector Database", "chroma": "ChromaDB", "chroma db": "ChromaDB",
    "pinecone db": "Pinecone", "openai": "OpenAI API", "open ai api": "OpenAI API",
    "anthropic": "Anthropic API", "claude api": "Anthropic API",
    "google gemini api": "Gemini API", "gemini": "Gemini API",
    "fine tuning": "Fine-Tuning", "low rank adaptation": "LoRA",
    "function-calling": "Function Calling", "tool-calling": "Tool Calling",

    # CV / MLOps
    "cv": "Computer Vision", "open cv": "OpenCV", "vit": "Vision Transformers",
    "ml ops": "MLOps", "azure ml": "Azure Machine Learning",
    "sagemaker": "AWS SageMaker", "aws sage maker": "AWS SageMaker",

    # Cloud
    "amazon web services": "AWS", "gcp": "Google Cloud", "google cloud platform": "Google Cloud",
    "microsoft azure": "Azure", "ec2": "AWS EC2", "s3": "AWS S3",
    "aws s3 bucket": "AWS S3", "lambda": "AWS Lambda", "rds": "AWS RDS",
    "eks": "AWS EKS", "ecs": "AWS ECS", "cloudwatch": "AWS CloudWatch",
    "cloudformation": "AWS CloudFormation", "aks": "Azure Kubernetes Service",
    "gke": "Google Kubernetes Engine", "gcs": "Google Cloud Storage",

    # DevOps
    "k8s": "Kubernetes", "cicd": "CI/CD", "ci cd": "CI/CD",
    "github action": "GitHub Actions", "gitlab ci": "GitLab CI/CD",
    "gitlab cicd": "GitLab CI/CD", "iac": "Infrastructure as Code",
    "argocd": "Argo CD", "argo": "Argo CD", "elk": "ELK Stack",
    "sre": "Site Reliability Engineering",

    # Version control
    "git hub": "GitHub", "github.com": "GitHub", "git lab": "GitLab",

    # Security
    "cyber security": "Cybersecurity", "infosec": "Information Security",
    "appsec": "Application Security", "security operations center": "SOC",
    "intrusion detection system": "IDS", "intrusion detection systems": "IDS",
    "intrusion prevention system": "IPS", "intrusion prevention systems": "IPS",
    "vulnerability scanning": "Vulnerability Assessment", "vapt": "Vulnerability Assessment",
    "pen test": "Penetration Testing", "pentesting": "Penetration Testing",
    "identity access management": "Identity and Access Management",
    "web application firewall": "WAF", "owasp top ten": "OWASP Top 10",
    "azure sentinel": "Microsoft Sentinel", "ms sentinel": "Microsoft Sentinel",

    # Networking
    "tcp ip": "TCP/IP", "tcp-ip": "TCP/IP", "domain name system": "DNS",
    "dynamic host configuration protocol": "DHCP", "virtual private network": "VPN",

    # Systems
    "ad": "Active Directory", "azure ad": "Azure Active Directory",
    "entra id": "Microsoft Entra ID", "office 365": "Microsoft 365", "o365": "Microsoft 365",
    "sysadmin": "System Administration", "system admin": "System Administration",

    # QA
    "qa": "Quality Assurance", "e2e testing": "End-to-End Testing",
    "end to end testing": "End-to-End Testing", "test ng": "TestNG",

    # Mobile / BI / enterprise / RPA
    "reactnative": "React Native", "powerbi": "Power BI", "powerquery": "Power Query",
    "google data studio": "Looker Studio", "lwc": "Lightning Web Components",
    "robotic process automation": "RPA", "ms power automate": "Power Automate",

    # Blockchain / IoT / analytics
    "smart contract": "Smart Contracts", "web3js": "Web3.js",
    "internet of things": "IoT", "raspberrypi": "Raspberry Pi", "esp-32": "ESP32",
    "google analytics 4": "GA4", "search engine optimization": "SEO",
    "search engine marketing": "SEM",
}


# ============================================================
# BUILD LOOKUPS
# ============================================================

_CANONICAL_BY_LOWER = {skill.lower(): skill for skill in ALL_SKILLS}

# If an alias target is not already canonical, add it for compatibility.
for _alias, _canonical in list(SKILL_ALIASES.items()):
    _key = _canonical.lower()
    if _key not in _CANONICAL_BY_LOWER:
        ALL_SKILLS.append(_canonical)
        _CANONICAL_BY_LOWER[_key] = _canonical

SKILL_SEARCH_MAP = {skill.lower(): skill for skill in ALL_SKILLS}
for _alias, _canonical in SKILL_ALIASES.items():
    SKILL_SEARCH_MAP[_alias.lower()] = _canonical

# Old code imports MASTER_SKILLS.
MASTER_SKILLS = ALL_SKILLS


def _normalized_compare_text(value):
    value = str(value).strip().lower()
    for character in ("-", "_", ".", "/"):
        value = value.replace(character, " ")
    return " ".join(value.split())


def normalize_skill(skill):

    """Return the canonical skill name for a canonical name or alias."""

    if skill is None:
        return ""

    value = str(skill).strip().strip(" \t\n\r,;:|")

    if not value:
        return ""

    lower = value.lower()

    # --------------------------------------------------------
    # 1. CHECK SEARCH MAP / ALIASES FIRST
    # --------------------------------------------------------

    if lower in SKILL_SEARCH_MAP:
        return SKILL_SEARCH_MAP[lower]

    # --------------------------------------------------------
    # 2. CHECK CANONICAL SKILLS
    # --------------------------------------------------------

    if lower in _CANONICAL_BY_LOWER:
        return _CANONICAL_BY_LOWER[lower]

    # --------------------------------------------------------
    # 3. NORMALIZED TEXT COMPARISON
    # --------------------------------------------------------

    normalized = _normalized_compare_text(value)

    for term, canonical in SKILL_SEARCH_MAP.items():

        if _normalized_compare_text(term) == normalized:
            return canonical

    # Backward-compatible behavior:
    # preserve unknown values.
    return value


def normalize_skill_list(skills):
    if not skills:
        return []

    result = []
    seen = set()

    for skill in skills:
        normalized = normalize_skill(skill)
        if not normalized:
            continue
        key = normalized.lower()
        if key not in seen:
            seen.add(key)
            result.append(normalized)

    return result


def find_master_skill(skill):
    if not skill:
        return None
    normalized = normalize_skill(skill)
    return _CANONICAL_BY_LOWER.get(normalized.lower())


def is_master_skill(skill):
    return find_master_skill(skill) is not None


def get_all_skills():
    return list(ALL_SKILLS)


def get_skill_search_map():
    """lowercase canonical/alias search phrase -> canonical skill"""
    return dict(SKILL_SEARCH_MAP)


def get_skill_search_terms():
    return list(SKILL_SEARCH_MAP.keys())


if __name__ == "__main__":
    tests = [
        "python3", "reactjs", "REST APIs", "postgres", "ML", "sklearn",
        "GenAI", "LLMs", "retrieval augmented generation", "lang chain",
        "chroma db", "sentence-transformers", "open ai api", "MLflow",
        "k8s", "AWS S3", "Azure ML", "tcp ip", "incident response",
        "azure sentinel", "PowerBI", "SpringBoot", "dotnet", "Azure AD",
    ]

    print("=" * 72)
    print("MASTER SKILLS SELF TEST")
    print("=" * 72)

    for item in tests:
        print(f"{item:38} -> {normalize_skill(item)}")

    print()
    print("Canonical skills:", len(ALL_SKILLS))
    print("Search terms including aliases:", len(SKILL_SEARCH_MAP))
