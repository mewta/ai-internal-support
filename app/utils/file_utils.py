import os

ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt"}

def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS
