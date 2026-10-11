# database/db_manager.py
# ============================================================
# SQLITE STORAGE LAYER
# AI Resume Screening & Job Recommendation System
# ============================================================

from __future__ import annotations

import json
import sqlite3

from pathlib import Path
from typing import Any


# ============================================================
# DATABASE PATH
# ============================================================

DATABASE_DIR = Path(__file__).resolve().parent

DEFAULT_DB_PATH = (
    DATABASE_DIR
    / "resume_screening.db"
)


# ============================================================
# SQLITE CONNECTION THAT CLOSES AUTOMATICALLY
# ============================================================

class ClosingConnection(
    sqlite3.Connection
):
    """
    sqlite3's normal context manager commits/rolls back,
    but it does not always close the connection immediately.

    On Windows this can leave the database file locked.

    This subclass guarantees that:
        with get_connection(...) as conn:
            ...

    will commit/rollback AND close the connection.
    """

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        try:

            return super().__exit__(
                exc_type,
                exc_value,
                traceback
            )

        finally:

            self.close()


# ============================================================
# CONNECTION
# ============================================================

def get_connection(
    db_path: str | Path | None = None
) -> sqlite3.Connection:

    path = (
        Path(db_path)
        if db_path
        else DEFAULT_DB_PATH
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        path,
        factory=ClosingConnection
    )

    conn.row_factory = (
        sqlite3.Row
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# ============================================================
# DATABASE SCHEMA
# ============================================================

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_filename TEXT,
    candidate_name TEXT,
    email TEXT,
    phone TEXT,

    job_description TEXT,

    total_experience REAL DEFAULT 0,
    stated_experience REAL DEFAULT 0,
    calculated_experience REAL DEFAULT 0,

    ats_score REAL DEFAULT 0,
    skill_score REAL DEFAULT 0,
    keyword_score REAL DEFAULT 0,
    experience_score REAL DEFAULT 0,
    education_score REAL DEFAULT 0,
    project_score REAL DEFAULT 0,
    resume_quality_score REAL DEFAULT 0,

    experience_requirement_json TEXT,

    job_match_score REAL DEFAULT 0,
    match_category TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS resume_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    skill TEXT NOT NULL,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS job_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    skill TEXT NOT NULL,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS matching_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    skill TEXT NOT NULL,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS missing_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    skill TEXT NOT NULL,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS education_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    degree TEXT,
    institution TEXT,
    score TEXT,
    duration TEXT,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS experience_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    job_title TEXT,
    date_range TEXT,
    start_date TEXT,
    end_date TEXT,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    title TEXT,
    technologies_json TEXT,
    description_json TEXT,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_id INTEGER NOT NULL,

    rank_number INTEGER,
    role TEXT,
    score REAL DEFAULT 0,

    matched_count INTEGER DEFAULT 0,
    total_skills INTEGER DEFAULT 0,

    matching_skills_json TEXT,
    missing_skills_json TEXT,
    core_matches_json TEXT,

    FOREIGN KEY (analysis_id)
        REFERENCES analyses(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_analyses_email
    ON analyses(email);


CREATE INDEX IF NOT EXISTS idx_analyses_created_at
    ON analyses(created_at);


CREATE INDEX IF NOT EXISTS idx_resume_skills_analysis
    ON resume_skills(analysis_id);


CREATE INDEX IF NOT EXISTS idx_recommendations_analysis
    ON recommendations(analysis_id);
"""


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db(
    db_path: str | Path | None = None
) -> Path:

    path = (
        Path(db_path)
        if db_path
        else DEFAULT_DB_PATH
    )

    with get_connection(
        path
    ) as conn:

        conn.executescript(
            SCHEMA_SQL
        )

        conn.commit()

    return path


# ============================================================
# HELPERS
# ============================================================

def _json(
    value: Any
) -> str:

    if value is None:
        value = []

    return json.dumps(
        value,
        ensure_ascii=False,
        default=str
    )


def _number(
    value: Any,
    default: float = 0.0
) -> float:

    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def _integer(
    value: Any,
    default: int = 0
) -> int:

    try:

        return int(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def _clean_skill_list(
    values: Any
) -> list[str]:

    if not values:
        return []

    output = []
    seen = set()

    for value in values:

        skill = str(
            value
        ).strip()

        if not skill:
            continue

        key = (
            skill.lower()
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        output.append(
            skill
        )

    return output


# ============================================================
# SAVE COMPLETE ANALYSIS
# ============================================================

def save_analysis(
    *,
    resume_filename: str = "",
    candidate_name: str = "",
    email: str = "",
    phone: str = "",
    resume_skills: list[str] | None = None,
    education: list[dict] | None = None,
    experience: dict | None = None,
    projects: list[dict] | None = None,
    job_description: str = "",
    job_skills: list[str] | None = None,
    ats_result: dict | None = None,
    job_match_result: dict | None = None,
    recommended_roles: list[dict] | None = None,
    db_path: str | Path | None = None,
) -> int:

    """
    Store one complete resume analysis.

    Returns:
        analysis_id
    """

    init_db(
        db_path
    )

    resume_skills = _clean_skill_list(
        resume_skills
    )

    education = (
        education
        or []
    )

    experience = (
        experience
        or {}
    )

    projects = (
        projects
        or []
    )

    job_skills = _clean_skill_list(
        job_skills
    )

    ats_result = (
        ats_result
        or {}
    )

    job_match_result = (
        job_match_result
        or {}
    )

    recommended_roles = (
        recommended_roles
        or []
    )


    matching = _clean_skill_list(
        ats_result.get(
            "matching_skills",
            []
        )
    )


    missing = _clean_skill_list(
        ats_result.get(
            "missing_skills",
            []
        )
    )


    experience_requirement = (
        ats_result.get(
            "experience_requirement",
            {}
        )
        or {}
    )


    total_experience = _number(
        experience.get(
            "total_years",
            0
        )
    )


    stated_experience = _number(
        experience.get(
            "stated_years",
            0
        )
    )


    calculated_experience = _number(
        experience.get(
            "calculated_years",
            0
        )
    )


    with get_connection(
        db_path
    ) as conn:

        cursor = conn.cursor()


        # ====================================================
        # MAIN ANALYSIS RECORD
        # ====================================================

        cursor.execute(
            """
            INSERT INTO analyses (
                resume_filename,
                candidate_name,
                email,
                phone,
                job_description,

                total_experience,
                stated_experience,
                calculated_experience,

                ats_score,
                skill_score,
                keyword_score,
                experience_score,
                education_score,
                project_score,
                resume_quality_score,

                experience_requirement_json,

                job_match_score,
                match_category
            )

            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?,
                ?,
                ?, ?
            )
            """,
            (
                str(
                    resume_filename
                    or ""
                ),

                str(
                    candidate_name
                    or ""
                ),

                str(
                    email
                    or ""
                ),

                str(
                    phone
                    or ""
                ),

                str(
                    job_description
                    or ""
                ),

                total_experience,

                stated_experience,

                calculated_experience,

                _number(
                    ats_result.get(
                        "score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "skill_score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "keyword_score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "experience_score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "education_score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "project_score",
                        0
                    )
                ),

                _number(
                    ats_result.get(
                        "resume_quality_score",
                        0
                    )
                ),

                _json(
                    experience_requirement
                ),

                _number(
                    job_match_result.get(
                        "match_score",
                        0
                    )
                ),

                str(
                    job_match_result.get(
                        "match_category",
                        ""
                    )
                    or ""
                ),
            ),
        )


        analysis_id = (
            cursor.lastrowid
        )


        # ====================================================
        # RESUME SKILLS
        # ====================================================

        cursor.executemany(
            """
            INSERT INTO resume_skills (
                analysis_id,
                skill
            )
            VALUES (?, ?)
            """,
            [
                (
                    analysis_id,
                    skill
                )
                for skill in resume_skills
            ],
        )


        # ====================================================
        # JOB SKILLS
        # ====================================================

        cursor.executemany(
            """
            INSERT INTO job_skills (
                analysis_id,
                skill
            )
            VALUES (?, ?)
            """,
            [
                (
                    analysis_id,
                    skill
                )
                for skill in job_skills
            ],
        )


        # ====================================================
        # MATCHING SKILLS
        # ====================================================

        cursor.executemany(
            """
            INSERT INTO matching_skills (
                analysis_id,
                skill
            )
            VALUES (?, ?)
            """,
            [
                (
                    analysis_id,
                    skill
                )
                for skill in matching
            ],
        )


        # ====================================================
        # MISSING SKILLS
        # ====================================================

        cursor.executemany(
            """
            INSERT INTO missing_skills (
                analysis_id,
                skill
            )
            VALUES (?, ?)
            """,
            [
                (
                    analysis_id,
                    skill
                )
                for skill in missing
            ],
        )


        # ====================================================
        # EDUCATION
        # ====================================================

        for item in education:

            if not isinstance(
                item,
                dict
            ):
                continue


            cursor.execute(
                """
                INSERT INTO education_records (
                    analysis_id,
                    degree,
                    institution,
                    score,
                    duration
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    analysis_id,

                    str(
                        item.get(
                            "degree",
                            ""
                        )
                        or ""
                    ),

                    str(
                        item.get(
                            "institution",
                            ""
                        )
                        or ""
                    ),

                    str(
                        item.get(
                            "score",
                            ""
                        )
                        or ""
                    ),

                    str(
                        item.get(
                            "duration",
                            ""
                        )
                        or ""
                    ),
                ),
            )


        # ====================================================
        # EXPERIENCE RECORDS
        # ====================================================

        records = (
            experience.get(
                "records",
                []
            )
            or []
        )


        for record in records:

            if not isinstance(
                record,
                dict
            ):
                continue


            cursor.execute(
                """
                INSERT INTO experience_records (
                    analysis_id,
                    job_title,
                    date_range,
                    start_date,
                    end_date
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    analysis_id,

                    str(
                        record.get(
                            "job_title",
                            ""
                        )
                        or ""
                    ),

                    str(
                        record.get(
                            "date_range",
                            ""
                        )
                        or ""
                    ),

                    str(
                        record.get(
                            "start",
                            ""
                        )
                        or ""
                    ),

                    str(
                        record.get(
                            "end",
                            ""
                        )
                        or ""
                    ),
                ),
            )


        # ====================================================
        # PROJECTS
        # ====================================================

        for project in projects:

            if not isinstance(
                project,
                dict
            ):
                continue


            title = (
                project.get(
                    "title"
                )
                or project.get(
                    "name"
                )
                or ""
            )


            technologies = (
                project.get(
                    "technologies"
                )
                or project.get(
                    "tech_stack"
                )
                or []
            )


            description = (
                project.get(
                    "description"
                )
                or []
            )


            if isinstance(
                description,
                str
            ):

                description = [
                    description
                ]


            cursor.execute(
                """
                INSERT INTO projects (
                    analysis_id,
                    title,
                    technologies_json,
                    description_json
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    analysis_id,

                    str(
                        title
                    ),

                    _json(
                        technologies
                    ),

                    _json(
                        description
                    ),
                ),
            )


        # ====================================================
        # JOB ROLE RECOMMENDATIONS
        # ====================================================

        for rank, role_item in enumerate(
            recommended_roles,
            start=1
        ):

            if not isinstance(
                role_item,
                dict
            ):
                continue


            cursor.execute(
                """
                INSERT INTO recommendations (
                    analysis_id,
                    rank_number,
                    role,
                    score,
                    matched_count,
                    total_skills,
                    matching_skills_json,
                    missing_skills_json,
                    core_matches_json
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    analysis_id,

                    rank,

                    str(
                        role_item.get(
                            "role",
                            ""
                        )
                        or ""
                    ),

                    _number(
                        role_item.get(
                            "score",
                            0
                        )
                    ),

                    _integer(
                        role_item.get(
                            "matched_count",
                            0
                        )
                    ),

                    _integer(
                        role_item.get(
                            "total_skills",
                            0
                        )
                    ),

                    _json(
                        role_item.get(
                            "matching_skills",
                            []
                        )
                    ),

                    _json(
                        role_item.get(
                            "missing_skills",
                            []
                        )
                    ),

                    _json(
                        role_item.get(
                            "core_matches",
                            []
                        )
                    ),
                ),
            )


        conn.commit()


    return int(
        analysis_id
    )


# ============================================================
# READ ONE ANALYSIS
# ============================================================

def get_analysis(
    analysis_id: int,
    db_path: str | Path | None = None
) -> dict | None:


    with get_connection(
        db_path
    ) as conn:


        analysis = conn.execute(
            """
            SELECT *
            FROM analyses
            WHERE id = ?
            """,
            (
                analysis_id,
            ),
        ).fetchone()


        if analysis is None:
            return None


        result = dict(
            analysis
        )


        result[
            "experience_requirement"
        ] = json.loads(
            result.pop(
                "experience_requirement_json",
                "{}"
            )
            or "{}"
        )


        # ====================================================
        # SKILL TABLE HELPER
        # ====================================================

        def fetch_skills(
            table_name: str
        ) -> list[str]:

            allowed_tables = {
                "resume_skills",
                "job_skills",
                "matching_skills",
                "missing_skills",
            }

            if table_name not in allowed_tables:
                raise ValueError(
                    "Invalid skill table."
                )


            rows = conn.execute(
                f"""
                SELECT skill
                FROM {table_name}
                WHERE analysis_id = ?
                ORDER BY id
                """,
                (
                    analysis_id,
                ),
            ).fetchall()


            return [
                row["skill"]
                for row in rows
            ]


        result[
            "resume_skills"
        ] = fetch_skills(
            "resume_skills"
        )


        result[
            "job_skills"
        ] = fetch_skills(
            "job_skills"
        )


        result[
            "matching_skills"
        ] = fetch_skills(
            "matching_skills"
        )


        result[
            "missing_skills"
        ] = fetch_skills(
            "missing_skills"
        )


        # ====================================================
        # EDUCATION
        # ====================================================

        result[
            "education"
        ] = [
            dict(
                row
            )
            for row in conn.execute(
                """
                SELECT
                    degree,
                    institution,
                    score,
                    duration
                FROM education_records
                WHERE analysis_id = ?
                ORDER BY id
                """,
                (
                    analysis_id,
                ),
            ).fetchall()
        ]


        # ====================================================
        # EXPERIENCE
        # ====================================================

        result[
            "experience_records"
        ] = [
            dict(
                row
            )
            for row in conn.execute(
                """
                SELECT
                    job_title,
                    date_range,
                    start_date,
                    end_date
                FROM experience_records
                WHERE analysis_id = ?
                ORDER BY id
                """,
                (
                    analysis_id,
                ),
            ).fetchall()
        ]


        # ====================================================
        # PROJECTS
        # ====================================================

        project_rows = conn.execute(
            """
            SELECT
                title,
                technologies_json,
                description_json
            FROM projects
            WHERE analysis_id = ?
            ORDER BY id
            """,
            (
                analysis_id,
            ),
        ).fetchall()


        result[
            "projects"
        ] = []


        for row in project_rows:

            result[
                "projects"
            ].append(
                {
                    "title":
                        row["title"],

                    "technologies":
                        json.loads(
                            row[
                                "technologies_json"
                            ]
                            or "[]"
                        ),

                    "description":
                        json.loads(
                            row[
                                "description_json"
                            ]
                            or "[]"
                        ),
                }
            )


        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        recommendation_rows = (
            conn.execute(
                """
                SELECT
                    rank_number,
                    role,
                    score,
                    matched_count,
                    total_skills,
                    matching_skills_json,
                    missing_skills_json,
                    core_matches_json

                FROM recommendations

                WHERE analysis_id = ?

                ORDER BY
                    rank_number,
                    id
                """,
                (
                    analysis_id,
                ),
            ).fetchall()
        )


        result[
            "recommended_roles"
        ] = []


        for row in recommendation_rows:

            result[
                "recommended_roles"
            ].append(
                {
                    "rank":
                        row[
                            "rank_number"
                        ],

                    "role":
                        row[
                            "role"
                        ],

                    "score":
                        row[
                            "score"
                        ],

                    "matched_count":
                        row[
                            "matched_count"
                        ],

                    "total_skills":
                        row[
                            "total_skills"
                        ],

                    "matching_skills":
                        json.loads(
                            row[
                                "matching_skills_json"
                            ]
                            or "[]"
                        ),

                    "missing_skills":
                        json.loads(
                            row[
                                "missing_skills_json"
                            ]
                            or "[]"
                        ),

                    "core_matches":
                        json.loads(
                            row[
                                "core_matches_json"
                            ]
                            or "[]"
                        ),
                }
            )


        return result


# ============================================================
# LIST ANALYSES
# ============================================================

def list_analyses(
    limit: int = 50,
    db_path: str | Path | None = None
) -> list[dict]:


    limit = max(
        1,
        min(
            _integer(
                limit,
                50
            ),
            500
        )
    )


    with get_connection(
        db_path
    ) as conn:


        rows = conn.execute(
            """
            SELECT
                id,
                resume_filename,
                candidate_name,
                email,
                total_experience,
                ats_score,
                job_match_score,
                match_category,
                created_at

            FROM analyses

            ORDER BY id DESC

            LIMIT ?
            """,
            (
                limit,
            ),
        ).fetchall()


        return [
            dict(
                row
            )
            for row in rows
        ]


# ============================================================
# DELETE ANALYSIS
# ============================================================

def delete_analysis(
    analysis_id: int,
    db_path: str | Path | None = None
) -> bool:


    with get_connection(
        db_path
    ) as conn:


        cursor = conn.execute(
            """
            DELETE FROM analyses
            WHERE id = ?
            """,
            (
                analysis_id,
            ),
        )


        conn.commit()


        return (
            cursor.rowcount
            > 0
        )
