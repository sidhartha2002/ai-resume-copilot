from io import BytesIO

from pypdf import PdfReader


def extract_text(pdf_bytes: bytes) -> str:
    """
    Extract text from a text-based PDF.
    """

    reader = PdfReader(BytesIO(pdf_bytes))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()