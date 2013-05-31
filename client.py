#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

import sys

class CarWidget(QWidget):
    WIDTH = 600
    HEIGHT = 226
    def __init__(self, car):
        super(CarWidget, self).__init__()
        self.setMouseTracking(True)

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

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        layout = QHBoxLayout(self)

        label = QLabel(self)
        label.setPixmap(QPixmap("background.png"))
        layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #main_window = MainWindow()
    #main_window.show()
    car_widget = CarWidget(None)
    car_widget.show()
    app.exec_()
