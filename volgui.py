import sys
from PyQt5.QtWidgets import QApplication
from volgui_mainwin import VolGuiMainWindow


app = QApplication(sys.argv)
volgui = VolGuiMainWindow()
volgui.show()
rc = app.exec_()
sys.exit(rc)
