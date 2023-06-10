import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class my_window(QMainWindow):
    def __init__(self):
        super(my_window,self).__init__()
        self.setGeometry(500,300,400,400)
        self.setFixedSize(400,400)
        self.setWindowTitle("App")
        self.initUI()

    def initUI(self):
        self.lbl1 = QtWidgets.QLabel(self)
        self.lbl1.setText('High:')
        self.lbl1.move(50,50)

        self.lbl2 = QtWidgets.QLabel(self)
        self.lbl2.setText('Low:')
        self.lbl2.move(50,90)

        self.txt1 = QtWidgets.QLineEdit(self)
        self.txt1.move(100,50)

        self.txt2 = QtWidgets.QLineEdit(self)
        self.txt2.move(100,90)

        self.lblC = QtWidgets.QLabel(self)
        self.lblC.setText('0.618 =>')
        self.lblC.move(250,50)

        self.lblD = QtWidgets.QLabel(self)
        self.lblD.setText('0.786 =>')
        self.lblD.move(250,90)

        self.lblE = QtWidgets.QLabel(self)
        self.lblE.setText('0.886 =>')
        self.lblE.move(250,130)

        self.valC = QtWidgets.QLabel(self)
        self.valC.move(300,50)

        self.valD = QtWidgets.QLabel(self)
        self.valD.move(300,90)

        self.valE = QtWidgets.QLabel(self)
        self.valE.move(300,130)

        self.btn_save = QtWidgets.QPushButton(self)
        self.btn_save.setText('Go')
        self.btn_save.clicked.connect(self.calculate)
        self.btn_save.move(100,130)
    
    def calculate(self):
        #print('Calculating...')
        if self.txt1.text() == "" or self.txt1.text() == None:
            self.txt1.setFocus()
            return
        if self.txt2.text() == "" or self.txt2.text() == None:
            self.txt2.setFocus()
            return
        high = float(self.txt1.text())
        low = float(self.txt2.text())
        if low > high:
            self.txt1.setFocus()
        else:
            C = float(high - (high - low) * 0.618)
            D = float(high - (high - low) * 0.786)
            E = float(high - (high - low) * 0.886)
            C = round(C,3)
            D = round(D,3)
            E = round(E,3)
            self.valC.setText(str(C))
            self.valD.setText(str(D))
            self.valE.setText(str(E))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return.value or event.key() == Qt.Key.Key_Enter.value:
            self.calculate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = my_window()
    win.show()
    sys.exit(app.exec())