import datetime
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QCompleter

from UI.add_allow_to_key import Ui_Add_Allow_Key_Win
from UI.adm_win import Ui_AdmWindow
from UI.build_create import Ui_Build_Create_Win
from UI.build_edit import Ui_Build_Edit_Win
from UI.give_the_key_win import Ui_GiveTheKeyWin
from UI.key_create import Ui_Key_Create_Win
from UI.main_win import Ui_MainWindow
from UI.person_create import Ui_Person_Create_Win
from UI.person_edit import Ui_Person_Edit_Win
from UI.report_win import Ui_ReportWin
from UI.return_the_key_win import Ui_ReturnTheKeyWin
from UI.vahta_win import Ui_VahtaWindow
from db_scheme import *


# person_id = int(1231231235)
# person1 = Person(id=person_id, name='Bob', birthday=date(1960, 1, 15), position='Teacher')
# person1.save()
#
# person_id = int(1231231232)
# person2 = Person(id=person_id, name='Maggy', birthday=date(1985, 6, 7), position='Teacher')
# person2.save()
#
# build1 = Building(name='build1')
# build1.save()
#
# build2 = Building(name='build2')
# build2.save()

# key1 = Key(name='key1',build=build1)
# key1.save()
#
# key2 = Key(name='key2',build=build1)
# key2.save()
#
# key3 = Key(name='key3',build=build1)
# key3.save()
#
# key1 = Key(name='key1',build=build2)
# key1.save()
#
# key2 = Key(name='key2',build=build2)
# key2.save()

class PersonEditWindow(QtWidgets.QDialog, Ui_Person_Edit_Win):
    window_closed = pyqtSignal()

    def __init__(self, person_ID):
        super().__init__()
        self.setupUi(self)
        self.person = Person.get(Person.guid == person_ID)
        self.fill_person()
        self.fill_buildings()
        self.currBuilding = None
        self.set_building()
        self.person_id.setReadOnly(True)
        self.person_name.setReadOnly(True)
        self.person_date.setReadOnly(True)
        self.person_position.setReadOnly(True)
        editbtn = self.EditSave_buttonBox.addButton('Edit', QtWidgets.QDialogButtonBox.ActionRole)
        editbtn.clicked.connect(self.edit_person)
        savebtn = self.EditSave_buttonBox.addButton('Save', QtWidgets.QDialogButtonBox.ActionRole)
        savebtn.clicked.connect(self.save_person)
        delbtn = self.EditSave_buttonBox.addButton('Delete', QtWidgets.QDialogButtonBox.ActionRole)
        delbtn.clicked.connect(self.show_affirmative_dialogue)
        self.person_id.returnPressed.connect(self.onEnterPressing)
        self.building_box.activated.connect(self.set_building)
        self.btn_add_key.clicked.connect(self.open_add_key_to_person)
        self.btn_del_key.clicked.connect(self.show_affirmative_dialogue)

    def onEnterPressing(self):
        self.person_name.setFocus(True)

    def delete_person(self):
        try:
            query = Person.delete().where(Person.guid == self.person.guid)
            query.execute()
            # Не работает, понять почему?
            # user = Person.get(Person.id == self.person.id)
            # user.delete_instance()

            self.window_closed.emit()
            self.close()
        except Exception as err:
            print(err)

    def show_affirmative_dialogue(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Вы действительно хотите удалить данный элемент из базы данных?")
        msgBox.setWindowTitle("Подтвердите удаление")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:
            self.delete_person()

    def accept(self):
        if self.buttonBox.hasFocus():
            self.window_closed.emit()
            self.close()

    def save_person(self):

        try:
            person = self.person
            person.guid = int(self.person_id.text().upper())
            person.name = self.person_name.text().upper()
            person.birthday = self.person_date.date().toPyDate()
            person.position = self.person_position.text().upper()
            person.save()
        except Exception as err:
            print(err)

    def edit_person(self):
        # self.person_id.setReadOnly(False)
        self.person_name.setFocus(True)
        self.person_name.setReadOnly(False)
        self.person_date.setReadOnly(False)
        self.person_position.setReadOnly(False)

    def fill_person(self):
        self.person_id.setText(str(self.person.guid))
        self.person_name.setText(self.person.name)
        self.person_date.setDate(self.person.birthday)
        self.person_position.setText(self.person.position)

    def fill_buildings(self):

        self.building_box.clear()
        buildings_query = Building.select()

        for building in buildings_query:
            self.building_box.addItem('[' + str(building.id) + '] ' + building.name)

    def set_building(self):
        buildName = self.building_box.currentText()
        startIndex = buildName.find('[', 0)
        startIndex += 1
        endIndex = buildName.find(']', 0)
        buildID = buildName[startIndex:endIndex]
        self.currBuilding = Building.get_by_id(int(buildID))
        self.fill_keys()

    def fill_keys(self):

        self.keys_table.clear()
        self.keys_table.setRowCount(0)

        keys = Key.select().where(Key.build_id == self.currBuilding)
        query = AllowedKeys.select().where((AllowedKeys.user == self.person) & AllowedKeys.key.in_(keys))

        for conniction in query:
            currentRowCount = self.keys_table.rowCount()
            self.keys_table.insertRow(currentRowCount)
            self.keys_table.setItem(currentRowCount, 0, QTableWidgetItem(conniction.key.name))
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, conniction.key.guid)
            self.keys_table.setItem(currentRowCount, 1, item)

    def open_add_key_to_person(self):
        self.addKeyToPersonUI = AddAllowKeyWin(self.currBuilding, self.person)
        self.addKeyToPersonUI.window_closed.connect(self.fill_keys)
        self.addKeyToPersonUI.show()

    def show_affirmative_dialogue(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Вы действительно хотите удалить данный элемент из базы данных?")
        msgBox.setWindowTitle("Подтвердите удаление")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            if self.sender().objectName().find('key') != -1:
                self.del_connection_key_to_person()
                self.fill_keys()

    def del_connection_key_to_person(self):

        if self.keys_table.selectionModel().selectedIndexes().__len__() > 0:

            for idx in self.keys_table.selectionModel().selectedIndexes():
                row_number = idx.row()
                keyGUID = self.keys_table.item(row_number, 1).text()
                key = Key.get(Key.guid == keyGUID)
                try:
                    query = AllowedKeys.delete().where((AllowedKeys.user == self.person) & (AllowedKeys.key == key))
                    query.execute()
                    self.fill_keys()
                except Exception as err:
                    print(err)


class PersonCreateWindow(QtWidgets.QDialog, Ui_Person_Create_Win):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.clearForm()
        self.person_id.setFocus(True)
        self.person_id.returnPressed.connect(self.onEnterPressing)

    def clearForm(self):
        self.person_id.clear()
        self.person_name.clear()
        self.person_date.clear()
        self.person_position.clear()

    def onEnterPressing(self):
        self.person_name.setFocus(True)

    def accept(self):

        if self.buttonBox.hasFocus():
            # ID = int(self.person_id.text().upper())
            ID = self.person_id.text().upper()
            name = self.person_name.text().upper()
            birthday = self.person_date.date().toPyDate()
            position = self.person_position.text().upper()
            person_guery = Person.select().where(Person.guid == ID)
            if person_guery.count() == 0:
                person_exist_id = self.find_person(name, birthday)
                if person_exist_id is None:
                    try:
                        new_person = Person(guid=ID, name=name, birthday=birthday, position=position)
                        new_person.save(force_insert=True)
                    except Exception as err:
                        print(err)
                    self.window_closed.emit()
                    self.close()
                else:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setWindowTitle("Warning")
                    msgBox.setText("Person exist, id:" + str(person_exist_id))
                    msgBox.exec()
                    # print("person exist, id:" + person_exist_id)
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Warning")
                msgBox.setText("This ID already in using, id:")
                msgBox.exec()

    def find_person(self, name, birthday):
        person_id = None
        person_query = Person.select().where((Person.name == name) & (Person.birthday == birthday))
        if person_query.count() == 1:
            person_id = person_query[0].guid
        return person_id


class BuildCreateWin(QtWidgets.QDialog, Ui_Build_Create_Win):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):

        buildName = self.build_name.text().upper()
        build_exist_id = self.find_build_by_name(buildName)
        if build_exist_id == None:
            try:
                new_building = Building(name=buildName)
                new_building.save()
                self.show_massage('Success', 'Building successfully created')
            except Exception as err:
                print(err)
        else:
            self.show_massage('Warning', "Building exist, id:" + str(build_exist_id))
            # print("Buildning exist, id:" + build_exist_id)
        self.window_closed.emit()
        self.close()

    def find_build_by_name(self, buildName):
        building_id = None
        buildings_query = Building.select().where((Building.name == buildName))
        if buildings_query.count() == 1:
            building_id = buildings_query[0].guid
        return building_id

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()


class BuildEditWin(QtWidgets.QDialog, Ui_Build_Edit_Win):
    window_closed = pyqtSignal()

    def __init__(self, building_id):
        super().__init__()
        self.setupUi(self)

        self.building = Building.get_by_id(building_id)
        self.build_name.setText(self.building.name)
        self.btn_add_key.clicked.connect(self.add_key_to_building)

    def accept(self):

        buildName = self.build_name.text().upper()
        if buildName != self.building.name:
            build_exist_id = self.find_build_by_name(buildName)
            if build_exist_id != None:
                self.show_massage('Warning', "THIS name in already using , id:" + str(build_exist_id))
            else:
                try:
                    self.building.name = buildName
                    self.building.save()
                    self.show_massage('Success', 'Building successfully changing')
                except Exception as err:
                    print(err)
                self.window_closed.emit()
                self.close()
        else:
            self.window_closed.emit()
            self.close()

    def find_build_by_name(self, buildName):
        building_id = None
        buildings_query = Building.select().where((Building.name == buildName))
        if buildings_query.count() == 1:
            building_id = buildings_query[0].id
        return building_id

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()

    def add_key_to_building(self):
        self.keyCreateUI = KeyCreateWin(self.building)
        self.keyCreateUI.show()


class KeyCreateWin(QtWidgets.QDialog, Ui_Key_Create_Win):
    window_closed = pyqtSignal()

    def __init__(self, building=None):
        super().__init__()
        self.setupUi(self)
        self.key_id.setFocus()
        self.key_id.returnPressed.connect(self.onEnterPressing)
        if building != None:
            self.building_box.setVisible(False)
            self.building = building
            self.building_name.setText(self.building.name)
            self.building_name.setReadOnly(True)
        else:
            self.building_name.setVisible(False)
            self.fill_buildings()
            self.building_box.currentIndexChanged.connect(self.set_building)
            self.set_building()

    def onEnterPressing(self):
        self.key_name.setFocus(True)

    def set_building(self):
        buildName = self.building_box.currentText()
        startIndex = buildName.find('[', 0)
        startIndex += 1
        endIndex = buildName.find(']', 0)
        buildID = buildName[startIndex:endIndex]
        self.building = Building.get_by_id(int(buildID))

    def fill_buildings(self):

        buildings_query = Building.select()

        for building in buildings_query:
            self.building_box.addItem('[' + str(building.id) + '] ' + building.name)

    def accept(self):

        if self.buttonBox.hasFocus():
            ID = int(self.key_id.text().upper())
            keyName = self.key_name.text().upper()
            key_guery = Key.select().where(Key.guid == ID)
            if key_guery.count() == 0:
                key_exist_id = self.find_key_by_name(keyName)
                if key_exist_id != None:
                    self.show_massage('Warning', "THIS name in already using , id:" + str(key_exist_id))
                else:
                    try:
                        new_key = Key(guid=ID, name=keyName, build_id=self.building.id)
                        new_key.save(force_insert=True)
                        self.show_massage('Success', 'Key successfully created')
                        self.window_closed.emit()
                        self.close()
                    except Exception as err:
                        print(err)
                        self.show_massage('Failure', str(err))
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Warning")
                msgBox.setText("This ID already in using, id:")
                msgBox.exec()

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()

    def find_key_by_name(self, keyName):
        keyID = None
        keys_query = Key.select().where((Key.name == keyName) & (Key.build_id == self.building.id))
        if keys_query.count() == 1:
            keyID = keys_query[0].guid
        return keyID


class AddAllowKeyWin(QtWidgets.QDialog, Ui_Add_Allow_Key_Win):
    window_closed = pyqtSignal()

    def __init__(self, building=None, person=None):
        super().__init__()
        self.setupUi(self)
        self.person = person
        self.person_name.setText(self.person.name)
        self.person_name.setReadOnly(True)
        self.key = None
        self.building = building
        self.fill_buildings()
        self.set_current_building_box()
        self.building_box.activated.connect(self.set_building)
        self.keys_box.activated.connect(self.set_key)

        self.filL_keys()
        self.key_id.setFocus()
        self.key_id.returnPressed.connect(self.on_enter_pressing)

    def on_enter_pressing(self):

        self.key = Key.get(Key.guid == self.key_id.text())
        self.building = Building.get(Building.id == self.key.build_id)
        self.set_current_building_box()
        if self.key is not None:
            text = '[' + str(self.key.guid) + '] ' + self.key.name
            index = self.keys_box.findText(text, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.keys_box.setCurrentIndex(index)

    def fill_buildings(self):
        buildings_query = Building.select()

        for building in buildings_query:
            self.building_box.addItem('[' + str(building.id) + '] ' + building.name)

    def fill_keys(self):
        self.keys_box.clear()
        keys_query = Key.select().where(Key.build_id == self.building)

        for key in keys_query:
            self.keys_box.addItem('[' + str(key.guid) + '] ' + key.name)

        text = '-Выберите ключ-'
        self.keys_box.addItem(text)
        index = self.keys_box.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.keys_box.setCurrentIndex(index)

    def set_current_building_box(self):
        text = '[' + str(self.building.id) + '] ' + self.building.name
        index = self.building_box.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.building_box.setCurrentIndex(index)
            self.fill_keys()

    def set_building(self):
        buildName = self.building_box.currentText()
        startIndex = buildName.find('[', 0)
        startIndex += 1
        endIndex = buildName.find(']', 0)
        buildID = buildName[startIndex:endIndex]
        self.building = Building.get_by_id(int(buildID))

    def set_key(self):
        keyName = self.keys_box.currentText()
        startIndex = keyName.find('[', 0)
        startIndex += 1
        endIndex = keyName.find(']', 0)

        self.key_id.setText(keyName[startIndex:endIndex])
        try:
            self.key = Key.get(Key.guid == self.key_id.text())
        except Exception as err:
            self.key = None

    def accept(self):
        if self.buttonBox.hasFocus():

            # keyGUID = self.key.guid
            # personGUID = self.person.guid
            allow_guery = AllowedKeys.select().where((AllowedKeys.user == self.person) & (AllowedKeys.key == self.key))
            if allow_guery.count() == 0:
                try:
                    new_connection = AllowedKeys(key=self.key, user=self.person)
                    new_connection.save()
                    self.show_massage('Success', 'Connection successfully created')
                    self.window_closed.emit()
                    self.close()
                except Exception as err:
                    print(err)
                    self.show_massage('Failure to add new connection', str(err))
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Warning")
                msgBox.setText("This key id: " + str(self.key.guid) + ' already allowed to user ' + str(
                    self.person.name) + '(' + self.person.id + ')')
                msgBox.exec()

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()


class AdmWindow(QtWidgets.QMainWindow, Ui_AdmWindow):

    def __init__(self):
        # super(Ui_MainWindow, self).__init__()
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Заполняем количество колонок и скрываем одну из них
        # self.persons_table.setColumnCount(2)
        # self.persons_table.setColumnHidden(1, True)
        # Убираем заголовки таблицы
        # Заполняем таблицу данными
        self.fill_persons()
        self.fill_buildings()
        self.persons_table.doubleClicked.connect(self.open_person_edit_ui)
        self.buildings_table.clicked.connect(self.fill_keys_by_building)
        self.buildings_table.doubleClicked.connect(self.open_build_edit_ui)
        self.btn_add_person.clicked.connect(self.open_person_create_ui)
        self.btn_add_build.clicked.connect(self.open_build_create_ui)
        self.btn_add_key.clicked.connect(self.open_key_create_ui)
        self.btn_del_build.clicked.connect(self.show_affirmative_dialogue)
        self.btn_del_key.clicked.connect(self.show_affirmative_dialogue)

    def show_affirmative_dialogue(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Вы действительно хотите удалить данный элемент из базы данных?")
        msgBox.setWindowTitle("Подтвердите удаление")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            if self.sender().objectName().find('build') != -1:
                self.delete_buildings()
                self.fill_buildings()
            else:
                self.delete_keys()
                self.fill_keys_by_building()

    def delete_keys(self):
        for idx in self.keys_table.selectionModel().selectedIndexes():
            row_number = idx.row()
            key_id = self.keys_table.item(row_number, 1).text()
            key = Key.get_by_id(key_id)
            try:
                key.delete_instance()
            except Exception as err:
                print(err)

    def delete_buildings(self):
        for idx in self.buildings_table.selectionModel().selectedIndexes():
            row_number = idx.row()
            building_id = self.buildings_table.item(row_number, 1).text()
            building = Building.get_by_id(building_id)
            try:
                building.delete_instance()
            except Exception as err:
                print(err)

    def fill_persons(self):
        self.persons_table.clear()
        self.persons_table.setRowCount(0)
        query = Person.select()

        for person in query:
            # print(user.name, user.id, user.birthday)
            currentRowCount = self.persons_table.rowCount()
            self.persons_table.insertRow(currentRowCount)
            self.persons_table.setItem(currentRowCount, 0, QTableWidgetItem(person.name))
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, person.guid)
            self.persons_table.setItem(currentRowCount, 1, item)

    def fill_buildings(self):
        self.buildings_table.clear()
        self.buildings_table.setRowCount(0)
        query = Building.select()

        for building in query:
            currentRowCount = self.buildings_table.rowCount()
            self.buildings_table.insertRow(currentRowCount)
            self.buildings_table.setItem(currentRowCount, 0, QTableWidgetItem(building.name))
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, building.id)
            self.buildings_table.setItem(currentRowCount, 1, item)

    def fill_keys_by_building(self):

        self.keys_table.clear()
        self.keys_table.setRowCount(0)

        if self.buildings_table.selectionModel().selectedIndexes().__len__() > 0:
            for idx in self.buildings_table.selectionModel().selectedIndexes():
                row_number = idx.row()
            building_id = self.buildings_table.item(row_number, 1).text()
            query = Key.select().where(Key.build_id == building_id)

            for key in query:
                currentRowCount = self.keys_table.rowCount()
                self.keys_table.insertRow(currentRowCount)
                self.keys_table.setItem(currentRowCount, 0, QTableWidgetItem(key.name))
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, key.guid)
                self.keys_table.setItem(currentRowCount, 1, item)

    def open_person_edit_ui(self, item):
        for idx in self.persons_table.selectionModel().selectedIndexes():
            row_number = idx.row()
        # print(self.persons_table.item(1, 1).text())
        # print(self.persons_table.currentItem().text())
        person_id = self.persons_table.item(row_number, 1).text()
        self.personCreateUI = PersonEditWindow(int(person_id))
        self.personCreateUI.window_closed.connect(self.fill_persons)
        self.personCreateUI.show()

    def open_person_create_ui(self):
        self.personCreateUI = PersonCreateWindow()
        self.personCreateUI.window_closed.connect(self.fill_persons)
        self.personCreateUI.show()

    def open_build_create_ui(self):
        self.buildingCreateUI = BuildCreateWin()
        self.buildingCreateUI.window_closed.connect(self.fill_buildings)
        self.buildingCreateUI.show()

    def open_build_edit_ui(self):
        for idx in self.buildings_table.selectionModel().selectedIndexes():
            row_number = idx.row()
        # print(self.persons_table.item(1, 1).text())
        # print(self.persons_table.currentItem().text())
        building_id = self.buildings_table.item(row_number, 1).text()
        self.buildingEditUI = BuildEditWin(int(building_id))
        self.buildingEditUI.window_closed.connect(self.fill_buildings)
        self.buildingEditUI.window_closed.connect(self.fill_keys_by_building)
        self.buildingEditUI.show()

    def open_key_create_ui(self):
        self.keyCreateUI = KeyCreateWin()
        self.keyCreateUI.window_closed.connect(self.fill_keys_by_building)
        self.keyCreateUI.show()


class GiveTheKeyWin(QtWidgets.QDialog, Ui_GiveTheKeyWin):

    def __init__(self):
        # super(Ui_MainWindow, self).__init__()
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        # self.person_name.setReadOnly(True)
        self.fill_persons_list()
        self.person_position.setReadOnly(True)
        self.building.setReadOnly(True)
        self.key_name.setReadOnly(True)

        self.key = None
        self.person = None

        self.person_id.setFocus()
        self.person_id.returnPressed.connect(self.fill_person_data)
        self.key_id.returnPressed.connect(self.fill_key_data)

    def fill_persons_list(self):
        query = Person.select()
        personList = []
        for q in query:
            person_string = q.name + ' [' + str(q.birthday) + ']'
            personList.append(person_string)
        completer = QCompleter(personList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.person_name.setCompleter(completer)

    def fill_person_data(self):
        if self.person_id != '':
            try:
                self.person = Person.get(Person.guid == self.person_id.text())
                self.person_name.setText(self.person.name)
                self.person_position.setText(self.person.position)
                self.key_id.setFocus()
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Пользователь с данным ID не найден')
                self.person_id.setFocus()

    def fill_key_data(self):
        if self.key_id != '':
            try:
                self.key = Key.get(Key.guid == self.key_id.text())
                self.key_name.setText(self.key.name)
                building = Building.get_by_id(self.key.build_id)
                self.building.setText(building.name)
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Ключ с данным ID не найден')
                self.person_id.setFocus()

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()

    def accept(self):
        if self.buttonBox.hasFocus():
            if self.key is not None and self.person is not None:
                key_available = self.get_key_status()
                if key_available:
                    try:
                        date = QDateTime.currentDateTime().toPyDateTime()
                        comment = 'Ключ выдан: ' + str(self.person.name)
                        new_key_history = KeysHistory(key=self.key, user=self.person, date=date, this_return=False,
                                                      comment=comment)
                        new_key_history.save()
                        self.show_massage('Success', 'Ключ успешно выдан')
                        self.close()
                    except Exception as err:
                        self.show_massage('Failed', 'Не удалось выдать ключ')
                        print(err)
                else:
                    self.show_massage('Failed', 'Ключ не доступен для выдачи, проверьте историю ключа')

    def get_key_status(self):
        key_available = False
        allows_keys_query = AllowedKeys.select().where(AllowedKeys.user == self.person)
        allows_keys = []
        for record in allows_keys_query:
            allows_keys.append(record.key)
        if self.key in allows_keys:
            key_history = (
                KeysHistory.select().where(KeysHistory.key == self.key).order_by(
                    KeysHistory.date.desc()))
            if key_history.count() == 0 or key_history[0].this_return is True:
                key_available = True
        else:
            self.show_massage('ОШИБКА ДОСТУПА', "Данному пользователю не разрешен доступ к данному ключу")
        return key_available


class ReturnTheKeyWin(QtWidgets.QDialog, Ui_ReturnTheKeyWin):

    def __init__(self):
        # super(Ui_MainWindow, self).__init__()
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.person_name.setReadOnly(True)
        self.person_position.setReadOnly(True)
        self.building.setReadOnly(True)
        self.key_name.setReadOnly(True)

        self.key = None
        self.person = None

        self.person_id.setFocus()
        self.person_id.returnPressed.connect(self.fill_person_data)
        self.key_id.returnPressed.connect(self.fill_key_data)

    def fill_person_data(self):
        if self.person_id != '':
            try:
                self.person = Person.get(Person.guid == self.person_id.text())
                self.person_name.setText(self.person.name)
                self.person_position.setText(self.person.position)
                self.key_id.setFocus()
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Пользователь с данным ID не найден')
                self.person_id.setFocus()

    def fill_key_data(self):
        if self.key_id != '':
            try:
                self.key = Key.get(Key.guid == self.key_id.text())
                self.key_name.setText(self.key.name)
                building = Building.get_by_id(self.key.build_id)
                self.building.setText(building.name)
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Ключ с данным ID не найден')
                self.person_id.setFocus()

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()

    def accept(self):
        if self.buttonBox.hasFocus():
            if self.key is not None:
                key_available = self.get_key_status()
                try:
                    date = QDateTime.currentDateTime().toPyDateTime()
                    if self.person is None:
                        comment = self.comment_line.text()
                    else:
                        comment = 'Ключ возвращен: ' + self.person.name
                    new_key_history = KeysHistory(key=self.key, user=self.person, date=date, this_return=True,
                                                  comment=comment)
                    new_key_history.save()
                    self.show_massage('Success', 'Ключ успешно принят')
                    self.close()
                except Exception as err:
                    self.show_massage('Failed', 'Не удалось принять ключ')
                    print(err)

    def get_key_status(self):
        key_available = False
        key_history = (
            KeysHistory.select().where((KeysHistory.key == self.key)).order_by(
                KeysHistory.date.desc()))
        if key_history.count() == 0:
            self.show_massage('Предупреждение', 'Нет данных об истории выдачи этого ключа')
        else:
            if key_history[0].this_return is False:
                key_available = True
        return key_available


class ReportWin(QtWidgets.QWidget, Ui_ReportWin):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fill_persons_list()
        self.fill_keys_list()
        self.btn_generate_a_report.clicked.connect(self.generate_a_report)
        startday = datetime.datetime.today()
        startday = startday.combine(startday.date(), startday.min.time())
        self.date_from.setDateTime(startday)
        self.date1 = startday

        endday = datetime.datetime.today()
        endday = endday.replace(hour=23, minute=59, second=0, microsecond=0)
        self.date_to.setDateTime(endday)
        self.date2 = endday

        self.key = None
        self.person = None

        self.person_id.returnPressed.connect(self.fill_person_data)
        self.key_id.returnPressed.connect(self.fill_key_data)

    def fill_persons_list(self):
        query = Person.select(Person.name)
        personList = []
        for q in query:
            personList.append(q.name)
        completer = QCompleter(personList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.activated.connect(self.fill_person_id)
        self.person_name.setCompleter(completer)

    def fill_person_id(self):
        try:
            query = Person.select().where(Person.name == self.person_name.text())
            if query.count() > 1:
                self.show_massage('ОШИБКА!', 'Слишком много совпадений')
            elif query.count() == 1:
                self.person_id.setText(query[0].guid)
        except Exception as err:
            print(err)
            self.show_massage('ОШИБКА!', 'Ошибка поиска по имени')
            self.person_id.setFocus()

    def fill_keys_list(self):
        query = Key.select(Key.name, Key.build_id)
        keyList = []
        for q in query:
            key_name = str('[' + q.build_id.name + '] ' + q.name)
            keyList.append(key_name)
        completer = QCompleter(keyList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.key_name.setCompleter(completer)

    def fill_person_data(self):
        if self.person_id != '':
            try:
                self.person = Person.get(Person.guid == self.person_id.text())
                self.person_name.setText(self.person.name)
                self.key_id.setFocus()
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Пользователь с данным ID не найден')
                self.person_id.setFocus()

    def fill_key_data(self):
        if self.key_id != '':
            try:
                self.key = Key.get(Key.guid == self.key_id.text())
                self.key_name.setText(self.key.name)
            except Exception as err:
                print(err)
                self.show_massage('ОШИБКА!', 'Ключ с данным ID не найден')
                self.person_id.setFocus()

    def show_massage(self, title, massage_text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(massage_text)
        msgBox.exec()

    def generate_a_report(self):

        dates_are_filled = False
        try:
            datetime.datetime.strptime(str(self.date_from.date().toPyDate()), '%Y-%m-%d')
            datetime.datetime.strptime(str(self.date_to.date().toPyDate()), '%Y-%m-%d')
            self.date1 = self.date_from.dateTime().toPyDateTime()
            self.date2 = self.date_to.dateTime().toPyDateTime()
            dates_are_filled = True
        except Exception as err:
            print(err)

        if self.key is not None and self.person is None:

            if dates_are_filled:
                query = KeysHistory.select().where(
                    (KeysHistory.key == self.key) & (KeysHistory.date.between(self.date1, self.date2))).order_by(
                    KeysHistory.date)
            else:
                query = KeysHistory.select().where(KeysHistory.key == self.key).order_by(KeysHistory.date)
            self.fill_history_table(query)

        elif self.key is None and self.person is not None:

            query = KeysHistory.select().where(KeysHistory.user == self.person).order_by(KeysHistory.date)
            self.fill_history_table(query)

        elif self.key is not None and self.person is not None:

            query = KeysHistory.select().where(
                (KeysHistory.user == self.person) & (KeysHistory.key == self.key)).order_by(KeysHistory.date)
            self.fill_history_table(query)

        else:

            self.show_massage('Ошибка', 'Укажите параметры отбора')

    def fill_history_table(self, query):

        self.history_table.clear()
        self.history_table.setRowCount(0)
        if query.count() > 0:
            for q in query:
                currentRowCount = self.history_table.rowCount()
                self.history_table.insertRow(currentRowCount)
                # DATE|ThisReturn|KEY|PERSON|COMMENT
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, q.date.strftime("%d.%m.%Y %H:%M:%S"))
                self.history_table.setItem(currentRowCount, 0, QTableWidgetItem(item))
                str_this_return = 'x' if q.this_return else ''
                self.history_table.setItem(currentRowCount, 1, QTableWidgetItem(str_this_return))
                str_key = '[' + q.key.build_id.name + '] ' + q.key.name
                self.history_table.setItem(currentRowCount, 2, QTableWidgetItem(str_key))
                str_user = ''
                if q.user_id is not None:
                    str_user = '[' + str(q.user.guid) + '] ' + q.user.name
                self.history_table.setItem(currentRowCount, 3, QTableWidgetItem(str_user))
                self.history_table.setItem(currentRowCount, 4, QTableWidgetItem(str(q.comment)))
        self.history_table.resizeColumnsToContents()


class VahtaWindow(QtWidgets.QMainWindow, Ui_VahtaWindow):

    def __init__(self):
        # super(Ui_MainWindow, self).__init__()
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.btn_exit.clicked.connect(self.show_affirmative_dialogue)
        self.btn_give_the_key.clicked.connect(self.open_give_the_key_win)
        self.btn_key_report.clicked.connect(self.open_report_win)
        self.btn_return_the_key.clicked.connect(self.open_return_the_key_win)

    def open_give_the_key_win(self):
        self.give_the_key_WinUI = GiveTheKeyWin()
        self.give_the_key_WinUI.show()

    def open_return_the_key_win(self):
        self.return_the_key_WinUI = ReturnTheKeyWin()
        self.return_the_key_WinUI.show()

    def open_report_win(self):
        self.report_WinUI = ReportWin()
        self.report_WinUI.show()

    def show_affirmative_dialogue(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Вы действительно хотите выйти из программы?")
        msgBox.setWindowTitle("Подтвердите выход")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:
            self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # super(Ui_MainWindow, self).__init__()
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.btn_adm.clicked.connect(self.open_adm_ui)
        self.btn_vahta.clicked.connect(self.open_vahta_ui)
        self.btn_reports.clicked.connect(self.open_reports_ui)
        self.btn_exit.clicked.connect(self.show_affirmative_dialogue)

    def open_adm_ui(self):
        self.admWinUI = AdmWindow()
        self.admWinUI.show()

    def open_vahta_ui(self):
        self.vahtaWinUI = VahtaWindow()
        self.vahtaWinUI.show()

    def open_reports_ui(self):
        self.report_WinUI = ReportWin()
        self.report_WinUI.show()

    def show_affirmative_dialogue(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Вы действительно хотите выйти из программы?")
        msgBox.setWindowTitle("Подтвердите выход")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return_value = msgBox.exec()
        if return_value == QMessageBox.Ok:
            self.close()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(app.exec())
