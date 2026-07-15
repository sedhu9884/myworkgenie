import os
import uuid
from PyPDF2 import PdfMerger
from pypdf import PdfWriter, PdfReader

OUTPUT_FOLDER = "outputs"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def merge_pdfs(files):

    output_path = os.path.join(

        OUTPUT_FOLDER,

        f"merged_{uuid.uuid4().hex}.pdf"

    )

    merger = PdfMerger()

    try:

        for pdf in files:

            merger.append(pdf)

        merger.write(output_path)

        merger.close()

        return output_path

    except Exception:

        merger.close()

        raise