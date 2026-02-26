from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QMessageBox,
    QMainWindow, QDockWidget, QListView, QSpacerItem, QSizePolicy, QStackedWidget, 
    QComboBox, QStackedLayout
)
from collections.abc import Callable
from typing import Literal
from .base_types import SIGNALS_TYPE


class AppWindow(QMainWindow):
    def __init__(self,mainwidget,sidebar=None,name:str="APP"):
        """Generic main window with a sidebar and one widget"""
        super().__init__()

        # Main widget setup
        self.main_widget = mainwidget
        self.setCentralWidget(self.main_widget)

        # Sidebar (DockWidget)
        if sidebar is not None:
            self.sidebar = sidebar
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

        ## Main layout
        #self.layout = QVBoxLayout(self.main_widget)
        
        self.setWindowTitle(name)

class ParentWidget(QStackedWidget):
    def __init__(self,name:str="ParentWidget",**widgets):
        """Generic stacked widget"""
        super().__init__()
        self._widgets={}
        self.name=name
        for i,name in enumerate(widgets):
            self._widgets[name]=(widgets[name],i)
            self.addWidget(widgets[name])

    def settop(self,widget: str | int):
        """Moves a widget to the top."""
        if isinstance(widget,str):
            widget=self._widgets[widget][0]
        print(widget)
        self.setCurrentWidget(widget)

    def __index__(self,key):
        try:
            return self._widgets[key]
        except KeyError:
            raise KeyError(f"Widget {key} is not a member of {self.name}.")
        except:
            raise

class SidebarWidget(QDockWidget):

    def __init__(self,buttons: list,
                 commands: list[Callable | None] | None=None,
                 signals: list[SIGNALS_TYPE] | SIGNALS_TYPE | None=None,
                 *,
                 logo: str=None,
                 settings: bool=False,
                 settings_signal: SIGNALS_TYPE | None=None,
                 settings_command: Callable| None=None,
                 width: int=150
                 ):
        super().__init__()

        # Widget Setup
        self.widget = QListView()
        self.setWidget(self.widget)

        # Set TitleBar to empty widget because we don't need dock features
        # Alternatively, can add a Title widget, and uncomment the setFeatures line
        self.setTitleBarWidget(QWidget())
        #self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Main layout of the sidebar
        self.layout = QVBoxLayout(self.widget)
        self.setLayout(self.layout)
        #layout.setContentsMargins(0, 0, 0, 0)
        #layout.setSpacing(10)

        # --- Logo Section ---
        if logo is not None:
            logo_label = QLabel(logo, self)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(logo_label)

        # --- Navigation Section ---
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(5)
        self.nav_buttons: list[QVBoxLayout]=[]

        for button in buttons:
            # Navigation buttons
            self.nav_buttons.append(QPushButton(button))

            # Add buttons to navigation layout
            nav_layout.addWidget(self.nav_buttons[-1])

        # Add navigation layout to the main layout
        self.layout.addLayout(nav_layout)

        if commands is not None:
            if len(commands)!=len(buttons):
                raise ValueError(f"{len(commands)} signals were provided, but {len(buttons)} are needed.")
            
            if not isinstance(signals,list):
                if signals is None:
                    signals="clicked"
                call_signals=[signals for i in range(len(commands))]
            else:
                if len(signals)!=len(buttons):
                    raise ValueError(f"{len(signals)} signals were provided, but {len(buttons)} are needed.")
                call_signals=[signal if signal is not None else "clicked" for signal in signals]

            for (button,command,signal) in zip(self.nav_buttons,commands,call_signals):
                getattr(button,signal).connect(command)

        # --- Settings Section ---
        if settings:
            spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.layout.addItem(spacer)

            # --- Settings Button ---
            settings_button = QPushButton("Settings")
            self.layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignBottom)
            if settings_signal is None:
                    settings_signal="clicked"
            getattr(settings_button,settings_signal).connect(settings_command)

        # Adjust the size
        self.setFixedWidth(width)