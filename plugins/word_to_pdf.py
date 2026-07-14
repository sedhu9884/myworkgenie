import os
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_word_to_pdf(docx_path, original_name):

    output_path = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".pdf"
    )

    system = platform.system()

    try:

        logger.info("Starting Word → PDF conversion")

        if system == "Windows":

            from docx2pdf import convert

            convert(docx_path, output_path)

        else:

            subprocess.run(

                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    OUTPUT_FOLDER,
                    docx_path
                ],

                check=True

            )

        logger.info("Conversion completed")

        return output_path

    except Exception as ex:

        logger.exception(ex)

        raise Exception(
            "Unable to convert Word document."
        )