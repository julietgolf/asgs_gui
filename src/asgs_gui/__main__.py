import sys
from PyQt6.QtWidgets import QApplication
from .base import AppWindow,ParentWidget,SidebarWidget#, CSTORM_APP_INTERFACE
from .asgs.handlers import ASGS_API
from .asgs.widgets import ASGS_Run_Input,Settings_Widget
from functools import partial
def run():
    if True:
        app = QApplication(sys.argv)
        window=AppWindow(ParentWidget(run_widget=ASGS_Run_Input()))
        window.show()
        app.exec()
    else:
        #TODO Add settings
        app = QApplication(sys.argv)
        run_widget=ASGS_Run_Input()
        main=ParentWidget(run_widget=run_widget,settings=Settings_Widget())
        sidebar=SidebarWidget(["ASGS Main"],[partial(main.settop,"run_widget")],settings=True,settings_command=partial(main.settop,"settings"),width=100)
        window=AppWindow(main,sidebar=sidebar)
        window.show()
        app.exec()