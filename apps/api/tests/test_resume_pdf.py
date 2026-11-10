from io import BytesIO

import pytest
from fastapi import HTTPException
from pypdf import PdfWriter

from app.modules.profiles.pdf import extract_pdf


def test_rejects_non_pdf():
    with pytest.raises(HTTPException) as exc:
        extract_pdf(b"not a pdf")
    assert exc.value.status_code == 400


def test_rejects_empty_pdf():
    stream = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(stream)
    with pytest.raises(HTTPException) as exc:
        extract_pdf(stream.getvalue())
    assert exc.value.status_code == 422


def test_rejects_too_many_pages():
    stream = BytesIO()
    writer = PdfWriter()
    for _ in range(21):
        writer.add_blank_page(width=200, height=200)
    writer.write(stream)
    with pytest.raises(HTTPException) as exc:
        extract_pdf(stream.getvalue())
    assert exc.value.status_code == 400
