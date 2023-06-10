import sys
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator,self).__init__()
        self.setGeometry(300,300,465,400)
        self.setFixedSize(465,400)
        self.setWindowTitle("Calculator")
        self.initUI()
        self.result = None
        self.operation = 0
        self.first_num = None
        self.second_num = None
        self.index = -1 #index for second_num start
    
    def edit(self,val):
        self.numberLine.setText(self.numberLine.text()+val)

    def reset(self):
        self.index,self.operation,self.first_num,self.second_num = -1, 0, None, None  

    def set_operation(self,op):
        empty = False
        if self.numberLine.text() == "" or self.numberLine.text() == None:
            empty = True
        if op == 0: #clear
            self.numberLine.setText("")
            self.reset()
        else:
            if not empty and self.operation == 0 or (self.previous != None and empty):
                if not empty:
                    self.first_num = float(self.numberLine.text())
                else:
                    self.first_num = float(self.previous.text())
                match op:
                    case 1: #add
                        self.operation = 1
                        v = '+'
                    case 2: #sub
                        self.operation = 2
                        v = '-'
                    case 3: #mul
                        self.operation = 3
                        v = 'x'
                    case 4: #div
                        self.operation = 4
                        v = '/'
                self.numberLine.setText(self.numberLine.text()+v)
                self.index = len(self.numberLine.text())
                
    def calculate(self):
        if self.index != -1 and self.first_num != None and self.operation != 0:
            self.second_num = float(self.numberLine.text()[self.index:])
            match self.operation:
                case 1:
                    self.result = self.first_num + self.second_num
                case 2:
                    self.result = self.first_num - self.second_num
                case 3:
                    self.result = self.first_num * self.second_num
                case 4:
                    self.result = self.first_num / self.second_num
            self.first_num = self.result
            self.numberLine.setText(str(self.result))
            self.previous.setText(str(self.result))
            self.reset()

    def initUI(self):
        self.numberLine = QtWidgets.QLineEdit(self)
        self.numberLine.move(70,50)
        self.numberLine.resize(190,32)
        self.numberLine.setValidator(QDoubleValidator(999999,-999999,8))
        self.numberLine.setMaxLength(20)
        self.numberLine.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.previous = QtWidgets.QLabel(self)
        self.previous.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.previous.move(156,30)

        self.nine = QtWidgets.QPushButton(self)
        self.nine.setText('9')
        self.nine.clicked.connect(lambda: self.edit('9'))
        self.nine.move(216,90)
        self.nine.resize(45,30)

        self.eight = QtWidgets.QPushButton(self)
        self.eight.setText('8')
        self.eight.clicked.connect(lambda: self.edit('8'))
        self.eight.move(144,90)
        self.eight.resize(45,30)

        self.seven = QtWidgets.QPushButton(self)
        self.seven.setText('7')
        self.seven.clicked.connect(lambda: self.edit('7'))
        self.seven.move(69,90)
        self.seven.resize(45,30)

        self.six = QtWidgets.QPushButton(self)
        self.six.setText('6')
        self.six.clicked.connect(lambda: self.edit('6'))
        self.six.move(216,130)
        self.six.resize(45,30)

        self.five = QtWidgets.QPushButton(self)
        self.five.setText('5')
        self.five.clicked.connect(lambda: self.edit('5'))
        self.five.move(144,130)
        self.five.resize(45,30)

        self.four = QtWidgets.QPushButton(self)
        self.four.setText('4')
        self.four.clicked.connect(lambda: self.edit('4'))
        self.four.move(69,130)
        self.four.resize(45,30)

        self.three = QtWidgets.QPushButton(self)
        self.three.setText('3')
        self.three.clicked.connect(lambda: self.edit('3'))
        self.three.move(216,170)
        self.three.resize(45,30)

        self.two = QtWidgets.QPushButton(self)
        self.two.setText('2')
        self.two.clicked.connect(lambda: self.edit('2'))
        self.two.move(144,170)
        self.two.resize(45,30)

        self.one = QtWidgets.QPushButton(self)
        self.one.setText('1')
        self.one.clicked.connect(lambda: self.edit('1'))
        self.one.move(69,170)
        self.one.resize(45,30)

        self.zero = QtWidgets.QPushButton(self)
        self.zero.setText('0')
        self.zero.clicked.connect(lambda: self.edit('0'))
        self.zero.move(69,210)
        self.zero.resize(45,30)

        self.dot = QtWidgets.QPushButton(self)
        self.dot.setText('.')
        self.dot.clicked.connect(lambda: self.edit('.'))
        self.dot.move(144,210)
        self.dot.resize(45,30)

        self.equal = QtWidgets.QPushButton(self)
        self.equal.setText('=')
        self.equal.clicked.connect(self.calculate)
        self.equal.move(216,210)
        self.equal.resize(45,30)
        
        self.clear = QtWidgets.QPushButton(self)
        self.clear.setText('CE')
        self.clear.clicked.connect(lambda: self.set_operation(0))
        self.clear.move(300,50)

        self.add = QtWidgets.QPushButton(self)
        self.add.setText('+')
        self.add.clicked.connect(lambda: self.set_operation(1))
        self.add.move(300,90)

        self.sub = QtWidgets.QPushButton(self)
        self.sub.setText('-')
        self.sub.clicked.connect(lambda: self.set_operation(2))
        self.sub.move(300,130)

        self.mul = QtWidgets.QPushButton(self)
        self.mul.setText('x')
        self.mul.clicked.connect(lambda: self.set_operation(3))
        self.mul.move(300,170)

        self.div = QtWidgets.QPushButton(self)
        self.div.setText('/')
        self.div.clicked.connect(lambda: self.set_operation(4))
        self.div.move(300,210)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())