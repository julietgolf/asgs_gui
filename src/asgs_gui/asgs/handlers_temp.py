from ..base.var import Variable,Var_Bin
from ..base.handlers import Generic_Handler
import subprocess as sp
from typing import Literal
import re
from pathlib import Path
from ..base.base_types import DIALOGUE_INPUT_TYPE
from .env_var import ENV_Var_File
import os
#TODO Turn this into a module
#TODO Transition from inputs to sb

class ASGS_API:
    @classmethod
    def _shell_command(cls,command:str):
        cls.SHELL_ENVIRO.stdin.write(bytes(command+"\necho \"SHELL_ENVIRO FINISHED\"\n","utf-8"))
        cls.SHELL_ENVIRO.stdin.flush()
        print("running command")
        output=b""
        for line in iter(cls.SHELL_ENVIRO.stdout.readline, b""):
            if b"SHELL_ENVIRO FINISHED" in line:
                break
            output+=line
        print(output)
        return output.decode("utf-8")

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
        return re.findall(r"(?<=').*(?=')",cls.show("config").strip())[0]
    
    @classmethod
    def _get_profile(cls):
        print("_get_profile")
        return re.findall(r"(?<=').*(?=')",cls.show("profile").strip())[0]
    
    
    @classmethod
    def _get_adcirc(cls):
        print("_get_adcirc")
        return os.getenv("ADCIRC_PROFILE_NAME")

    @classmethod
    def _set_mesh(cls,mesh=None):
        if mesh is None:
            mesh=cls._get_mesh()
        cls.mesh.value=mesh

    @classmethod
    def _set_adcirc(cls,adcirc=None):
        if adcirc is None:
            adcirc=cls._get_adcirc()
        cls._set_adcirc(adcirc)

    @classmethod
    def _set_config(cls,config=None):
        print("setting")
        if config is None:
            config=cls._get_config()
        cls.config.value=config
        cls._set_mesh(cls._get_mesh())

    @classmethod
    def _set_profile(cls,profile):
        cls.profile.value=profile
        cls._set_config()

    @classmethod
    def _set_options(cls,var: Variable):
        if var.name!="config":
            result=cls.list(cls._PARAM_PLURALS[var.name])
            print(result)
            var.options=[val.split()[-1].strip() for val in result if val]
        else:
            with open(f"{var.name}.fake") as fake_input:
                result=fake_input.readlines()
                var.options=[val.split()[-1].strip() for val in result if val]


    @classmethod
    def _init(cls):
        cls._PARAM_PLURALS={"profile":"profiles","mesh":"meshes","adcirc":"adcircs"}
        cls.SHELL_ENVIRO=sp.Popen([Path(os.getenv("ASGS_HOME"))/"asgsh"],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT,bufsize=1)

        cls.SHELL_ENVIRO.stdin.write(b"\necho 'INITIALIZED'\n")
        cls.SHELL_ENVIRO.stdin.flush()

        for line in iter(cls.SHELL_ENVIRO.stdout.readline, b""):
            print(line.decode())
            if b"INITIALIZED" in line:
                break
        
        print("running")
        cls.load("profile","default-asgs")
        current_profile=cls._get_profile()
        cls.profile=Variable("profile",current_profile,"Profile",current_profile)
        cls._pro_file=ENV_Var_File.load(Path(os.getenv("ASGS_HOME"))/"profiles"/cls.profile.value)
        print(cls._pro_file)
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
        cls._shell_command(f"load {param} {name}")
        if param=="profile":
            cls._set_profile(name)
        elif param=="adcirc":
            cls._set_adcirc(cls._get_adcirc())


    @classmethod
    def run(cls):
        ...

    @classmethod
    def define(cls,param:Literal["adcircdir", "adcircbranch", "adcircremote", "config", "editor", "hostfile", "scratchdir", "scriptdir", "workdir"], value: str):
        cls._shell_command(f"define {param} {value}")
        
        if param=="config":
            cls._set_config(value)

    @classmethod
    def init(cls):
        ...

    @classmethod    
    def save(cls,param:str,name:str):
        cls._shell_command(f"save {param} {name}",shell=True,executable=Path(os.getenv("ASGS_HOME")/"asgsh"))

        if name not in cls.profile.options:
            cls.profile.add_option(name)
        cls._set_profile(name)
        
        
    @classmethod
    def show(cls,param:Literal["config","adcircbase","adcircdir","adcircbranch","adcircremote","asgslocaldir","asgsversion","machinename","adcirccompiler","asgscompiler","home","hostfile","installpath","brewflags","editor","exported","instancename","ld_include_path","ld_library_path","path","profile","rundir","scratchdir","scriptdir","statefile","syslog","workdir","platform_init","age","info"]):
        return cls._shell_command(f"show {param}")

    @classmethod    
    def list(cls,param: Literal['adcirc', 'configs', 'meshes', 'platforms', 'profiles']) -> list[str]:
        
        return cls._shell_command(f"list {param}")

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

