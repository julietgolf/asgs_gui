import sys
from PyQt6.QtWidgets import QApplication
from .base import AppWindow,ParentWidget#, CSTORM_APP_INTERFACE
from .asgs.handlers import ASGS_API
from .asgs_widgets import ASGS_Run_Input
def run():
    app = QApplication(sys.argv)
    window=AppWindow(ParentWidget(run_widget=ASGS_Run_Input()))
    window.show()
    app.exec()
    ASGS_API.SHELL_ENVIRO.kill()

