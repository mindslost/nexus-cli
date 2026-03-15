import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

DB_PATH: Path = Path.home() / ".para_notes.db"


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """Context manager for SQLite database connections."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialize the SQLite database schema and FTS5 search index."""
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Core Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                para_category TEXT CHECK(para_category IN ('Project', 'Area', 'Resource', 'Archive')) NOT NULL,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Search Index (FTS5)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                title,
                content,
                tags,
                content='notes',
                content_rowid='rowid'
            )
        """)

        # 3. Auto-Sync Triggers
        # Trigger on INSERT
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
                INSERT INTO notes_fts(rowid, title, content, tags)
                VALUES (new.rowid, new.title, new.content, new.tags);
            END;
        """)

        # Trigger on DELETE
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, title, content, tags)
                VALUES('delete', old.rowid, old.title, old.content, old.tags);
            END;
        """)

        # Trigger on UPDATE
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, title, content, tags)
                VALUES('delete', old.rowid, old.title, old.content, old.tags);
                INSERT INTO notes_fts(rowid, title, content, tags)
                VALUES (new.rowid, new.title, new.content, new.tags);
            END;
        """)

        conn.commit()
