import unittest
from copy import copy
from typing import List

from interfaces.desktop.models.drop_pdf_list_model import DropPDFListModel
from PyQt6.QtCore import QUrl, Qt


class TestDropPDFListModel(unittest.TestCase):
    def setUp(self) -> None:
        self.data: List[QUrl] = [
            QUrl("/a/test/file/allo.pdf"),
            QUrl("/another/test/file/bonjour.pdf"),
        ]
        self.model_with_data: DropPDFListModel = DropPDFListModel(data=copy(self.data))
        self.model_without_data: DropPDFListModel = DropPDFListModel()

    def test_row_count(self):
        self.assertEqual(len(self.data), self.model_with_data.rowCount())
        self.assertEqual(0, self.model_without_data.rowCount())

    def test_data_inserted_match(self):
        for qurl, pdf_data in zip(self.data, self.model_with_data._pdfs_data):
            self.assertEqual(qurl, pdf_data)

    def test_data_filename(self):
        for row, qurl in enumerate(self.data):
            index = self.model_with_data.index(row, 0)
            model_data = self.model_with_data.data(index, Qt.ItemDataRole.DisplayRole)
            self.assertEqual(model_data, qurl.fileName())

    def test_insert_pdf(self):
        new_pdf_url = QUrl("/new/test/file/hello.pdf")
        self.model_with_data.add_pdf(new_pdf_url)

        self.assertEqual(self.model_with_data.rowCount(), len(self.data) + 1)

        index = self.model_with_data.index(self.model_with_data.rowCount() - 1, 0)
        new_data = self.model_with_data.data(index, Qt.ItemDataRole.DisplayRole)

        self.assertEqual(new_data, new_pdf_url.fileName())

    def test_insert_file_not_pdf(self):
        new_csv_url = QUrl("/wrong/file/type.csv")
        self.model_with_data.add_pdf(new_csv_url)

        # make sure no data was inserted
        self.assertEqual(self.model_with_data.rowCount(), len(self.data))


if __name__ == "__main__":
    unittest.main()
