"""
Tests everything that has to do with the PDFInfoModel.
"""
import unittest
from typing import List, Dict, Union

from PyQt6.QtCore import QModelIndex, Qt

from interfaces.desktop.models.pdf_info import PDFInfoModel
from interfaces.desktop.exceptions.pdf_info_exceptions import (
    IncorrectPDFInfoModelDataLength,
)


class TestPDFInfoModel(unittest.TestCase):
    """
    Tests all functionalities of the PDFInfoModelClass
    """

    def setUp(self) -> None:
        self.data: List[Dict[str, Union[str, int]]] = [
            {
                "filename": "test.pdf",
                "filepath": "/a/path/for/test.pdf",
                "pages_amount": 5,
                "words_amount": 10,
            }
        ]
        self.data_2_pdfs: List[Dict[str, Union[str, int]]] = [
            {
                "filename": "test.pdf",
                "filepath": "/a/path/for/test.pdf",
                "pages_amount": 5,
                "words_amount": 10,
            },
            {
                "filename": "another_test.pdf",
                "filepath": "/another/path/for/another_test.pdf",
                "pages_amount": 7,
                "words_amount": 14,
            },
        ]
        self.data_model: PDFInfoModel = PDFInfoModel(self.data)
        self.data_model_2_pdfs: PDFInfoModel = PDFInfoModel(self.data_2_pdfs)

    def test_incorrect_data_length_too_long(self) -> None:
        """
        Asserts IncorrectPDFInfoModelDataLength is raised when there are too much data points.
        """
        self.data[0]["extra_args"] = "extra_value"
        with self.assertRaises(IncorrectPDFInfoModelDataLength):
            PDFInfoModel(self.data)

    def test_incorrect_data_length_too_short(self) -> None:
        """
        Asserts IncorrectPDFInfoModelDataLength is raised when there are not enough data points
        """
        del self.data[0]["filename"]
        with self.assertRaises(IncorrectPDFInfoModelDataLength):
            PDFInfoModel(self.data)

    def test_incorrect_data_types(self) -> None:
        """
        Asserts IncorrectPDFInfoModelDataLength is raised when there are too much
        or not enough data points.
        """
        self.data[0]["words_amount"] = "5"
        with self.assertRaises(TypeError):
            PDFInfoModel(self.data)

    def test_incorrect_data_keys(self) -> None:
        """
        Asserts IncorrectPDFInfoModelDataLength is raised when there are too much
        or not enough data points.
        """
        del self.data[0]["words_amount"]
        self.data[0]["words_number"] = 5
        with self.assertRaises(KeyError):
            PDFInfoModel(self.data)

    def test_column_count(self) -> None:
        """
        Asserts that the column amount returned is correct, it needs to match
        the mapping.
        """
        columns_amount = len(PDFInfoModel.mapping())
        self.assertEqual(columns_amount, self.data_model_2_pdfs.columnCount())

    def test_row_count(self) -> None:
        """
        Asserts that the row amount returned is correct, it needs to match
        the mapping.
        """
        row_amount_2_pdfs = len(self.data_2_pdfs)
        self.assertEqual(row_amount_2_pdfs, self.data_model_2_pdfs.rowCount())

        row_amount_1_pdf = len([self.data])
        self.assertEqual(row_amount_1_pdf, self.data_model.rowCount())

    def test_data(self) -> None:
        """
        Tests that the data function returns the expected data.
        """
        for row, pdf_data in enumerate(self.data_2_pdfs):
            for column, data in enumerate(pdf_data.values()):
                index = self.data_model_2_pdfs.index(row, column)
                model_data = self.data_model_2_pdfs.data(index, Qt.ItemDataRole.DisplayRole)
                self.assertEqual(data, model_data)


if __name__ == "__main__":
    unittest.main()
