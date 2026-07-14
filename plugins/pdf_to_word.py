import os
import logging

import fitz

from docx import Document

from plugins.pdf_detector import analyze_pdf
from plugins.pdf_ocr import extract_text_ocr

logger = logging.getLogger(__name__)

OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_pdf_to_word(pdf_path, original_name):

    info = analyze_pdf(pdf_path)

    output = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".docx"
    )

    document = Document()

    document.core_properties.title = info["title"]

    document.core_properties.author = info["author"]

    pdf = fitz.open(pdf_path)

    try:

        if info["is_text"]:

            logger.info("Text PDF detected")

            for page in pdf:

                text = page.get_text()

                if text.strip():

                    document.add_paragraph(text)

        else:

            logger.info("OCR PDF detected")

            text = extract_text_ocr(pdf_path)

            for paragraph in text.split("\n"):

                if paragraph.strip():

                    document.add_paragraph(paragraph)

        document.save(output)

        logger.info("DOCX created")

        return output

    finally:

        pdf.close()