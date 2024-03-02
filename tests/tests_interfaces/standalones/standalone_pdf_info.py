import sys
from typing import List, Dict, Union

from PyQt6.QtWidgets import QApplication, QTableView
from interfaces.desktop.models.pdf_info_model import PDFInfoModel

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)

    # fake data
    data: List[Dict[str, Union[str, int]]] = [
        {
            "filename": "test.pdf",
            "filepath": "/a/path/for/test.pdf",
            "pages_amount": 5,
            "words_amount": 10,
        }
    ]

    # init model and view
    pdf_info_model: PDFInfoModel = PDFInfoModel(data)
    table_view: QTableView = QTableView()
    table_view.setModel(pdf_info_model)

    # show view
    table_view.show()

    app.exec()
