# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/give_the_key_win.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GiveTheKeyWin(object):
    def setupUi(self, GiveTheKeyWin):
        GiveTheKeyWin.setObjectName("GiveTheKeyWin")
        GiveTheKeyWin.resize(814, 263)
        self.buttonBox = QtWidgets.QDialogButtonBox(GiveTheKeyWin)
        self.buttonBox.setGeometry(QtCore.QRect(460, 220, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.person_id = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.person_id.setGeometry(QtCore.QRect(10, 40, 381, 31))
        self.person_id.setObjectName("person_id")
        self.label_7 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.person_name = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.person_name.setGeometry(QtCore.QRect(10, 110, 381, 31))
        self.person_name.setObjectName("person_name")
        self.label_4 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.person_position = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.person_position.setGeometry(QtCore.QRect(10, 180, 381, 31))
        self.person_position.setObjectName("person_position")
        self.label_8 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_8.setGeometry(QtCore.QRect(420, 10, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.key_id = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.key_id.setGeometry(QtCore.QRect(420, 40, 381, 31))
        self.key_id.setObjectName("key_id")
        self.building = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.building.setGeometry(QtCore.QRect(420, 110, 381, 31))
        self.building.setObjectName("building")
        self.label_9 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_9.setGeometry(QtCore.QRect(420, 80, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(GiveTheKeyWin)
        self.label_10.setGeometry(QtCore.QRect(420, 150, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.key_name = QtWidgets.QLineEdit(GiveTheKeyWin)
        self.key_name.setGeometry(QtCore.QRect(420, 180, 381, 31))
        self.key_name.setObjectName("key_name")
        self.line = QtWidgets.QFrame(GiveTheKeyWin)
        self.line.setGeometry(QtCore.QRect(389, 10, 31, 201))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(GiveTheKeyWin)
        self.buttonBox.accepted.connect(GiveTheKeyWin.accept)  # type: ignore
        self.buttonBox.rejected.connect(GiveTheKeyWin.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GiveTheKeyWin)

    def retranslateUi(self, GiveTheKeyWin):
        _translate = QtCore.QCoreApplication.translate
        GiveTheKeyWin.setWindowTitle(_translate("GiveTheKeyWin", "Dialog"))
        self.label_7.setText(_translate("GiveTheKeyWin", "PERSON ID"))
        self.label_4.setText(_translate("GiveTheKeyWin", "ИМЯ ПОЛЬЗОВАТЕЛЯ"))
        self.label_6.setText(_translate("GiveTheKeyWin", "ДОЛЖНОСТЬ"))
        self.label_8.setText(_translate("GiveTheKeyWin", "KEY ID"))
        self.label_9.setText(_translate("GiveTheKeyWin", "ЗДАНИЕ"))
        self.label_10.setText(_translate("GiveTheKeyWin", "ИМЯ КЛЮЧА"))
