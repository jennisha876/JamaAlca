import os
import uuid
from datetime import datetime

try:
    import pyodbc
    _PYODBC = True
except Exception:
    pyodbc = None
    _PYODBC = False


class DBHelper:
    """Simple DB helper for Azure SQL using pyodbc.

    Methods:
      - connect() : lazily connects when needed
      - upsert_user(profile_dict) -> returns user_id (int) or None
      - insert_scan(scan_record) -> returns True/False
    """

    def __init__(self, conn_str=None):
        self.conn_str = conn_str or os.environ.get("AZURE_SQL_CONN")
        self._conn = None

    def connect(self):
        if self._conn:
            return self._conn
        if not _PYODBC or not self.conn_str:
            return None
        try:
            self._conn = pyodbc.connect(self.conn_str, autocommit=True)
            return self._conn
        except Exception as e:
            print("[DBHelper] connection error:", e)
            self._conn = None
            return None

    def upsert_user(self, profile):
        """Upsert a user row from profile. Returns user_id if available.

        Expects a table `Users` with columns (id INT IDENTITY or INT PK, name, phone, location, farm_size, main_crop)
        If the Users table uses an auto-increment integer key, this will try to find a matching phone and return its id,
        otherwise insert a new user and return the newly created id (if obtainable).
        """
        conn = self.connect()
        if not conn:
            return None
        try:
            cur = conn.cursor()
            # Try find by phone
            phone = profile.get("phone")
            if phone:
                cur.execute("SELECT id FROM Users WHERE phone = ?", phone)
                row = cur.fetchone()
                if row:
                    uid = row[0]
                    # Optionally update details
                    cur.execute("UPDATE Users SET name = ?, location = ?, farm_size = ?, main_crop = ? WHERE id = ?",
                                profile.get("name"), profile.get("location"), profile.get("farm_size"), profile.get("main_crop"), uid)
                    return uid

            # Insert new user
            cur.execute("INSERT INTO Users (name, phone, location, farm_size, main_crop) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)",
                        profile.get("name"), profile.get("phone"), profile.get("location"), profile.get("farm_size"), profile.get("main_crop"))
            # FETCH inserted id
            try:
                new_id = cur.fetchone()[0]
            except Exception:
                new_id = None
            return new_id
        except Exception as e:
            print("[DBHelper] upsert_user failed:", e)
            return None

    def insert_scan(self, rec):
        """Insert a scan record. Expects rec dict with keys matching Scans table."""
        conn = self.connect()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            sql = (
                "INSERT INTO Scans (id, user_id, crop, disease, confidence, treatment, image_path, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            cur.execute(sql, rec["id"], rec["user_id"], rec["crop"], rec["disease"], float(rec["confidence"]), rec["treatment"], rec["image_path"], rec["created_at"]) 
            return True
        except Exception as e:
            print("[DBHelper] insert_scan failed:", e)
            return False
