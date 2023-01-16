from PyQt5 import uic
from PyQt5.QtWidgets import *

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("qtDesigner.ui", self)
        self.show()

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__=='__main__':
    main()