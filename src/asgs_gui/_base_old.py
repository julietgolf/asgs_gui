import sys
import inspect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QMessageBox,
    QMainWindow, QDockWidget, QListView, QSpacerItem, QSizePolicy, QStackedWidget, 
    QComboBox, QStackedLayout
)
#from .handlers.utils import UtilsHandler
from .asgs.production_system import ProductionSystem

#utils = UtilsHandler()
ps = ProductionSystem()

#CSTORM_APP_INTERFACE={
#    "Interp":{
#        "Interp":utils.stacks
#    },
#    "Utils":{
#        "maxover63":None,
#        "split_fort63":None
#    },
#    "Plotters":{
#        "pltminmax63":utils.pltminmax63,
#        "pltadcout":utils.pltadcout,
#        "pltdepth":utils.pltdepth,
#        "pltstwave":None,
#        "stats":{
#            "hist":None,
#            "statplot":utils.statplot,
#            "test":utils.hello,
#        }
#    }
#}


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main widget setup
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        # Sidebar (DockWidget)
        self.sidebar = SidebarWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

        # Main layout
        self.layout = QVBoxLayout(self.main_widget)
        
        self.setWindowTitle("CSTORM GUI")

        # Sidebar navigation connections to Main widget
        self.sidebar.production_system_button.clicked.connect(lambda: self.main_widget.setCurrentWidget(self.main_widget.production_system_page))
        #self.sidebar.utils_button.clicked.connect(lambda: self.main_widget.setCurrentWidget(self.main_widget.utils_page))

class MainWidget(QStackedWidget):

    def __init__(self):
        super().__init__()

        #self.utils_page = UtilsWidget(CSTORM_APP_INTERFACE)
        self.production_system_page = ProductionSystemWidget()
        self.ps_dialog=PSCreateFileDialog()
        #self.addWidget(self.utils_page)
        self.addWidget(self.production_system_page)
        self.addWidget(self.ps_dialog)


class ProductionSystemWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self) # QStackedLayout()

        dialog_button = QPushButton("Create a file")
        run_button = QPushButton("Run the script")
        self.layout.addWidget(dialog_button)
        self.layout.addWidget(run_button)

        dialog_button.pressed.connect(self.ps_run)
        run_button.pressed.connect(ps.run_with_file)

    def ps_run(self):
        self.parent().setCurrentIndex(1)
        """        dialog = PSCreateFileDialog()
       if dialog.exec():
           try:
               dialog.set_arguments()
               result = dialog.production_system.create_input_file()
           except Exception as e:
               QMessageBox.critical(self, "Error", str(e)) """


class SidebarWidget(QDockWidget):

    def __init__(self):
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
        logo_label = QLabel("Logo Placeholder", self)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(logo_label)

        # --- Navigation Section ---
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(5)

        # Navigation buttons
        self.home_button = QPushButton("Home", self)
        self.production_system_button = QPushButton("Production System", self)
        self.utils_button = QPushButton("Utils", self)

        # Add buttons to navigation layout
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.production_system_button)
        nav_layout.addWidget(self.utils_button)

        # Add navigation layout to the main layout
        self.layout.addLayout(nav_layout)

        # --- Vertical Spacer ---
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        # --- Settings Button ---
        settings_button = QPushButton("Settings", self)
        self.layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignBottom)

        # Adjust the size
        self.setFixedWidth(150)

class PSCreateFileDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.production_system = ps
        self.setWindowTitle(f"Create CSTORM Input File")
        self.layout = QFormLayout(self)
        self.inputs = {}
        test_combo_box=QComboBox()
        test_combo_box.addItems(["one","two","three"])
        self.layout.addRow("Test Combo Box",test_combo_box)
        for name, parameter in self.production_system.parameters.items():
            label = QLabel(f"{parameter.pretty_name}", self)
            # label.setToolTip(f"Expecting {parameter.type_hint}")
            line_edit = QLineEdit(self, placeholderText=f"{parameter.default_value}", clearButtonEnabled=True)
            self.inputs[name] = line_edit
            self.layout.addRow(label, line_edit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        #self.buttons.accepted.connect(self.accept)
        #self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def set_arguments(self):
        for name, line_edit in self.inputs.items():
            text = line_edit.text()
            self.production_system.parameters[name].set_value(text)

