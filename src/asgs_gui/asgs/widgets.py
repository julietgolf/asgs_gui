from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,   
    QPushButton, QLabel, QLineEdit, QDialog, QFormLayout, QDialogButtonBox,       
    QComboBox, QCheckBox,QHBoxLayout,QFileDialog
)
from .handlers import ASGS_API,ASGS_Run_Handler,ASGS_Settings_Handlers
INPUT_TYPES={"checkbox":QLineEdit,"combobox":QComboBox,"lineedit":QCheckBox}

class ASGS_Input_Basic(QWidget):
    def _set_combobox(self,var,mutable=True):
        label=QLabel(var.pretty_name)
        combo_box = QComboBox(self)
        combo_box.addItems([var.value,]+[option for option in var.options if option!=var.value])
        if not mutable:
            combo_box.setEnabled(False)
        self._layout.addRow(label, combo_box)

        self.inputs[var.name]=combo_box

    def _set_lineedit(self,var,mutable=True):
        label=QLabel(var.pretty_name)
        line_edit = QLineEdit(self, placeholderText=var.value, clearButtonEnabled=True)
        if not mutable:
            line_edit.setReadOnly(True)
        self._layout.addRow(label, line_edit)

        self.inputs[var.name]=line_edit

    def _set_checkbox(self,var,mutable=True):
        raise NotImplementedError("Add this you fucking moron") #TODO

    def __init__(self,handler=None,ok_button=True):
        super().__init__()
        self.handler=handler
        self.inputs={}
        self.setWindowTitle(f"Start Basic ASGS Runner")
        self._layout = QFormLayout()
        setter_dict={'combobox':self._set_combobox, 'lineedit':self._set_lineedit, 'checkbox':self._set_checkbox}
        for var_info in self.handler:
            setter_dict[var_info[1]](var_info[0],var_info[2])

        if ok_button:
            self.buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            self._layout.addRow(self.buttons)
        self.setLayout(self._layout)

class Profile_Save_Dialog(QDialog):
    def __init__(self,parent,message:str):
        super().__init__()

        self._parent=parent

        self.setWindowTitle("ASGS")

        layout = QFormLayout()
        layout.addRow(QLabel(message))
        self.line_edit = QLineEdit(self,placeholderText=str(parent.inputs["profile"].currentText()), clearButtonEnabled=True)
        layout.addRow("Profile Name",self.line_edit)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)
        self.setFixedSize(321,101+15*(len(message)>50))
        self.exec()

    def save(self):
        text=self.line_edit.text()
        if text:
            profile_combobox=self._parent.inputs["profile"]
            ASGS_API.save("profile",text,not self._parent._ca_change[1])
            index = profile_combobox.findText(self._parent.handler.var_hold_obj.variables["profile"].value)
            if index >= 0:
                profile_combobox.setCurrentIndex(index)
            else:
                profile_combobox.addItem(text)
                profile_combobox.setCurrentIndex(profile_combobox.count()-1)

                print(str(profile_combobox.currentText()))
        else:
            text=self.line_edit.placeholderText()
            ASGS_API.save("profile",text,not self._parent._ca_change[1])

        self._parent._ca_change[0]=True
        self._parent._ca_change[1]=True
        self.close()

class ASGS_Run_Input(ASGS_Input_Basic):

    def __init__(self):
        super(QWidget,self).__init__()
        self.handler=ASGS_Run_Handler()
        self.inputs={}
        self.setWindowTitle(f"Start Basic ASGS Runner")
        self._layout = QFormLayout()
        self._set_combobox(self.handler.get_var("profile"))

        self._config_layout=QHBoxLayout()

        for var in (self.handler.get_var("config_years"),self.handler.get_var("config")):
            combo_box = QComboBox(self)
            combo_box.addItems([var.value,]+[option for option in var.options if option!=var.value])
            self._config_layout.addWidget(combo_box)
            print("combo_box",var.name)
            self.inputs[var.name]=combo_box

        self._layout.addRow(QLabel(var.pretty_name),self._config_layout)
        self.inputs["config_years"].setFixedWidth(55)
        self._set_combobox(self.handler.get_var("adcirc"))
        self._set_combobox(self.handler.get_var("mesh"),False)

        self._button_layout=QHBoxLayout()
        
        cancel_button=QPushButton("Cancel")
        self._button_layout.addWidget(cancel_button)
        self.inputs["cancel"]=cancel_button

        save_button=QPushButton("Save")
        self._button_layout.addWidget(save_button)
        self.inputs["save"]=save_button

        run_button=QPushButton("Run")
        self._button_layout.addWidget(run_button)
        self.inputs["run"]=run_button
        self._layout.addRow(self._button_layout)

        self.inputs["profile"].currentTextChanged.connect(self.change_profile)
        self.inputs["config_years"].currentTextChanged.connect(self.change_config_years)
        self.inputs["config"].currentTextChanged.connect(self.change_config)
        self.inputs["adcirc"].currentTextChanged.connect(self.change_adcirc)
        cancel_button.clicked.connect(self.stop_run)
        save_button.clicked.connect(self.save_profile)
        run_button.clicked.connect(self.start_run)

        self.setLayout(self._layout)
        self.changedyear=False
        self._ca_change=[True,True]
        

    def change_profile(self):
        print("Chanfing profile")
        ASGS_API.load("profile",str(self.inputs["profile"].currentText()))
        print("Chanfing profile ")

        index = self.inputs["config_years"].findText(self.handler.var_hold_obj.variables["config_years"].value)
        print(index)
        if index >= 0:
            #SGS_API._set_config()
            self.inputs["config_years"].setCurrentIndex(index)
        else:
            print("fuck",self.handler.var_hold_obj.variables["config_years"].value)

        index = self.inputs["config"].findText(self.handler.var_hold_obj.variables["config"].value)
        print(index)
        if index >= 0:
            self.inputs["config"].setCurrentIndex(index)
        else:
            print("fuck",self.handler.var_hold_obj.variables["config"].value)
        

        index = self.inputs["mesh"].findText(self.handler.var_hold_obj.variables["mesh"].value)
        print(index)
        if index >= 0:
            self.inputs["mesh"].setCurrentIndex(index)
        else:
            print("coundlfind mesh")

        index = self.inputs["adcirc"].findText(self.handler.var_hold_obj.variables["adcirc"].value)
        print(index)
        if index >= 0:
            self.inputs["adcirc"].setCurrentIndex(index)
        else:
            print("coundlfind adcirc")

        self._ca_change[0]=True
        self._ca_change[1]=True

    def change_config_years(self):
        print("asgs")

        #self.changedyear=True
        ASGS_API._set_config_years(str(self.inputs["config_years"].currentText()))
        ASGS_API._set_options(ASGS_API.config)
        #self.changedyear=True
        self.inputs["config"].blockSignals(True)
        self.inputs["config"].clear()
        #self.changedyear=True

        self.inputs["config"].addItems([option for option in ASGS_API.config.options if option!=ASGS_API.config.value])
        #self.changedyear=True

        self.inputs["config"].setCurrentText("")
        self.inputs["config"].blockSignals(False)

    def change_config(self):
        config=self.inputs["config"].currentText()
        print(self.changedyear)
        if self.changedyear:
            self.changedyear=False
            
            return
        print("config")
        print(config)
        ASGS_API._set_config(config)
        index = self.inputs["mesh"].findText(self.handler.var_hold_obj.variables["mesh"].value)
        if index >= 0:
            print(index)
            self.inputs["mesh"].setCurrentIndex(index)
        else:
            print("coundlfind mesh")

        self._ca_change[0]=False

    def change_adcirc(self):
        print("adcirc")
        print(self.inputs["adcirc"].currentText())
        ASGS_API.load("adcirc",self.inputs["adcirc"].currentText()) 
        self._ca_change[1]=False

    def start_run(self):
        if not all(self._ca_change):
            print("GOOOD DDDANMIT")
            Profile_Save_Dialog(self,"Profile settings changed. Please save before running.")
            if not all(self._ca_change):
                return

        print("*LK* ... Nice")
        ASGS_API.run()

    def stop_run(self):
        ASGS_API._run_proc.terminate()
        ASGS_API._run_proc.kill()


    def save_profile(self):
        Profile_Save_Dialog(self,"Enter name to create a new profile or leave empty to\n update current.")


class Settings_Widget(ASGS_Input_Basic):
    def __init__(self,*args,**kwargs):
        super().__init__(ASGS_Settings_Handlers(),*args,**kwargs)

        self.inputs["asgs_home"].setText(self.handler.get_var("asgs_home").value)
        