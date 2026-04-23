import sqlite3
import datetime

class SynapticMemory:
    def __init__(self, db_path="christin_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                role TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def add_interaction(self, role, content):
        """Adds a user or assistant message to memory."""
        timestamp = datetime.datetime.now()
        self.cursor.execute(
            "INSERT INTO interactions (timestamp, role, content) VALUES (?, ?, ?)",
            (timestamp, role, content)
        )
        self.conn.commit()

    def get_recent_context(self, limit=10):
        """Retrieves the last N interactions as a formatted string."""
        self.cursor.execute(
            "SELECT role, content FROM interactions ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = self.cursor.fetchall()
        # Reverse to get chronological order
        rows.reverse()
        
        context = ""
        for role, content in rows:
            context += f"{role.capitalize()}: {content}\n"
        return context

    def clear_memory(self):
        self.cursor.execute("DELETE FROM interactions")
        self.conn.commit()

# Global instance
memory = SynapticMemory()
