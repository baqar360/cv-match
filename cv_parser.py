"""Extract text from uploaded CV files."""
import fitz  # PyMuPDF


def extract_text_from_pdf(file):
    """Accepts a file path, bytes, or a file-like object (e.g. a Streamlit upload)."""
    try:
        if isinstance(file, str):
            doc = fitz.open(file)
        else:
            data = file if isinstance(file, bytes) else file.read()
            doc = fitz.open(stream=data, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    except Exception as e:
        raise ValueError(f"Could not read the PDF: {e}")

    if not text.strip():
        raise ValueError("No readable text found. The PDF may be a scanned image.")
    return text.strip()