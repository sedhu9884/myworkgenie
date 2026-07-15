import os
from docx2pdf import convert

OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_word_to_pdf(input_path, original_name):

    output_path = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".pdf"
    )

    convert(
        input_path,
        output_path
    )

    return output_path