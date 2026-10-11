# database/init_db.py

from database.db_manager import init_db, DEFAULT_DB_PATH


def main():
    path = init_db()

    print("=" * 60)
    print("DATABASE INITIALIZED")
    print("=" * 60)
    print("Database:", path)
    print("Status: READY")


if __name__ == "__main__":
    main()
