import os

# ==========================================
# 1. JOB SEARCH PARAMETERS
# ==========================================
# The exact search queries the agent will type into LinkedIn
TARGET_ROLES = [
    "Data Engineer",
    "Senior Data Engineer",
    "AI Engineer GCP"
]

LOCATION = "Remote"

# ==========================================
# 2. THE AI CONTEXT (FULL PLAIN-TEXT RESUME)
# ==========================================
# Minimum ATS score required to trigger an application
MIN_ATS_SCORE = 75 

RESUME_TEXT = """
Name: Balmukund Desai
Email: bmdesai.dev@gmail.com
Work Authorization: US OPT Visa (Started Oct 2025)

SUMMARY:
- Data Engineer with 6 years of experience designing and managing scalable data pipelines across Google Cloud Platform(GCP), Azure, and AWS.
- Expertise in building scalable MLOps frameworks with Vertex AI and enforcing enterprise-grade data governance.
- Built a scalable streaming ingestion framework using Cloud Dataflow to orchestrate data movement from Google Cloud Storage (GCS) into BigQuery, optimizing for low-latency processing and schema evolution.
- Optimized BigQuery storage and compute costs by implementing advanced partitioning, clustering strategies, and materialized views for high-volume Search Analytics datasets.
- Engineered serverless ETL pipelines on Cloud Dataflow to perform complex windowing and aggregations, ensuring exactly-once processing for financial transaction data before loading into BigQuery.
- Streamlined the transition of raw Google Cloud Storage (GCS) assets to production-ready tables by leveraging Cloud Dataflow for automated schema validation and data cleansing.
- Expert in PySpark and Databricks, with deep experience building real-time streaming jobs between BigQuery and Kafka clusters.
- Expert in designing and implementing Medallion Architectures (Bronze/Silver/Gold) using Delta Lake and Snowflake, bridging the gap between raw data lakes and high-performance warehousing.
- Specialist in Spark Performance Tuning and cloud resource management, with a proven track record of reducing compute costs through Predicate Pushdown, Z-Ordering, and strategic GKE resource isolation.
- Implemented Databricks Unity Catalog to provide a unified interface for data discovery, lineage tracking, and fine-grained access control across the entire Lakehouse.
- Advanced background in Data Security and Compliance (HIPAA/GDPR), implementing robust encryption protocols (RSA/SSL), VPC Service Controls, and centralized identity management via IAM and KMS.
- Specialist in advanced Airflow orchestration, including building "DAG Factories" using Jinja2 and YAML to automate the generation of hundreds of production pipelines.
- Strong background in Python automation, specifically in creating metadata-driven frameworks for high-volume API ingestion and enterprise-level ELT.
- Expert in data quality and observability, implementing Great Expectations for automated validation and PagerDuty for real-time incident response.
- Heavy focus on data security and reliability, including implementing RSA encryption, JKS certificate handling, and Kubernetes-based resource isolation.
- Proven consultant for major retail, financial, and media clients, delivering idempotent and highly automated data solutions.

EDUCATION:
- Master of Science in Information Technology Management, Campbellsville University

EXPERIENCE:
Cloud Data Engineer / OBT Solution
- Built an Apache Beam-based ingestion engine on Cloud Dataflow, enabling high-throughput data loads from Google Cloud Storage (GCS) into BigQuery for downstream analytical use.
- Architected a Cross-Project DAG Execution model, allowing a centralized Composer environment to trigger and monitor data jobs across multiple GCP projects.
- Enhanced pipeline reliability by building Custom Airflow Plugins to interface with proprietary APIs and automate administrative tasks within the Cloud Console.
- Engineered a Dead Letter Queue (DLQ) pattern within Dataflow to capture and reroute malformed records, ensuring zero data loss during high-velocity streaming.
- Built a multi-stage Data Lakehouse on Google Cloud Platform (GCP), utilizing Delta Lake on Google Cloud Storage (GCS) to provide ACID transactions and schema enforcement for sensitive healthcare datasets.
- Engineered a high-performance processing engine using PySpark on Cloud Dataproc, implementing custom logic to transform high-volume billing data and clinical datasets within the Data Lakehouse.
- Integrated a unified data governance fabric using Google Dataplex, enabling centralized metadata management and security policy enforcement across the Google Cloud Storage (GCS) and BigQuery layers.
- Designed and deployed serverless ETL pipelines using Cloud Dataflow (Apache Beam) to handle real-time stream processing of healthcare telemetry data into BigQuery.
- Architected an event-driven messaging backbone using Cloud Pub/Sub to decouple ingestion services from downstream Cloud Dataflow processing jobs, improving system resilience.
- Developed an automated synchronization pipeline using Spark to bridge the gap between analytical and operational layers, syncing results from Google Cloud Storage (GCS) to a Couchbase NoSQL database for sub-second UI response times.
- Orchestrated complex, event-driven workflows using Google Cloud Composer (Managed Airflow), designing custom operators to trigger data analysis and filtering jobs based on dynamic metadata.
- Designed a secure, HIPAA-compliant data perimeter by integrating VPC Service Controls, Cloud Key Management Service (KMS) for encryption at rest, and Cloud IAM for granular identity management.
- Built an extensible Business Logic Layer that allows non-technical users to submit Spark SQL queries, which are programmatically parsed and executed by a Spark-based engine to generate revenue-impacting insights.
- Maximized I/O throughput by utilizing Parquet for intermediate state storage, ensuring high-speed data persistence and retrieval during multi-stage transformation cycles.
- Automated machine learning workflows by building Vertex AI Pipelines to handle the data preparation, training, and deployment phases without manual intervention.
- Centralized feature management using Vertex AI Feature Store, allowing data science teams to reuse processed variables across different models to save time and compute.
- Monitored model health by setting up Vertex AI Model Monitoring to alert the team when data drift occurred, maintaining the accuracy of production insights.
- Engineered a notification mechanism in Cloud Composer (Airflow) to alert business teams in case of data discrepancies using Microsoft Teams Power Automate functionality.
- Established a robust Data Governance framework by implementing Row-Level Security (RLS) and Column-Level Access Control (via Policy Tags) to protect sensitive PII data.
- Developed a BigQuery Slot Monitoring dashboard to identify and refactor inefficient "heavy-hitter" queries, ensuring optimal reservation usage.

SKILLS:
- Cloud: AWS, GCP
- DevOps: CI/CD, Infrastructure as Code, Docker, Kubernetes
- Data: Python, SQL, Data Pipelines, ETL
- Data Engineering: Data Wearhousing, Dataflow, Dataproc, BigQuery, Cloud Storage, Cloud Composer, Airflow, Pub/Sub
- AI/ML: LLMs, Vertex AI
"""

# ==========================================
# 3. FILTERING RULES (THE GUARDRAILS)
# ==========================================
# If a job description lacks these, the agent scores it lower
MUST_HAVE_KEYWORDS = ["GCP", "Google Cloud", "Vertex", "AI", "ETL", "Data Ingestion", "Data Engineer", "Dataflow", "Airflow"]

# Instantly reject jobs with these keywords (saves AI processing time)
# E.g., skipping defense jobs since they require citizenship/clearances
EXCLUDE_KEYWORDS = ["Top Secret", "Clearance Required", "US Citizen Only", "Green Card Only"]

# ==========================================
# 4. SAFETY & STEALTH LIMITS (CRITICAL)
# ==========================================
# Do NOT increase these numbers dramatically. 
# LinkedIn will flag the account if it behaves too fast.
MAX_DAILY_APPLICATIONS = 2    # Start low to warm up the script
MAX_PAGE_SCROLLS = 3           # How deep to scroll on the search page
MIN_HUMAN_DELAY_SEC = 30        # Minimum wait time between clicks
MAX_HUMAN_DELAY_SEC = 90        # Maximum wait time between clicks

# ==========================================
# 5. LOCAL AI CONFIGURATION
# ==========================================
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434"