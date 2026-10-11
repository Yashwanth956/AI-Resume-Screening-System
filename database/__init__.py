"""Database package for the AI Resume Screening system."""

from .db_manager import (
    DEFAULT_DB_PATH,
    get_connection,
    init_db,
    save_analysis,
    get_analysis,
    list_analyses,
    delete_analysis,
)

__all__ = [
    "DEFAULT_DB_PATH",
    "get_connection",
    "init_db",
    "save_analysis",
    "get_analysis",
    "list_analyses",
    "delete_analysis",
]
