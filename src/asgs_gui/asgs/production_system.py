import tempfile
import subprocess

class ProductionSystem:
    def __init__(self):
        self.script_path = ""

        self.Storm_Class = ProductionSystemVariable(
            "Storm_Class",
            default_value=None,
            pretty_name="Storm_Class",
            setter_func=lambda val: ProductionSystemVariable.set_Storm_Class(self.Storm_Class, val)
        )
        
        self.Storm_Type = ProductionSystemVariable(
            "Storm_Type",
            default_value=None,
            pretty_name="Storm_Type",
            setter_func=lambda val: ProductionSystemVariable.set_Storm_Type(self.Storm_Type, val)
        )
        
        self.Storm_Number = ProductionSystemVariable(
            "Storm_Number",
            default_value=None,
            pretty_name="Storm_Number",
            setter_func=lambda val: ProductionSystemVariable.set_Storm_Number(self.Storm_Number, val)
        )
        
        self.Tidal_Scenario = ProductionSystemVariable(
            "Tidal_Scenario",
            default_value=None,
            pretty_name="Tidal_Scenario",
            setter_func=lambda val: ProductionSystemVariable.set_Tidal_Scenario(self.Tidal_Scenario, val)
        )
        
        self.River_Cond = ProductionSystemVariable(
            "River_Cond",
            default_value=None,
            pretty_name="River_Cond",
            setter_func=lambda val: ProductionSystemVariable.set_River_Cond(self.River_Cond, val)
        )
        
        self.SeaLevel_Cond = ProductionSystemVariable(
            "SeaLevel_Cond",
            default_value=None,
            pretty_name="SeaLevel_Cond",
            setter_func=lambda val: ProductionSystemVariable.set_SeaLevel_Cond(self.SeaLevel_Cond, val)
        )
        
        self.Ice_Scenario = ProductionSystemVariable(
            "Ice_Scenario",
            default_value=None,
            pretty_name="Ice_Scenario",
            setter_func=lambda val: ProductionSystemVariable.set_Ice_Scenario(self.Ice_Scenario, val)
        )
        
        self.ADC_COLDHOT = ProductionSystemVariable(
            "ADC_COLDHOT",
            default_value=None,
            pretty_name="ADC_COLDHOT",
            setter_func=lambda val: ProductionSystemVariable.set_ADC_COLDHOT(self.ADC_COLDHOT, val)
        )
        
        self.GridConf_Packet = ProductionSystemVariable(
            "GridConf_Packet",
            default_value=None,
            pretty_name="GridConf_Packet",
            setter_func=lambda val: ProductionSystemVariable.set_GridConf_Packet(self.GridConf_Packet, val)
        )
        
        self.Sim_Run_Time = ProductionSystemVariable(
            "Sim_Run_Time",
            default_value=None,
            pretty_name="Sim_Run_Time",
            setter_func=lambda val: ProductionSystemVariable.set_Sim_Run_Time(self.Sim_Run_Time, val)
        )
        
        self.Email_Address = ProductionSystemVariable(
            "Email_Address",
            default_value=None,
            pretty_name="Email_Address",
            setter_func=lambda val: ProductionSystemVariable.set_Email_Address(self.Email_Address, val)
        )
        
        self.Waves_On = ProductionSystemVariable(
            "Waves_On",
            default_value=None,
            pretty_name="Waves_On",
            setter_func=lambda val: ProductionSystemVariable.set_Waves_On(self.Waves_On, val)
        )
        
        self.Viz_On = ProductionSystemVariable(
            "Viz_On",
            default_value=None,
            pretty_name="Viz_On",
            setter_func=lambda val: ProductionSystemVariable.set_Viz_On(self.Viz_On, val)
        )

        self.parameters = {}

        for name, value in self.__dict__.items():
            if isinstance(value, ProductionSystemVariable):
                self.parameters[value.name] = value
    
    # create the input file that will be used for running the script
    def create_input_file(self):
        with open("file.inp", "w") as file:
            file.write("\n".join([f"{parameter.name} = {parameter._value}" for name, parameter in self.parameters.items()]) + "\n")

    # run cstorm_master script with a file as input for the script
    def run_with_file(self):
        result = subprocess.run([self.script_path, "file.inp"])

class ProductionSystemVariable:

    def __init__(self, name, value=None, default_value=None, pretty_name=None, setter_func=None):
        self.name = name
        self.default_value = default_value
        self._value = value if value else self.default_value
        self.pretty_name = pretty_name
        self.setter_function = setter_func if setter_func else self.default_setter
    
    def set_value(self, value):
        self.setter_function(value)

    def default_setter(self, value):
        self._value = value

    # Unique Setters TODO
    def set_Storm_Class(self, value):
        self._value = value

    def set_Storm_Type(self, value):
        self._value = value

    def set_Storm_Number(self, value):
        self._value = value

    def set_Tidal_Scenario(self, value):
        self._value = value

    def set_River_Cond(self, value):
        self._value = value

    def set_SeaLevel_Cond(self, value):
        self._value = value

    def set_Ice_Scenario(self, value):
        self._value = value

    def set_ADC_COLDHOT(self, value):
        self._value = value

    def set_GridConf_Packet(self, value):
        self._value = value

    def set_Sim_Run_Time(self, value):
        self._value = value

    def set_Email_Address(self, value):
        self._value = value

    def set_Waves_On(self, value):
        self._value = value

    def set_Viz_On(self, value):
        self._value = value
    
