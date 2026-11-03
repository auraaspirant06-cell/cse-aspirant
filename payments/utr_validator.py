"""
CSE Aspirant - UTR & Transaction ID Validation
"""
import re

class UTRValidator:
    # Standard Indian Banking UTRs are 12 alphanumeric/numeric characters
    UTR_REGEX = re.compile(r"^[A-Z0-9]{10,22}$")

    @classmethod
    def validate(cls, utr: str) -> bool:
        if not utr:
            return False
        clean_utr = utr.strip().upper()
        return bool(cls.UTR_REGEX.match(clean_utr))

utr_validator = UTRValidator()

