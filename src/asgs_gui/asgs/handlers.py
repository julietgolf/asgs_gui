from ..base.var import Variable,Var_Bin
from ..base.handlers import Generic_Handler
import subprocess as sp
from typing import Literal
import re
from pathlib import Path
from ..base.base_types import DIALOGUE_INPUT_TYPE
#TODO Turn this into a module
#TODO Transition from inputs to sb

ASGS_BASE_DIR=Path("/root/asgs/asgs_gui/asgs_gui/test2/opt/test_gui")



class ASGS_API:
    SHELL_ENVIRO=sp.Popen(["bash"],stdin=sp.PIPE,stdout=sp.PIPE)
    @classmethod
    def _tmp_load(cls,param:str,name:str):
        cls.SHELL_ENVIRO.stdin.write(bytes(f". {ASGS_BASE_DIR/param/name}\n","utf-8"))
        cls.SHELL_ENVIRO.stdin.flush()

    @classmethod
    def _get_mesh(cls):
        print("_get_mesh")
        with sp.Popen(["bash"],stdin=sp.PIPE,stdout=sp.PIPE) as proc:
            proc.stdin.write(bytes(f". {cls.config.value}\n","utf-8"))
            proc.stdin.flush()

            proc.stdin.write(bytes("printf \"$GRIDNAME\n\"\n","utf-8"))
            proc.stdin.flush()
            return proc.stdout.readline().decode("utf-8").strip()
    
    @classmethod
    def _get_config(cls):
        print("_get_config")
        cls.SHELL_ENVIRO.stdin.write(bytes("printf \"(info) ASGS_CONFIG is defined as \'${ASGS_CONFIG}\'\n\"\n","utf-8"))
        cls.SHELL_ENVIRO.stdin.flush()

        return re.findall(r"(?<=').*(?=')",cls.SHELL_ENVIRO.stdout.readline().decode("utf-8").strip())[0]
    
    @classmethod
    def _get_profile(cls):
        print("_get_profile")
        cls.SHELL_ENVIRO.stdin.write(bytes("printf \"(info) PROFILE_NAME is defined as \'${PROFILE_NAME}\'\n\"\n","utf-8"))
        cls.SHELL_ENVIRO.stdin.flush()

        return re.findall(r"(?<=').*(?=')",cls.SHELL_ENVIRO.stdout.readline().decode("utf-8").strip())[0]
    
    
    @classmethod
    def _get_adcirc(cls):
        print("_get_adcirc")
        cls.SHELL_ENVIRO.stdin.write(bytes("printf \"(info) ADCIRC_PROFILE_NAME is defined as \'${ADCIRC_PROFILE_NAME}\'\n\"\n","utf-8"))
        cls.SHELL_ENVIRO.stdin.flush()

        return re.findall(r"(?<=').*(?=')",cls.SHELL_ENVIRO.stdout.readline().decode("utf-8").strip())[0]

    @classmethod
    def _set_config(cls,config=None):
        print("setting")
        if config is None:
            config=cls._get_config()
        cls.config.value=config
        cls.mesh.value=cls._get_mesh()

    @classmethod
    def _set_profile(cls,profile):
        cls.profile.value=profile
        cls._set_config()

    @classmethod
    def _set_options(cls,var: Variable):
        with open(f"{var.name}.fake") as fake_input:
            result=fake_input.readlines()
        var.options=[val.split()[-1].strip() for val in result]

    @classmethod
    def _init(cls):
        current_profile=cls._get_profile()
        cls.profile=Variable("profile",current_profile,"Profile",current_profile)
        cls._set_options(cls.profile)
        print(cls.profile)
        current_config=cls._get_config()
        cls.config=Variable("config",current_config,"Config",current_config)
        cls._set_options(cls.config)
        print(cls.config)
        #echo $ADCIRC_PROFILE_NAME
        current_adcirc=cls._get_adcirc()
        cls.adcirc=Variable("adcirc",current_adcirc,"ADCIRC",current_adcirc)
        cls._set_options(cls.adcirc)
        print(cls.adcirc)
        current_mesh=cls._get_mesh()
        cls.mesh=Variable("mesh",current_mesh,"Mesh",current_mesh)
        cls._set_options(cls.mesh)
        print(cls.mesh)
    
    def __new__(cls):
        return cls

    @classmethod
    def _refresh_options(cls):
        cls._set_options(cls.profile)
        cls._set_options(cls.config)
        cls._set_options(cls.adcirc)
        cls._set_options(cls.mesh)

    @classmethod
    def _reset(cls):
        cls.profile.set_default()
        cls.config.set_default()
        cls.adcirc.set_default()
        cls.mesh.set_default()
        cls._refresh_options()

    @classmethod
    def load(cls,param:str,name:str):
        cls._tmp_load(param,name)
        if param=="profile":
            if name in cls.profile.options:
                cls._set_profile(name)
                #TODO reset cls.config.value
            else:
                raise ValueError(f"{name} is not a valid option for {cls.profile}")
        elif param=="adcirc":
            if name in cls.adcirc.options:
                cls.adcirc.value=cls._get_adcirc()
            else:
                raise ValueError(f"{name} is not a valid option for {cls.adcirc}")


    @classmethod
    def run(cls):
        ...

    @classmethod
    def define(cls,param:Literal["adcircdir", "adcircbranch", "adcircremote", "config", "editor", "hostfile", "scratchdir", "scriptdir", "workdir"], value: str):
        if param=="config":
            cls.SHELL_ENVIRO.stdin.write(bytes(f"export ASGS_CONFIG={value}\n","utf-8"))
            cls._set_config(value)

    @classmethod
    def init(cls):
        ...

    @classmethod    
    def save(cls,param:str,name:str):
        print(f"saved {param} {name}")
        with open(ASGS_BASE_DIR/param/name,"w") as file:
            file.writelines([
                f"export ASGS_CONFIG={cls.config.value}\n",
                f"export ADCIRC_PROFILE_NAME={cls.adcirc.value}\n",
                f"export PROFILE_NAME={name}\n"
            ])

        with open(ASGS_BASE_DIR/f"{param}.fake","a") as file:
            file.write(f"1. {name}\n")

        cls.profile.add_option(name)

        cls._set_profile(name)
        
        


    @classmethod    
    def list(cls,param: Literal['adcirc', 'configs', 'meshes', 'platforms', 'profiles']) -> list[str]:
        input(f"Place result of list {param} in input.fake")
        with open("input.fake") as fake_input:
            result=fake_input.readlines()
        
        return [val.split()[-1].strip() for val in result]

    @classmethod
    def get_results(cls):
        ...
        # This is a place holder

ASGS_API._init()

#Final Form
# Simple Run where the profile, config, adcirc, and maybe one or two other things
# Config editor. Simialar to whats online, but additionally can select the profile and adcirc. Really a profile editor
# Result viewer. A mix between matplotlib and a terminal/file explorer
# Settings. TBD

class ASGS_API_Bin(Var_Bin):
    INSTANCE=None
    def __new__(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE=super().__new__(cls)
        return cls.INSTANCE

    def __init__(self):
        super().__init__(
            "ASGS API Bin",
            profile=ASGS_API.profile,
            config=ASGS_API.config,
            adcirc=ASGS_API.adcirc,
            mesh=ASGS_API.mesh,
        )

class ASGS_Run_Handler(Generic_Handler,
                       var_names=["profile","config","adcirc","mesh"],
                       var_input_type={"profile":'combobox',"config":'combobox',"adcirc":'combobox',"mesh":'combobox'},
                       immutable_vars=["mesh"]
                      ):
    def __init__(self,var_input_type:dict[str,DIALOGUE_INPUT_TYPE]={},immutable_vars: list[str]=[]):
        super().__init__(ASGS_API_Bin(),var_input_type,immutable_vars)

