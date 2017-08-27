# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_fit.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(599, 434)
        self.gridLayout_2 = QtWidgets.QGridLayout(Window)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.speedSlider = QtWidgets.QSlider(Window)
        self.speedSlider.setMinimum(1)
        self.speedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider.setInvertedAppearance(False)
        self.speedSlider.setInvertedControls(False)
        self.speedSlider.setObjectName("speedSlider")
        self.gridLayout.addWidget(self.speedSlider, 1, 1, 1, 2)
        self.colorTwoView = QtWidgets.QGraphicsView(Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorTwoView.sizePolicy().hasHeightForWidth())
        self.colorTwoView.setSizePolicy(sizePolicy)
        self.colorTwoView.setMaximumSize(QtCore.QSize(16777215, 100))
        self.colorTwoView.setObjectName("colorTwoView")
        self.gridLayout.addWidget(self.colorTwoView, 5, 1, 1, 1)
        self.colorThreeView = QtWidgets.QGraphicsView(Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorThreeView.sizePolicy().hasHeightForWidth())
        self.colorThreeView.setSizePolicy(sizePolicy)
        self.colorThreeView.setMaximumSize(QtCore.QSize(16777215, 100))
        self.colorThreeView.setObjectName("colorThreeView")
        self.gridLayout.addWidget(self.colorThreeView, 5, 2, 1, 1)
        self.colorOneView = QtWidgets.QGraphicsView(Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorOneView.sizePolicy().hasHeightForWidth())
        self.colorOneView.setSizePolicy(sizePolicy)
        self.colorOneView.setMinimumSize(QtCore.QSize(0, 0))
        self.colorOneView.setMaximumSize(QtCore.QSize(16777215, 100))
        self.colorOneView.setObjectName("colorOneView")
        self.gridLayout.addWidget(self.colorOneView, 5, 0, 1, 1)
        self.speedLabel = QtWidgets.QLabel(Window)
        self.speedLabel.setObjectName("speedLabel")
        self.gridLayout.addWidget(self.speedLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.colorOneLabel = QtWidgets.QLabel(Window)
        self.colorOneLabel.setObjectName("colorOneLabel")
        self.gridLayout.addWidget(self.colorOneLabel, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.colorThreeLabel = QtWidgets.QLabel(Window)
        self.colorThreeLabel.setObjectName("colorThreeLabel")
        self.gridLayout.addWidget(self.colorThreeLabel, 4, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.colorTwoLabel = QtWidgets.QLabel(Window)
        self.colorTwoLabel.setObjectName("colorTwoLabel")
        self.gridLayout.addWidget(self.colorTwoLabel, 4, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.startStopButton = QtWidgets.QPushButton(Window)
        self.startStopButton.setObjectName("startStopButton")
        self.gridLayout.addWidget(self.startStopButton, 0, 2, 1, 1)
        self.openButton = QtWidgets.QPushButton(Window)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 1)
        self.imageView = QGraphicsViewFit(Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)
        self.imageView.setMinimumSize(QtCore.QSize(1, 1))
        self.imageView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imageView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imageView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.imageView.setObjectName("imageView")
        self.gridLayout.addWidget(self.imageView, 3, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Form"))
        self.speedLabel.setText(_translate("Window", "Speed"))
        self.colorOneLabel.setText(_translate("Window", "Color 1"))
        self.colorThreeLabel.setText(_translate("Window", "Color 3"))
        self.colorTwoLabel.setText(_translate("Window", "Color 2"))
        self.startStopButton.setText(_translate("Window", "Start/Stop"))
        self.openButton.setText(_translate("Window", "Open Image"))

from qgraphicsviewfit import QGraphicsViewFit

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QWidget()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())

