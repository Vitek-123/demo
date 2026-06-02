from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from qt_material import apply_stylesheet

from db.Base import *
from window.python.auth import *
from window.python.guest import *
from window.python.cart import *
from window.python.admin_cart import *
from window.python.manager import *
from window.python.admin import *
from window.python.update_cart import *


class Auth(QWidget, Auth):
    def __init__(self):
        super().__init__()
        self.auth(self)
        icon = QtGui.QIcon(f"resourse/icon/img.ico")
        self.setWindowIcon(icon)
        self.label.setPixmap(QtGui.QPixmap(f"resourse/icon/img.ico"))

        self.pushButton.clicked.connect(self.go_in)
        self.pushButton_2.clicked.connect(self.go_guest)

    def go_guest(self):
        try:
            self.window = Guest()
            self.window.show()
            self.hide()
        except Exception as e:
            print(e)
    def go_in(self):
        try:
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()

            user = Base().select_client(login, password)
            if not all([login, password]):
                QMessageBox.warning(self, "", "Заполните все поля")
                return

            if not user:
                QMessageBox.warning(self, "", "Неверный логин или пароль")
                return

            if user[6] == 1:
                self.window = Client(user)
                self.window.show()
                self.hide()
            elif user[6] == 2:
                self.window = Manager(user)
                self.window.show()
                self.hide()
            elif user[6] == 3:
                self.window = Admin(user)
                self.window.show()
                self.hide()
        except Exception as e:
                print(e)


class Guest(QWidget, Gues):
    def __init__(self):
        super().__init__()
        self.gues(self)
        icon = QtGui.QIcon(f"resourse/icon/img.ico")
        self.setWindowIcon(icon)

        self.interface()

        self.vertical_layout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.select_all()

        self.pushButton.clicked.connect(self.exit)
    def interface(self):
        self.label.setText("Гостевой режим")
        self.pushButton.setText("Выход")

    def select_all(self):
        try:
            self.clear_layout()

            for tovar in Base().select_tovar():
                cart = Cart(tovar)
                self.vertical_layout.addWidget(cart)
        except Exception as e:
            print(e)

    def clear_layout(self):
        try:
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        except Exception as e:
            print(e)

    def exit(self):
        self.window = Auth()
        self.window.show()
        self.hide()


class Client(QWidget, Gues):
    def __init__(self, info):
        super().__init__()
        self.gues(self)
        self.info = info
        icon = QtGui.QIcon(f"resourse/icon/img.ico")
        self.setWindowIcon(icon)

        self.interface()

        self.vertical_layout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.select_all()

        self.pushButton.clicked.connect(self.exit)
    def interface(self):
        self.label.setText(f"{self.info[1]} {self.info[2]}")
        self.pushButton.setText("Выход")

    def select_all(self):
        try:
            self.clear_layout()

            for tovar in Base().select_tovar():
                cart = Cart(tovar)
                self.vertical_layout.addWidget(cart)
        except Exception as e:
            print(e)

    def clear_layout(self):
        try:
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        except Exception as e:
            print(e)

    def exit(self):
        self.window = Auth()
        self.window.show()
        self.hide()


class Manager(QWidget, Manager):
    def __init__(self, info):
        super().__init__()
        self.manager(self)
        self.info = info
        icon = QtGui.QIcon(f"resourse/icon/img.ico")
        self.setWindowIcon(icon)

        self.interface()

        self.vertical_layout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.select_all()

        self.pushButton.clicked.connect(self.exit)

        self.lineEdit_find.textChanged.connect(self.select_all)
        self.comboBox_filter.currentTextChanged.connect(self.select_all)
        self.comboBox_sort.currentTextChanged.connect(self.select_all)
    def interface(self):
        self.label.setText(f"{self.info[1]} {self.info[2]}")

        self.comboBox_sort.addItem("Без сортировки", 0)
        self.comboBox_sort.addItem("Наибольшее количсетво", 1)
        self.comboBox_sort.addItem("Наименьшее количество", 2)

        self.comboBox_filter.addItem("Все поставщики", 0)
        for i in Base().select_supplier():
            self.comboBox_filter.addItem(i[1], i[0])


    def select_all(self):
        try:
            self.clear_layout()

            find = self.lineEdit_find.text()
            filter = self.comboBox_filter.currentData()
            sort = self.comboBox_sort.currentData()

            for tovar in Base().select_tovar(find, filter, sort):
                cart = Cart(tovar)
                self.vertical_layout.addWidget(cart)
        except Exception as e:
            print(e)

    def clear_layout(self):
        try:
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        except Exception as e:
            print(e)

    def exit(self):
        self.window = Auth()
        self.window.show()
        self.hide()


class Admin(QWidget, Admin):
    def __init__(self, info):
        super().__init__()
        self.admin(self)
        self.info = info
        icon = QtGui.QIcon(f"resourse/icon/img.ico")
        self.setWindowIcon(icon)

        self.interface()

        self.vertical_layout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.select_all()

        self.pushButton.clicked.connect(self.exit)
        self.pushButton_3.clicked.connect(self.add_tovar)

        self.lineEdit_find.textChanged.connect(self.select_all)
        self.comboBox_filter.currentTextChanged.connect(self.select_all)
        self.comboBox_sort.currentTextChanged.connect(self.select_all)
    def interface(self):
        self.label.setText(f"{self.info[1]} {self.info[2]}")

        self.comboBox_sort.addItem("Без сортировки", 0)
        self.comboBox_sort.addItem("Наибольшее количсетво", 1)
        self.comboBox_sort.addItem("Наименьшее количество", 2)

        self.comboBox_filter.addItem("Все поставщики", 0)
        for i in Base().select_supplier():
            self.comboBox_filter.addItem(i[1], i[0])

    def add_tovar(self):
        try:
            self.window = AddTovar(self)
            self.window.show()
        except Exception as e:
            print(e)

    def select_all(self):
        try:
            self.clear_layout()

            find = self.lineEdit_find.text()
            filter = self.comboBox_filter.currentData()
            sort = self.comboBox_sort.currentData()

            for tovar in Base().select_tovar(find, filter, sort):
                cart = ManagerCart(tovar, self)
                self.vertical_layout.addWidget(cart)
        except Exception as e:
            print(e)

    def clear_layout(self):
        try:
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        except Exception as e:
            print(e)

    def exit(self):
        self.window = Auth()
        self.window.show()
        self.hide()


class Cart(QWidget, Cart):
    def __init__(self, info):
        super().__init__()
        self.cart(self)
        self.info = info

        self.interface()

    def interface(self):
        try:
            if self.info[10] > 15:
                self.setStyleSheet("QWidget{background-color: rgb(46, 139, 87);}")

            if self.info[10] > 0:
                self.label_12.setStyleSheet('text-decoration: line-through; color: red;')
                price = float(self.info[7])
                sale = int(self.info[10])
                new_price = price - (price / 100 * sale)
                self.label_17.setText(f"{new_price}")
            else:
                self.label_17.setText("")


            if self.info[2]:
                self.label.setPixmap(QtGui.QPixmap(f"resourse/images/{self.info[2]}").scaled(300, 200))
            else:
                self.label.setPixmap(QtGui.QPixmap(f"resourse/icon/img.ico"))

            self.label_2.setText(f"{self.info[8]}|{self.info[1]}")
            self.label_9.setText(f"{self.info[3]}")
            self.label_10.setText(f"{self.info[14]}")
            self.label_11.setText(f"{self.info[16]}")
            self.label_12.setText(f"{self.info[7]}")
            self.label_13.setText(f"{self.info[8]}")
            self.label_14.setText(f"{self.info[9]}")
            self.label_16.setText(f"{self.info[10]}")
        except Exception as e:
            print(e)


class ManagerCart(QWidget, AdminCart):
    def __init__(self, info, parent = None):
        super().__init__()
        self.admincart(self)
        self.info = info
        self.parent = parent

        self.interface()

        self.pushButton_2.clicked.connect(lambda _, id = self.info[0]: self.delete_tovar(id))
        self.pushButton.clicked.connect(lambda _, info=self.info: self.update_tovar(info))

    def interface(self):
        try:
            if self.info[10] > 15:
                self.setStyleSheet("QWidget{background-color: rgb(46, 139, 87);}")

            if self.info[10] > 0:
                self.label_12.setStyleSheet('text-decoration: line-through; color: red;')
                price = float(self.info[7])
                sale = int(self.info[10])
                new_price = price - (price / 100 * sale)
                self.label_17.setText(f"{new_price}")
            else:
                self.label_17.setText("")


            if self.info[2]:
                self.label.setPixmap(QtGui.QPixmap(f"resourse/images/{self.info[2]}").scaled(300, 200))
            else:
                self.label.setPixmap(QtGui.QPixmap(f"resourse/icon/img.ico"))

            self.label_2.setText(f"{self.info[8]}|{self.info[1]}")
            self.label_9.setText(f"{self.info[3]}")
            self.label_10.setText(f"{self.info[14]}")
            self.label_11.setText(f"{self.info[16]}")
            self.label_12.setText(f"{self.info[7]}")
            self.label_13.setText(f"{self.info[8]}")
            self.label_14.setText(f"{self.info[9]}")
            self.label_16.setText(f"{self.info[10]}")
        except Exception as e:
            print(e)

    def delete_tovar(self, id):
        try:
            result = Base().delete_tovar(id)
            if result == False:
                QMessageBox.information(self, '', "Товар добавлен в заказ, невозможно удалить")
                return
            QMessageBox.information(self, "", "товар успешно удален")
            self.parent.select_all()
        except Exception as e:
            print(e)

    def update_tovar(self, info):
        try:
            self.window = UpdateCar(info, self.parent)
            self.window.show()
        except Exception as e:
            print(e)


class UpdateCar(QWidget, UpdateCart):
    def __init__(self, info, parent = None):
        super().__init__()
        self.updatecart(self)
        self.info = info
        self.parent = parent

        self.interface()

        self.pushButton_2.clicked.connect(self.exit)
        self.pushButton.clicked.connect(self.update_tovar)
        self.pushButton_photo.clicked.connect(self.choose_photo)

    def interface(self):
        try:
            self.lineEdit.setEnabled(False)

            self.lineEdit_2.setText(f"{self.info[1]}")
            self.textEdit.setText(f"{self.info[3]}")
            self.lineEdit.setText(f"{self.info[2]}")
            self.doubleSpinBox.setValue(float(self.info[7]))
            self.lineEdit_3.setText(f"{self.info[8]}")
            self.spinBox.setValue(int(self.info[9]))
            self.spinBox_2.setValue(int(self.info[10]))

            for cat in Base().select_category():
                self.comboBox.addItem(cat[1], cat[0])

            for cat in Base().select_manuract():
                self.comboBox_2.addItem(cat[1], cat[0])

            for cat in Base().select_supplier():
                self.comboBox_3.addItem(cat[1], cat[0])
        except Exception as e:
            print(e)

    def update_tovar(self):
        try:
            title = self.lineEdit_2.text()
            photo = self.lineEdit.text()
            desc = self.textEdit.toPlainText()
            category = self.comboBox.currentData()
            manuf = self.comboBox_2.currentData()
            supplier = self.comboBox_3.currentData()
            price = self.doubleSpinBox.value()
            unit = self.lineEdit_3.text()
            count = self.spinBox.value()
            sale = self.spinBox_2.value()

            if not all([title, photo, desc, category, manuf, supplier, price, unit,]):
                QMessageBox.warning(self, "", "Заполните все поля")
                return

            result = Base().update_tovar(title, photo, desc, category, manuf, supplier, price, unit, count, sale, self.info[0])
            if result:
                QMessageBox.information(self, "", "Товар успешно обновлен")
                self.parent.select_all()

        except Exception as e:
            print(e)



    def choose_photo(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "", "", "*jpg")
            if file_name:
                self.lineEdit.setText(f"{file_name[0].split("/")[-1]}")
        except Exception as e:
            print(e)
    def exit(self):
        self.hide()


class AddTovar(QWidget, UpdateCart):
    def __init__(self, parent = None):
        super().__init__()
        self.updatecart(self)
        self.parent = parent

        self.interface()

        self.pushButton_2.clicked.connect(self.exit)
        self.pushButton.clicked.connect(self.update_tovar)
        self.pushButton_photo.clicked.connect(self.choose_photo)

    def interface(self):
        try:
            self.lineEdit.setEnabled(False)

            for cat in Base().select_category():
                self.comboBox.addItem(cat[1], cat[0])

            for cat in Base().select_manuract():
                self.comboBox_2.addItem(cat[1], cat[0])

            for cat in Base().select_supplier():
                self.comboBox_3.addItem(cat[1], cat[0])
        except Exception as e:
            print(e)

    def update_tovar(self):
        try:
            title = self.lineEdit_2.text()
            photo = self.lineEdit.text()
            desc = self.textEdit.toPlainText()
            category = self.comboBox.currentData()
            manuf = self.comboBox_2.currentData()
            supplier = self.comboBox_3.currentData()
            price = self.doubleSpinBox.value()
            unit = self.lineEdit_3.text()
            count = self.spinBox.value()
            sale = self.spinBox_2.value()

            if not all([title, photo, desc, category, manuf, supplier, price, unit,]):
                QMessageBox.warning(self, "", "Заполните все поля")
                return

            result = Base().add_tovar(title, photo, desc, category, manuf, supplier, price, unit, count, sale)
            if result:
                QMessageBox.information(self, "", "Товар успешно добавлен")
                self.parent.select_all()

        except Exception as e:
            print(e)



    def choose_photo(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "", "", "*jpg")
            if file_name:
                self.lineEdit.setText(f"{file_name[0].split("/")[-1]}")
        except Exception as e:
            print(e)
    def exit(self):
        self.hide()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_purple.xml")
    window = Auth()
    window.show()
    sys.exit(app.exec())