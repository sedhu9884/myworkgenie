import os
import logging
import fitz
from docx import Document

logger = logging.getLogger(__name__)

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_pdf_to_word(pdf_path, original_name):
    """
    Convert text-based PDF to Word.
    """

    output_path = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".docx"
    )

    pdf = fitz.open(pdf_path)

    document = Document()

    try:

        document.add_heading(original_name, level=1)

        for page in pdf:

            text = page.get_text("text")

            if text.strip():

                document.add_paragraph(text)

        document.save(output_path)

        logger.info("PDF converted successfully")

        return output_path

    except Exception as ex:

        logger.exception(ex)

        raise Exception(
            "Unable to convert PDF."
        )

    finally:

        pdf.close()