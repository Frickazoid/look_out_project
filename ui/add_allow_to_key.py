# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/add_allow_to_key.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Add_Allow_Key_Win(object):
    def setupUi(self, Add_Allow_Key_Win):
        Add_Allow_Key_Win.setObjectName("Add_Allow_Key_Win")
        Add_Allow_Key_Win.resize(823, 190)
        self.buttonBox = QtWidgets.QDialogButtonBox(Add_Allow_Key_Win)
        self.buttonBox.setGeometry(QtCore.QRect(656, 150, 151, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_4 = QtWidgets.QLabel(Add_Allow_Key_Win)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Add_Allow_Key_Win)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.building_name = QtWidgets.QLineEdit(Add_Allow_Key_Win)
        self.building_name.setGeometry(QtCore.QRect(10, 40, 381, 31))
        self.building_name.setObjectName("building_name")
        self.building_box = QtWidgets.QComboBox(Add_Allow_Key_Win)
        self.building_box.setGeometry(QtCore.QRect(10, 40, 381, 31))
        self.building_box.setObjectName("building_box")
        self.key_id = QtWidgets.QLineEdit(Add_Allow_Key_Win)
        self.key_id.setGeometry(QtCore.QRect(426, 110, 381, 31))
        self.key_id.setObjectName("key_id")
        self.label_7 = QtWidgets.QLabel(Add_Allow_Key_Win)
        self.label_7.setGeometry(QtCore.QRect(426, 80, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.keys_box = QtWidgets.QComboBox(Add_Allow_Key_Win)
        self.keys_box.setGeometry(QtCore.QRect(10, 110, 381, 31))
        self.keys_box.setObjectName("keys_box")
        self.person_name = QtWidgets.QLineEdit(Add_Allow_Key_Win)
        self.person_name.setGeometry(QtCore.QRect(426, 40, 381, 31))
        self.person_name.setObjectName("person_name")
        self.label_5 = QtWidgets.QLabel(Add_Allow_Key_Win)
        self.label_5.setGeometry(QtCore.QRect(426, 10, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Add_Allow_Key_Win)
        self.buttonBox.accepted.connect(Add_Allow_Key_Win.accept)  # type: ignore
        self.buttonBox.rejected.connect(Add_Allow_Key_Win.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Add_Allow_Key_Win)

    def retranslateUi(self, Add_Allow_Key_Win):
        _translate = QtCore.QCoreApplication.translate
        Add_Allow_Key_Win.setWindowTitle(_translate("Add_Allow_Key_Win", "Dialog"))
        self.label_4.setText(_translate("Add_Allow_Key_Win", "ЗДАНИЕ"))
        self.label_6.setText(_translate("Add_Allow_Key_Win", "ИМЯ КЛЮЧА"))
        self.label_7.setText(_translate("Add_Allow_Key_Win", "ID"))
        self.label_5.setText(_translate("Add_Allow_Key_Win", "ПОЛЬЗОВАТЕЛЬ"))
