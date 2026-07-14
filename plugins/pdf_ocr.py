import pytesseract

from pdf2image import convert_from_path


def extract_text_ocr(pdf_path):

    pages = convert_from_path(

        pdf_path,

        dpi=300

    )

    output = []

    for page in pages:

        text = pytesseract.image_to_string(

            page,

            lang="eng"

        )

        output.append(text)

    return "\n".join(output)