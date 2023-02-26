import sys
import sqlite3

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class QDialogClass(QtWidgets.QDialog):
    def __init__(self, index, data, edit):
        super().__init__()
        self.update = {'id': '', 'name': '', 'grade': '', 'degree of roast': '', 'type': '', 'taste description': '',
                       'price': '', 'size': ''}
        self.index = index
        self.edit = edit
        uic.loadUi('addEditCoffeeForm.ui', self)

        if edit:
            print('fd')
            self.update = {}
            self.textEdit.setText(str(data[index][1]))
            self.textEdit_2.setText(data[index][2])
            self.textEdit_3.setText(str(data[index][3]))
            self.textEdit_4.setText(data[index][4])
            self.textEdit_6.setText(data[index][5])
            self.textEdit_8.setText(str(data[index][6]))
            self.textEdit_7.setText(str(data[index][7]))
        else:
            print('fw')
            self.textEdit.setText('Название')
            self.textEdit_2.setText('Название сорта')
            self.textEdit_3.setText('Степень обжарки')
            self.textEdit_4.setText('Молотый/в зернах')
            self.textEdit_6.setText('Описание вкуса')
            self.textEdit_8.setText('Цена')
            self.textEdit_7.setText('Размер')

        self.textEdit.textChanged.connect(lambda: self.save(par='name', val=self.textEdit.toPlainText()))
        self.textEdit_2.textChanged.connect(lambda: self.save(par='grade', val=self.textEdit_2.toPlainText()))
        self.textEdit_3.textChanged.connect(lambda: self.save(par='degree of roast', val=self.textEdit_3.toPlainText()))
        self.textEdit_4.textChanged.connect(lambda: self.save(par='type', val=self.textEdit_4.toPlainText()))
        self.textEdit_6.textChanged.connect(lambda: self.save(par='taste description', val=self.textEdit_6.toPlainText()))
        self.textEdit_8.textChanged.connect(lambda: self.save(par='price', val=self.textEdit_8.toPlainText()))
        self.textEdit_7.textChanged.connect(lambda: self.save(par='size', val=self.textEdit_7.toPlainText()))

        self.pushButton.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.write)

    def save(self, par=None, val=None):
        self.update[par] = val

    def write(self):
        cur = sqlite3.connect("coffee.sqlite")
        cur.cursor()
        if self.edit:
            for el in self.update:
                cur.execute(f'UPDATE info SET "{el}" = "{self.update[el]}" WHERE id = {self.index}')

        else:
             cur.execute(f'''INSERT INTO info ("id", "name", "grade", "degree of roast", "type", "taste description", "price", "size")
                         VALUES ("{self.update['id']}", "{self.update['name']}", "{self.update['grade']}",
                         "{self.update['degree of roast']}", "{self.update['type']}", "{self.update['taste description']}",
                         "{self.update['price']}", "{self.update['size']}");''')
        cur.commit()
        cur.close()
        self.accept()

    def exit(self):
        self.reject()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coffee.ui', self)
        con = sqlite3.connect("coffee.sqlite")

        cur = con.cursor()

        self.coffee_list = cur.execute("""SELECT * FROM info""").fetchall()
        cur.close()
        self.textBrowser.setText('ID')
        self.textBrowser_2.setText('Название сорта')
        self.textBrowser_6.setText('Степень обжарки')
        self.textBrowser_5.setText('Молотый/в зернах')
        self.textBrowser_3.setText('Описание вкуса')
        self.textBrowser_4.setText('Цена')
        self.textBrowser_8.setText('Объем упаковки')

        self.pushButton.clicked.connect(lambda: self.change_info(edit=True))
        self.pushButton_2.clicked.connect(lambda: self.change_info(edit=False))

        for coffee in self.coffee_list:
            self.comboBox.addItem(coffee[1])

        self.change()

        self.comboBox.currentIndexChanged.connect(self.change)

    def change(self):
        self.textEdit.setText(str(self.coffee_list[self.comboBox.currentIndex()][0]))
        self.textEdit_2.setText(self.coffee_list[self.comboBox.currentIndex()][2])
        self.textEdit_6.setText(str(self.coffee_list[self.comboBox.currentIndex()][3]))
        self.textEdit_5.setText(self.coffee_list[self.comboBox.currentIndex()][4])
        self.textEdit_3.setText(self.coffee_list[self.comboBox.currentIndex()][5])
        self.textEdit_4.setText(str(self.coffee_list[self.comboBox.currentIndex()][6]))
        self.textEdit_8.setText(str(self.coffee_list[self.comboBox.currentIndex()][7]))

    def change_info(self, edit):
        if edit:
            print('adfas')
            dialog = QDialogClass(self.comboBox.currentIndex(), self.coffee_list, True)
        else:
            print('fgdgfd')
            dialog = QDialogClass(self.comboBox.currentIndex(), self.coffee_list, False)
        dialog.exec_()
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        self.coffee_list = cur.execute("""SELECT * FROM info""").fetchall()
        cur.close()
        self.change()
        self.comboBox.clear()
        for coffee in self.coffee_list:
            self.comboBox.addItem(coffee[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())