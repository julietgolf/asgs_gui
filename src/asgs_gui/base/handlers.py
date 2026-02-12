from .base_types import DIALOGUE_INPUT_TYPE
from typing import TypeVar
from .var import Variable

#class _Handler_Var_Base:
#    __slots__=()
#
#class ComboBox_Var(_Handler_Var_Base):
#    def __init__(self,var,options: list=[]):
#        self.var
#
#class CheckBox_Var(_Handler_Var_Base):
#    def __init__(self,var,start_on: bool=True):
#        ...
#
#class LineEdit_Var(_Handler_Var_Base):
#    def __init__(self,var):
#        ...

V=TypeVar("Variable Holder")
class Generic_Handler:
    DEFAULT_INPUT_TYPE: DIALOGUE_INPUT_TYPE="lineedit"
    # Add a variable for default vals vars
    def __init_subclass__(cls,var_names:list,var_input_type: dict[str,DIALOGUE_INPUT_TYPE]={},immutable_vars: list[str]=[]):
        cls.VAR_NAMES=var_names
        cls.INPUT_INFO={key: [var_input_type.get(key,cls.DEFAULT_INPUT_TYPE), True if key not in immutable_vars else False] for key in var_names}
        
    def __init__(self,var_hold_obj: type[Variable],var_input_type:dict[str,DIALOGUE_INPUT_TYPE]={},immutable_vars: list[str]=[]):
        self.var_hold_obj=var_hold_obj

        # There is probably a better way to do this
        self.input_info=self.INPUT_INFO.copy()
        self.input_info.update({key : [var_input_type.get(key,self.input_info[key]), True if key not in immutable_vars else False] for key in list(set(var_input_type.keys()) | set(immutable_vars)) })

    def __iter__(self):
        return (self.get(var_name) for var_name in self.var_hold_obj.variables.keys())

    def get(self,var_name:str) -> list[type[Variable],str,bool]:
        return [self.var_hold_obj.variables[var_name],*self.input_info[var_name]]
    
    def get_var(self,var_name:str) -> type[Variable]:
        return self.var_hold_obj.variables[var_name]
        
    def get_input(self,var_name:str) -> str:
        return self.input_info[var_name][0]
        
    def get_mutable(self,var_name:str) -> bool:
        return self.input_info[var_name][1]

