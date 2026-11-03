"""
CSE Aspirant - Suspicious File & Payload Scanner
"""
from typing import Tuple, Optional
import os

class FileScanner:
    DANGEROUS_EXTENSIONS = {
        ".exe", ".bat", ".cmd", ".sh", ".vbs", ".ps1", ".scr", ".pif", ".apk", ".dll", ".so"
    }

    def inspect_file(self, filename: str, mime_type: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        if not filename:
            return True, None
        
        _, ext = os.path.splitext(filename.lower())
        if ext in self.DANGEROUS_EXTENSIONS:
            return False, f"Potentially malicious executable file rejected: {ext}"

        if mime_type and ("application/x-msdos-program" in mime_type or "application/x-executable" in mime_type):
            return False, "Dangerous binary MIME type detected"

        return True, None

file_scanner = FileScanner()

