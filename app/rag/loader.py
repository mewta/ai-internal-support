from pypdf import PdfReader
from pathlib import Path

def load_text(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix == ".pdf":
        return _load_pdf(path)
    else:
        return _load_text(path)

def _load_pdf(path: Path) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)

def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")
