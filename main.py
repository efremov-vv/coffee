import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coffee.ui', self)
        self.textBrowser.setText('ID')
        self.textBrowser_2.setText('Название сорта')
        self.textBrowser_6.setText('Степень обжарки')
        self.textBrowser_5.setText('Молотый/в зернах')
        self.textBrowser_3.setText('Описание вкуса')
        self.textBrowser_4.setText('Цена')
        self.textBrowser_8.setText('Объем упаковки')

        con = sqlite3.connect("coffee.sqlite")

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и получение всех результатов
        self.coffee_list = cur.execute("""SELECT * FROM info""").fetchall()

        for coffee in self.coffee_list:
            self.comboBox.addItem(coffee[1])

        self.comboBox.currentIndexChanged.connect(self.change)

    def change(self):
        self.textEdit.setText(str(self.coffee_list[self.comboBox.currentIndex()][0]))
        self.textEdit_2.setText(self.coffee_list[self.comboBox.currentIndex()][2])
        self.textEdit_6.setText(str(self.coffee_list[self.comboBox.currentIndex()][3]))
        self.textEdit_5.setText(self.coffee_list[self.comboBox.currentIndex()][4])
        self.textEdit_3.setText(self.coffee_list[self.comboBox.currentIndex()][5])
        self.textEdit_4.setText(str(self.coffee_list[self.comboBox.currentIndex()][6]))
        self.textEdit_8.setText(str(self.coffee_list[self.comboBox.currentIndex()][7]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())