import fitz


def analyze_pdf(pdf_path):
    """
    Analyze a PDF and return useful metadata.

    Returns:
    {
        "pages": int,
        "is_text": bool,
        "is_scanned": bool,
        "title": str,
        "author": str
    }
    """

    pdf = fitz.open(pdf_path)

    pages = len(pdf)

    text_chars = 0

    metadata = pdf.metadata

    for page in pdf:

        text_chars += len(page.get_text().strip())

    pdf.close()

    return {

        "pages": pages,

        "is_text": text_chars > 30,

        "is_scanned": text_chars <= 30,

        "title": metadata.get("title", ""),

        "author": metadata.get("author", "")

    }


def is_text_pdf(pdf_path):

    return analyze_pdf(pdf_path)["is_text"]


def is_scanned_pdf(pdf_path):

    return analyze_pdf(pdf_path)["is_scanned"]