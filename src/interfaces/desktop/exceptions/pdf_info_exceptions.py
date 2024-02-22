"""
Exceptions specific to the PDFInfo Table View/Model.
"""
from typing import Dict, Union


class PDFInfoException(Exception):
    """
    General exception for all PDF info exceptions.
    All PDF Info related exceptions should inherit this exception.
    """


class IncorrectPDFInfoModelDataLength(Exception):
    """
    Raised when data passed to the data model is not of the correct length.
    """

    def __init__(self, pdf_data: Dict[str, Union[str, int]], correct_amount: int):
        super().__init__(
            f"There are {len(pdf_data)} data points but there should be {correct_amount}"
        )
