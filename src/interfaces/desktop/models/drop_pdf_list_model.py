"""
Model to populate a view that accepts PDFs drops and displays them.
"""
import os

from PyQt6.QtCore import QAbstractListModel, QUrl, Qt
from typing import List, Union

PDF_EXTENSION = ".pdf"


class DropPDFListModel(QAbstractListModel):
    """
    The responsibility of the model is to hold data of the PDFs' url
    provided by the user.
    """

    _pdfs_data: List[QUrl]

    def __init__(self, data=None, parent=None) -> None:
        """
        Initializes the model with the data if it is provided.
        Else, it creates an empty list.

        Args:
            data:
            parent:
        """
        super().__init__(parent)
        self._pdfs_data = list() if data is None else data

    def rowCount(self, parent=...) -> int:
        """
        The amount rows are defined by how much PDFs are provided in the data.

        Args:
            parent: Useless in this case, there are no parents for this model

        Returns:
            The number of rows to display.
        """
        return len(self._pdfs_data)

    def data(self, index, role=...) -> Union[str, None]:
        """
        Returns the correct PDF data depending on the role and index.

        Args:
            index: The row to be fetched.
            role: The role of the data.

        Returns:
            The correct data associated to the index and the role
        """
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._pdfs_data[index.row()].fileName()

    def add_pdf(self, url: QUrl) -> None:
        """
        Checks if the url is a PDF.
        Adds it to the model's data structure if it is a PDF.

        Args:
            url: The URL to add to the data structure.
        """
        # parent index and row count
        index = self.index(0, 0)
        row_count = self.rowCount(index)

        self.beginInsertRows(index, row_count, row_count)

        # insert path is it's not already there
        path = url.path()
        _, extension = os.path.splitext(path)
        if extension == PDF_EXTENSION and path not in self._pdfs_data:
            self._pdfs_data.append(url)

        self.endInsertRows()

        # send signal that
        self.dataChanged.emit(index, self.index(self.rowCount()))
