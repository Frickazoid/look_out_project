# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/person_create.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Person_Create_Win(object):
    def setupUi(self, Person_Create_Win):
        Person_Create_Win.setObjectName("Person_Create_Win")
        Person_Create_Win.resize(402, 321)
        self.buttonBox = QtWidgets.QDialogButtonBox(Person_Create_Win)
        self.buttonBox.setGeometry(QtCore.QRect(240, 280, 151, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_4 = QtWidgets.QLabel(Person_Create_Win)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 381, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Person_Create_Win)
        self.label_5.setGeometry(QtCore.QRect(10, 140, 381, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Person_Create_Win)
        self.label_6.setGeometry(QtCore.QRect(10, 210, 381, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.person_name = QtWidgets.QLineEdit(Person_Create_Win)
        self.person_name.setGeometry(QtCore.QRect(10, 100, 381, 40))
        self.person_name.setObjectName("person_name")
        self.person_position = QtWidgets.QLineEdit(Person_Create_Win)
        self.person_position.setGeometry(QtCore.QRect(10, 240, 381, 40))
        self.person_position.setObjectName("person_position")
        self.person_date = QtWidgets.QDateEdit(Person_Create_Win)
        self.person_date.setGeometry(QtCore.QRect(10, 170, 381, 40))
        self.person_date.setCalendarPopup(True)
        self.person_date.setObjectName("person_date")
        self.person_id = QtWidgets.QLineEdit(Person_Create_Win)
        self.person_id.setGeometry(QtCore.QRect(10, 40, 381, 31))
        self.person_id.setObjectName("person_id")
        self.label_7 = QtWidgets.QLabel(Person_Create_Win)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Person_Create_Win)
        self.buttonBox.accepted.connect(Person_Create_Win.accept)  # type: ignore
        self.buttonBox.rejected.connect(Person_Create_Win.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Person_Create_Win)

    def retranslateUi(self, Person_Create_Win):
        _translate = QtCore.QCoreApplication.translate
        Person_Create_Win.setWindowTitle(_translate("Person_Create_Win", "Dialog"))
        self.label_4.setText(_translate("Person_Create_Win", "NAME"))
        self.label_5.setText(_translate("Person_Create_Win", "DATE OF BIRTH"))
        self.label_6.setText(_translate("Person_Create_Win", "POSITION"))
        self.label_7.setText(_translate("Person_Create_Win", "ID"))
