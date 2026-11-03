"""
CSE Aspirant - URL Phishing & Malicious Link Scanner
"""
import re
from typing import Tuple, Optional

class URLScanner:
    URL_REGEX = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\-.~:?#\[\]@!$&'()*+,;=]*")
    
    BLOCKED_DOMAINS = {
        "grabify.link", "iplogger.org", "2no.co", "blasze.com", "bit.ly/malicious-cse",
        "free-airdrop.xyz", "t.me/phishing_bot"
    }

    def scan_urls(self, text: str) -> Tuple[bool, Optional[str]]:
        matches = self.URL_REGEX.findall(text)
        for url in matches:
            for bad_domain in self.BLOCKED_DOMAINS:
                if bad_domain in url.lower():
                    return False, f"Malicious or suspicious domain detected: {bad_domain}"
        return True, None

url_scanner = URLScanner()

