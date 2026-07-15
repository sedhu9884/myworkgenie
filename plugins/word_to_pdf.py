import os
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

OUTPUT_FOLDER = "outputs"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def windows_convert(
    input_file,
    output_file
):

    from docx2pdf import convert

    convert(
        input_file,
        output_file
    )


def linux_convert(
    input_file
):

    subprocess.run(

        [

            "libreoffice",

            "--headless",

            "--convert-to",

            "pdf",

            "--outdir",

            OUTPUT_FOLDER,

            input_file

        ],

        check=True

    )


def get_output_path(
    original_name
):

    return os.path.join(

        OUTPUT_FOLDER,

        original_name + ".pdf"

    )

def convert_word_to_pdf(

    input_path,

    original_name

):

    output_path = get_output_path(

        original_name

    )

    system = platform.system().lower()

    logger.info(

        f"Operating System : {system}"

    )

    try:

        if system == "windows":

            windows_convert(

                input_path,

                output_path

            )

        else:

            linux_convert(

                input_path

            )

            generated = os.path.join(

                OUTPUT_FOLDER,

                os.path.splitext(

                    os.path.basename(input_path)

                )[0] + ".pdf"

            )

            if generated != output_path and os.path.exists(generated):

                os.replace(

                    generated,

                    output_path

                )

            if not os.path.exists(output_path):

                raise Exception(

                    "PDF was not generated."

                )

        logger.info(

            "Word converted successfully."

        )

        return output_path

    except Exception as ex:

        logger.exception(ex)

        raise Exception(

            f"Word to PDF conversion failed: {str(ex)}"

        )                