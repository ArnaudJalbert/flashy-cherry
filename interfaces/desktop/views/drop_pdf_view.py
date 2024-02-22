"""
View that allows PDF files to be dropped and saved.
"""
import sys

from PyQt6.QtWidgets import QApplication, QListView
from PyQt6.QtCore import pyqtSignal, QSize, Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from interfaces.desktop.models import DropPDFListModel


class DropPDFListView(QListView):
    def __init__(self, parent=None):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the initial state of the object, which in this case means setting
        the acceptDrops property to True so that it can receive drag events.

        Args:
            self: Represent the instance of the object itself
            parent: Set the parent of the widget

        Returns:
            The object that is being initialized
        """
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        Triggered when files are dragged onto the view.
        Checks if the provided data contains urls.
        Accept the event if there are urls.

        Args:
            event: The drag enter event.
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        """
        Triggered when files are dragged and moved onto the view.
        Checks if the provided data contains urls.
        Accept the event if there are urls.

        Args:
            event: The drag move event.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """
        Triggered when files are dropped into the view.
        Checks if the provided data contains urls and if they have a PDF extension.
        Accept the event if there are urls.

        Args:
            event: The drop event.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for dropped_url in event.mimeData().urls():
                self.model().add_pdf(dropped_url)
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DropPDFListView()
    model = DropPDFListModel()
    form.setModel(model)
    form.show()
    app.exec()
