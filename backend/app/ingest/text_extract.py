"""Pluggable text extraction for uploaded company docs."""
from __future__ import annotations

import io
from typing import Optional


def extract_text(raw: bytes, mime_type: str, filename: str = "") -> str:
    if mime_type == "application/pdf":
        return _pdf(raw)
    if mime_type == ("application/vnd.openxmlformats-officedocument."
                      "wordprocessingml.document"):
        return _docx(raw)
    if mime_type in ("text/plain", "text/markdown", "text/csv"):
        return raw.decode("utf-8", errors="replace")
    if mime_type.startswith("image/"):
        return _ocr(raw, mime_type)
    if mime_type == "text/url":
        # Caller resolves URLs via fetch_link; this branch is unused.
        return ""
    raise ValueError(f"unsupported mime type {mime_type}")


def _pdf(raw: bytes) -> str:
    try:
        import pdfplumber
    except ImportError:
        return ""
    parts = []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n\n".join(parts)


def _docx(raw: bytes) -> str:
    try:
        from docx import Document
    except ImportError:
        return ""
    doc = Document(io.BytesIO(raw))
    return "\n".join(p.text for p in doc.paragraphs)


def _ocr(raw: bytes, mime_type: str) -> str:
    """Optional. Falls back gracefully if tesseract not installed."""
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        return ""
    img = Image.open(io.BytesIO(raw))
    try:
        return pytesseract.image_to_string(img)
    except Exception:
        return ""
