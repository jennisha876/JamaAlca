import os
import shutil
import uuid
from datetime import datetime

try:
    import pyodbc
    _PYODBC_AVAILABLE = True
except Exception:
    pyodbc = None
    _PYODBC_AVAILABLE = False


class ScanStore:
    """Simple scan persistence helper.

    - Saves an image copy under ./scans/<uuid><ext>
    - Attempts to insert a metadata row into Azure SQL when AZURE_SQL_CONN env var is set and pyodbc is available
    """

    def __init__(self, scans_dir=None, db_helper=None):
        self.scans_dir = scans_dir or os.path.join(os.getcwd(), "scans")
        os.makedirs(self.scans_dir, exist_ok=True)
        # Optional DB helper (db.DBHelper instance)
        self.db_helper = db_helper

    def _save_image_copy(self, src_path):
        try:
            ext = os.path.splitext(src_path)[1] or ".jpg"
            filename = f"{uuid.uuid4().hex}{ext}"
            dst = os.path.join(self.scans_dir, filename)
            shutil.copyfile(src_path, dst)
            return dst
        except Exception as e:
            print("[ScanStore] failed to save image copy:", e)
            return src_path

    def _insert_sql(self, rec):
        if self.db_helper:
            try:
                return self.db_helper.insert_scan(rec)
            except Exception as e:
                print("[ScanStore] db_helper.insert_scan failed:", e)
                return False
        # No DB helper available, and no internal connection
        return False

    def save_scan(self, image_path, crop, disease, confidence, treatment_text, user_id=0):
        """Save a scan. Returns a dict with saved metadata.

        image_path: source image path
        crop: crop name
        disease: disease string or 'Healthy'
        confidence: numeric
        treatment_text: free text (can be multiline)
        user_id: int
        """
        saved_image = self._save_image_copy(image_path)
        rec = {
            "id": uuid.uuid4().hex,
            "user_id": int(user_id) if user_id is not None else 0,
            "crop": crop,
            "disease": disease,
            "confidence": float(confidence),
            "treatment": treatment_text,
            "image_path": saved_image,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        persisted = self._insert_sql(rec)
        rec["persisted_to_sql"] = bool(persisted)
        return rec
