from pathlib import Path
import sys


# Make the src directory importable
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from resume_critiquer.resume_parser import extract_text


# Resume PDF
pdf_path = PROJECT_ROOT / "sample_resume.pdf"

if not pdf_path.exists():
    raise FileNotFoundError(
        f"Could not find resume PDF: {pdf_path}"
    )


# Read PDF
pdf_bytes = pdf_path.read_bytes()


# Extract text
text = extract_text(pdf_bytes)


print("\n===== EXTRACTED RESUME TEXT =====\n")

if text:
    print(text[:3000])
else:
    print("No readable text was extracted from the PDF.")