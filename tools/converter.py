from plugins.pdf_to_word import convert_pdf_to_word
from plugins.word_to_pdf import convert_word_to_pdf


SUPPORTED_TOOLS = {

    "pdf_to_word": convert_pdf_to_word,

    "word_to_pdf": convert_word_to_pdf

}


def convert(

    tool,

    input_path,

    original_name

):

    """
    Calls the appropriate converter plugin.

    Parameters
    ----------
    tool : str
    input_path : str
    original_name : str

    Returns
    -------
    str
        Converted file path.
    """

    if tool not in SUPPORTED_TOOLS:

        raise Exception(

            "Unsupported conversion selected."

        )

    converter = SUPPORTED_TOOLS[tool]

    return converter(

        input_path,

        original_name

    )