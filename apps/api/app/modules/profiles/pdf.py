from io import BytesIO

from fastapi import HTTPException
from pypdf import PdfReader

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_PAGES = 20
MAX_TEXT_CHARS = 30000


def extract_pdf(data: bytes) -> tuple[str, int, bool]:
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Arquivo não é um PDF válido.")
    try:
        reader = PdfReader(BytesIO(data), strict=True)
        if reader.is_encrypted:
            raise HTTPException(status_code=400, detail="PDF protegido por senha não é aceito.")
        pages = len(reader.pages)
        if pages < 1 or pages > MAX_PAGES:
            raise HTTPException(status_code=400, detail="O PDF deve ter entre 1 e 20 páginas.")
        chunks = []
        total = 0
        truncated = False
        for page in reader.pages:
            part = page.extract_text() or ""
            if total + len(part) > MAX_TEXT_CHARS:
                part = part[: MAX_TEXT_CHARS - total]
                truncated = True
            chunks.append(part)
            total += len(part)
            if truncated:
                break
        text = "\n".join(chunks).strip()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Não foi possível ler o PDF.") from exc
    if not text:
        raise HTTPException(
            status_code=422,
            detail="PDF sem texto selecionável. Currículos digitalizados precisam de OCR.",
        )
    return text, pages, truncated
