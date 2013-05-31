#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

import sys

class MainWindow(QMainWindow):
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
