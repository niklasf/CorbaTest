#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

import sys
import threading

import CORBA

import CorbaTest

class CarWidget(QWidget):
    WIDTH = 600
    HEIGHT = 226

    doRepaint = Signal()
    doShowLock = Signal()

    def __init__(self, car):
        super(CarWidget, self).__init__()
        self.setMouseTracking(True)
        self.setFixedSize(QSize(CarWidget.WIDTH, CarWidget.HEIGHT))

        self.doRepaint.connect(self.repaint)
        self.doShowLock.connect(self.onShowLock)

        self.car = car

        self.active = []
        self.onUpdate()
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

        self.setWindowTitle("CORBA: Car " + self.car.get_uuid())

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

    def mouseReleaseEvent(self, event):
        if event.x() >= 0 and event.y() >= 0 and event.x() < CarWidget.WIDTH and event.y() < CarWidget.HEIGHT:
            for layer in self.layers:
                if self.layers[layer].pixel(event.x(), event.y()):
                    if layer in self.active:
                        QMessageBox.warning(self, self.windowTitle(), "Already done.")
                        return

                    thread = threading.Thread(target=self.doLayer, args=[layer])
                    thread.start()

    def onShowLock(self):
        QMessageBox.warning(self, self.windowTitle(), "Car is locked.")

    def doLayer(self, layer):
        ret = False

        if layer == "color":
            ret = self.car.add_color()
        elif layer == "engine":
            ret = self.car.add_engine()
        elif layer == "wheels":
            ret = self.car.add_wheels()
        elif layer == "windows":
            ret = self.car.add_windows()
        elif layer == "doors":
            ret = self.car.add_doors()
        elif layer == "steering-wheel":
            ret = self.car.add_steering_wheel()
        elif layer == "brakes":
            ret = self.car.add_brakes()
        elif layer == "lights":
            ret = self.car.add_lights()

        if not ret:
            self.doShowLock.emit()
        else:
            self.onUpdate()
            self.doRepaint.emit()

    def onUpdate(self):
        self.active = []
        if self.car.has_wheels():
            self.active.append("wheels")
        if self.car.has_windows():
            self.active.append("windows")
        if self.car.has_doors():
            self.active.append("doors")
        if self.car.has_engine():
            self.active.append("engine")
        if self.car.has_brakes():
            self.active.append("brakes")
        if self.car.has_lights():
            self.active.append("lights")
        if self.car.has_steering_wheel():
            self.active.append("steering-wheel")
        if self.car.has_color():
            self.active.append("color")

class CarFactoryTableModel(QAbstractTableModel):
    def __init__(self, factory):
        super(CarFactoryTableModel, self).__init__()
        self.factory = factory

    def rowCount(self, parent=QModelIndex()):
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
                if section == 0:
                    return "Car ID"

class MainWindow(QMainWindow):
    def __init__(self, factory):
        super(MainWindow, self).__init__()

        self.windows = { }

        self.factory = factory
        self.model = CarFactoryTableModel(factory)

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.doubleClicked.connect(self.onDoubleClicked)
        self.setCentralWidget(self.view)

        self.setWindowTitle("CORBA: Car list")

    def sizeHint(self):
        return QSize(600, 400)

    def onDoubleClicked(self, index):
        if not index.row() in self.windows or not self.windows[index.row()].isVisible():
            car = self.factory.get_car(index.row())
            self.windows[index.row()] = CarWidget(car)
        self.windows[index.row()].show()
        self.windows[index.row()].activateWindow()

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

    main_window = MainWindow(connect_dialog.factory)
    main_window.show()

    app.exec_()
