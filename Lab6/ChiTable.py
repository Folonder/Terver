
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class ChiTable(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('chi_table.ui', self)