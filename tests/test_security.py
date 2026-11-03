"""
Unit Tests for Security, Anti-Spam, Content Filtering & Scanners
"""
import pytest
from security.anti_flood import anti_flood
from security.anti_spam import anti_spam
from security.content_filter import content_moderator
from security.url_scanner import url_scanner
from security.file_scanner import file_scanner
from security.audit import audit_logger

def test_anti_flood_sliding_window():
    user_id = 1001
    anti_flood.reset(user_id)

    # Sending 5 messages within window should be fine
    for _ in range(5):
        assert anti_flood.is_flooding(user_id) is False

    # 6th message exceeds burst limit
    assert anti_flood.is_flooding(user_id) is True

def test_anti_spam_duplicate_detection():
    user_id = 2002
    text = "Join my free telegram crypto pump channel now!"

    assert anti_spam.is_spam(user_id, text) is False
    assert anti_spam.is_spam(user_id, text) is False
    assert anti_spam.is_spam(user_id, text) is False
    # 4th repeated text is flagged as spam
    assert anti_spam.is_spam(user_id, text) is True

def test_content_moderation():
    ok, _ = content_moderator.inspect_text("Hello let us study operating systems and algorithms.")
    assert ok is True

    bad, reason = content_moderator.inspect_text("Check this out porn free access")
    assert bad is False
    assert "explicit content detected" in reason

def test_url_security_scanner():
    safe, _ = url_scanner.scan_urls("Visit our academy at https://cse-aspirant.org/courses")
    assert safe is True

    malicious, reason = url_scanner.scan_urls("Click here http://grabify.link/track-user")
    assert malicious is False
    assert "Malicious" in reason

def test_file_scanner():
    safe, _ = file_scanner.inspect_file("upsc_syllabus.pdf")
    assert safe is True

    danger, reason = file_scanner.inspect_file("malicious_trojan.exe")
    assert danger is False
    assert "malicious executable" in reason

def test_audit_logging():
    audit_logger.log("MEMBER_WARNED", actor_id=1, target_id=2, details="Spamming")
    logs = audit_logger.get_logs(5)
    assert len(logs) >= 1
    assert logs[-1]["action"] == "MEMBER_WARNED"

