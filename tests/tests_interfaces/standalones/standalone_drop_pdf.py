import sys
from PyQt6.QtWidgets import QApplication
from interfaces.desktop.views.drop_pdf_view import DropPDFListView
from interfaces.desktop.models.drop_pdf_list_model import DropPDFListModel

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)

    # init view and model
    drop_pdf_view: DropPDFListView = DropPDFListView()
    drop_pdf_model: DropPDFListModel = DropPDFListModel()
    drop_pdf_view.setModel(drop_pdf_model)

    # show view
    drop_pdf_view.show()

    app.exec()
