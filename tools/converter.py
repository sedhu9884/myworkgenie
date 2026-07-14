from plugins.pdf_to_word import convert_pdf_to_word
from plugins.word_to_pdf import convert_word_to_pdf


def convert(tool, input_path, original_name):

    if tool == "pdf_to_word":
        return convert_pdf_to_word(input_path, original_name)

    elif tool == "word_to_pdf":
        return convert_word_to_pdf(input_path, original_name)

    else:
        raise Exception("Unsupported conversion tool.")