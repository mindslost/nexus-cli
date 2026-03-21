"""
Database management for the Ostraca CLI.

This module handles SQLite database connections, schema initialization,
and Full-Text Search (FTS5) index synchronization using triggers.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator, List

# Database file is stored in the user's home directory
DB_PATH: Path = Path.home() / ".para_notes.db"

# Valid PARA categories enforced by both Python and SQL CHECK constraints
PARA_CATEGORIES: List[str] = ["Project", "Area", "Resource", "Archive"]


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """
    Provide a transactional scope around a series of database operations.

    Yields:
        A sqlite3.Connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """
    Initialize the SQLite database schema and FTS5 search index.

    Creates the 'notes' table with PARA category constraints,
    sets up the 'notes_fts' virtual table for searching,
    and installs triggers to keep the search index in sync.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Core Table: Stores the source of truth for all notes
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

        # 2. Search Index (FTS5): External content table for high-performance searching
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                title,
                content,
                tags,
                content='notes',
                content_rowid='rowid'
            )
        """)

        # 3. Auto-Sync Triggers: Ensure 'notes_fts' stays updated as 'notes' changes

        # Trigger on INSERT: Add new records to the FTS index
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
                INSERT INTO notes_fts(rowid, title, content, tags)
                VALUES (new.rowid, new.title, new.content, new.tags);
            END;
        """)

        # Trigger on DELETE: Remove records from the FTS index
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, title, content, tags)
                VALUES('delete', old.rowid, old.title, old.content, old.tags);
            END;
        """)

        # Trigger on UPDATE: Refresh records in the FTS index
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, title, content, tags)
                VALUES('delete', old.rowid, old.title, old.content, old.tags);
                INSERT INTO notes_fts(rowid, title, content, tags)
                VALUES (new.rowid, new.title, new.content, new.tags);
            END;
        """)
        conn.commit()
