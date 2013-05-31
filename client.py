#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

import sys

import CORBA

import CorbaTest

class CarWidget(QWidget):
    WIDTH = 600
    HEIGHT = 226
    def __init__(self, car):
        super(CarWidget, self).__init__()
        self.setMouseTracking(True)
        self.setFixedSize(QSize(CarWidget.WIDTH, CarWidget.HEIGHT))

        self.car = car

        self.active = []
        self.hovered = None

        self.background = QImage("background.png")
        self.layers = {
            "wheels": QImage("layer-wheels.png"),
            "windows": QImage("layer-windows.png"),
            "lights": QImage("layer-lights.png"),
            "doors": QImage("layer-doors.png"),
            "steering-wheel": QImage("layer-steering-wheel.png"),
            "brakes": QImage("layer-brakes.png"),
            "engine": QImage("layer-engine.png"),
            "color": QImage("layer-color.png"),
        };

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.background)

        for layer in self.layers:
            if layer in self.active or layer == self.hovered:
                painter.drawImage(0, 0, self.layers[layer]);

        painter.end()

    def mouseMoveEvent(self, event):
        if event.x() >= 0 and event.y() >= 0 and event.x() < CarWidget.WIDTH and event.y() < CarWidget.HEIGHT:
            for layer in self.layers:
                if self.layers[layer].pixel(event.x(), event.y()):
                    if self.hovered != layer:
                        self.hovered = layer
                        self.repaint()
                    return

        if self.hovered:
            self.hovered = None
            self.repaint()

    def leaveEvent(self, event):
        if self.hovered:
            self.hovered = None
            self.repaint()

class CarFactoryTableModel(QAbstractTableModel):
    def __init__(self, factory):
        super(CarFactoryTableModel, self).__init__()
        self.factory = factory

    def rowCount(self, parent=QModelIndex()):
        print "hi"
        return self.factory.get_car_count()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()

        return self.createIndex(row, column, row)

    def parent(self, index):
        return QModelIndex()

    def data(self, index, role=Qt.DisplayRole):
        car = self.factory.get_car(index.row())
        
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return car.get_uuid()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 1:
                    return "Car ID"

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        layout = QHBoxLayout(self)

        label = QLabel(self)
        label.setPixmap(QPixmap("background.png"))
        layout.addWidget(label)

class ConnectDialog(QDialog):
    def __init__(self, orb):
        super(ConnectDialog, self).__init__()

        self.orb = orb
        self.factory = None

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("IOR string:"))

        self.object_string_box = QLineEdit()
        layout.addWidget(self.object_string_box)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.onAccepted)
        layout.addWidget(buttons)

        self.setWindowTitle("CORBA: Connection to car factory")

    def sizeHint(self):
        return QSize(600, 80)

    def onAccepted(self):
        try:
            obj = self.orb.string_to_object(self.object_string_box.text())
            self.factory = obj._narrow(CorbaTest.CarFactory)
            self.accept()
        except Exception, e:
            QMessageBox.critical(self, self.windowTitle(), str(e))


if __name__ == "__main__":
    orb = CORBA.ORB_init()

    app = QApplication(sys.argv)

    connect_dialog = ConnectDialog(orb)
    connect_dialog.exec_()
    if not connect_dialog.factory:
       sys.exit(0)

    model = CarFactoryTableModel(connect_dialog.factory)
    view = QTableView()
    view.setModel(model)
    view.show()

    app.exec_()
