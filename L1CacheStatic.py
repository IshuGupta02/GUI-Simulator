from PyQt5 import uic
from PyQt5.QtWidgets import *

class PacketWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        uic.loadUi("packet_details.ui", self)

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("qtDesigner.ui", self)
        self.show()

        self.pkt2.setEnabled(False)
        self.pkt3.setEnabled(False)
        self.pkt4.setEnabled(False)
        self.pkt5.setEnabled(False)
        self.pkt6.setEnabled(False)
        self.pkt7.setEnabled(False)

        self.pkt1.clicked.connect(self.displayPacket)

    def displayPacket(self):
        self.w = PacketWindow()
        self.w.show()

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__=='__main__':
    main()