"""
Defines the data model for displaying information about a PDF.
"""
from copy import copy
from typing import Dict, Union, List
from PyQt6.QtCore import QAbstractTableModel, Qt

from interfaces.desktop.exceptions.pdf_info_exceptions import (
    IncorrectPDFInfoModelDataLength,
)


class PDFInfoModel(QAbstractTableModel):
    """
    Data model to display information about PDF(s).
    """

    _mapping: Dict[int, str] = {
        0: "filename",
        1: "filepath",
        2: "pages_amount",
        3: "words_amount",
    }
    _type_mapping: Dict[str, type] = {
        "filename": str,
        "filepath": str,
        "pages_amount": int,
        "words_amount": int,
    }
    _pdfs_data: List[Dict[str, Union[int, str]]]

    def __init__(self, pdfs_data: List[Dict[str, Union[int, str]]]) -> None:
        """
        Validates and initializes the data.
        The data needs to be stored in a list of dict(s) that matches the mapping.
        The mapping is the following, assume key/value type:
            filename -> str(needs to correspond to a filename)
            filepath -> str(needs to correspond to a filepath)
            pages_amount -> int >= 0
            words_amount -> int >= 0

        Args:
            pdfs_data: The data representing the current PDF.
        """
        super().__init__()
        self._validate_data(pdfs_data)
        self._pdfs_data = pdfs_data

    def _validate_data(self, pdfs_data: List[Dict[str, Union[int, str]]]) -> None:
        """
        Validates the data matches the type mapping and that all data is correct.

        Args:
            pdfs_data: The data representing the current PDF.

        Raises:
            IncorrectPDFInfoModelDataLength: When the length of data is incorrect.
            KeyError: When the keys of the data do not match the mapping.
            TypeError: When the type of the values of the data do not match the mapping.
        """
        for pdf_data in pdfs_data:
            # check the length of the data
            if len(pdf_data) != len(self._type_mapping):
                raise IncorrectPDFInfoModelDataLength(pdf_data, len(self._type_mapping))

            # check that all needed keys are there
            pdf_data_keys = set(pdf_data.keys())
            correct_keys = set(self._type_mapping.keys())
            if pdf_data_keys != correct_keys:
                raise KeyError(
                    f"The provided keys in pdf_data {pdf_data_keys} do not match {correct_keys}"
                )

            # check the typing
            for key, data_point in pdf_data.items():
                if self._type_mapping[key] != type(data_point):
                    raise TypeError(
                        f"Expected {self._type_mapping[key]} but got {type(data_point)}"
                    )

    @classmethod
    def mapping(cls) -> dict[int, str]:
        """
        Returns:
            The mapping of the data model.
        """
        return copy(cls._mapping)

    @classmethod
    def type_mapping(cls) -> Dict[str, type]:
        """
        Returns:
            The type mapping of the data model.
        """
        return copy(cls._type_mapping)

    def rowCount(self, parent=...) -> int:
        """
        The amount rows are defined by how much PDFs are provided in the data.
        Args:
            parent: Useless in this case, there are no parents for this model
        Returns:
            The number of rows to display.
        """
        return len(self._pdfs_data)

    def columnCount(self, parent=...) -> int:
        """
        The mapping defines the number of columns, depending on how much data points
        need to be displayed.
        Args:
            parent: Useless in this case, there are no parents for this model

        Returns:
            The number of rows to display.
        """
        return len(self._mapping)

    def data(self, index, role=...) -> Union[str, int]:
        """

        Args:
            index: The index of the current table position.
            role: The role to the data

        Returns:
            The corresponding data to that index.
        """
        if not index.isValid():
            return ""

        row = index.row()
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._pdfs_data[row][self._mapping[column]]
