from PyQt5 import uic
from PyQt5.QtWidgets import *
from assets import parse

class PacketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("packet_details.ui", self)

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("qtDesigner.ui", self)
        self.show()
        self.data = parse.parse_data()
        self.queues = parse.queue_details()

        self.cycle=0

        self.total_cycles.setText(str(len(self.data)-1))
        self.current_cycle.setText("No started")

        self.Start.setEnabled(True)
        self.Start.clicked.connect(self.startDisplay)

        self.goToCycleBtn.clicked.connect(lambda : self.jumpCycle(self.goToCycle.text()))
        
    def displayPacket(self):
        self.w = PacketWindow()
        self.w.show()

    def displayCycle(self, cycle):
        if cycle<0:
            self.cycle = len(self.data)+cycle
            cycle = self.cycle
        elif cycle>= len(self.data):
            self.cycle = cycle % len(self.data)
            cycle = self.cycle
        else:
            self.cycle = cycle

        self.current_cycle.setText(str(self.cycle))
        print("displayCycle :", self.cycle)

        all_queues = self.data[cycle]

        for i, queue in enumerate(all_queues):
            queue_name = self.queues[i]
            
            for idx, pkt in enumerate(queue):
                buttonName = queue_name+"_"+str(idx+1)

                # remove this try except once ui changes in all queues is done
                try:
                    x = getattr(self, buttonName)
                    x.setText(pkt)
                    if pkt!="NaN":
                        x.setEnabled(True)
                except:
                    pass

            
    def enableSupportButtons(self):
        self.Next.setEnabled(True)
        self.Next.clicked.connect(lambda : self.nextCycle(1))

        self.Next_5.setEnabled(True)
        self.Next_5.clicked.connect(lambda : self.nextCycle(5))

        self.Next_10.setEnabled(True)
        self.Next_10.clicked.connect(lambda : self.nextCycle(10))

        self.Previous.setEnabled(True)
        self.Previous.clicked.connect(lambda : self.prevCycle(1))

        self.Previous_5.setEnabled(True)
        self.Previous_5.clicked.connect(lambda : self.prevCycle(5))

        self.Previous_10.setEnabled(True)
        self.Previous_10.clicked.connect(lambda : self.prevCycle(10))

    def startDisplay(self):
        self.displayCycle(0)
        self.enableSupportButtons()
    
    def nextCycle(self, inc=1):
        self.displayCycle(self.cycle+inc)

    def prevCycle(self, dec=1):
        self.displayCycle(self.cycle-dec)
    
    def jumpCycle(self, cycle=0):
        try:
            cycle = int(cycle)
        except:
            print("Please enter a valid cycle number")
            return

        self.displayCycle(cycle)

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__=='__main__':
    main()