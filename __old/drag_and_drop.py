"""

    this script will cater the DRAG & DROP function of the app

"""
import os

from gui.ui_main_window import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Gif_drop(QLabel):

    fileDropped = Signal(list)

    def __init__(self, type, parent=None):
        super(Gif_drop, self).__init__(parent)
       


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.fileDropped.emit(links)
        else:
            event.ignore()


