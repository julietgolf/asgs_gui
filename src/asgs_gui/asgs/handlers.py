from ..base.var import Variable,Var_Bin
from ..base.handlers import Generic_Handler
import subprocess as sp
from typing import Literal
import re
from pathlib import Path
from ..base.base_types import DIALOGUE_INPUT_TYPE
from .env_var import ENV_Var_File
import os,sys,signal #psutil
import warnings
#TODO Turn this into a module
#TODO Transition from inputs to sb

#ADCIRC_PROFILE_NAME=
#

class _Server_Handler:
    def __init__(self):
        self.server_meta_dir=Path(f"{os.getenv("HOME")}/.asgsh")
        self._pipein_path=self.server_meta_dir/"pipein"
        self._pipeout_path=self.server_meta_dir/"pipeout"
        if not (self._pipein_path.exists() and self._pipeout_path.exists()):
            raise FileExistsError(f"Missings pipe file in {self.server_meta_dir}.")
    
        self._end_token=str(hash("---Server-Call-Done---"))+"\n"
        self._server_call_out=self.server_meta_dir/(self._end_token.strip()+".out")
        self._server_call_out.touch()
        self.pipeout=open(self._pipeout_path,"r")
        self.pipein=open(self._pipein_path,"w")
        #start_file=self.server_meta_dir/".gui_init"

        #self._ansi_filter=re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\].*?(?:\x07|\x1b\\)|\x1b[A-Za-z0-9_=><]|\x1b[\x20-\x2f]?[\x30-\x7e]')
        #self._prompt=re.compile(r"^\[ASGS \([a-zA-Z0-9_][a-zA-Z0-9_\+-]*\)\] [a-zA-Z0-9_][a-zA-Z0-9_\+-]*@[a-zA-Z0-9_][a-zA-Z0-9_\+-]*>")

        #if start_file.exists():
        #    return
        
        self.pipein.write("echo --end--\n")
        self.pipein.flush()
#
        #while True:
        #    line=self.pipeout.readline()
        #    print(line,end="")
        #    line=self._ansi_filter.sub("",line)
        #    if line == "--end--\n":#re.search(self._prompt,line):
        #        #print("line 35: Broken")
        #        break
        #
        #start_file.touch()

    def run(self,command):
        print(command+f" > {self._server_call_out}; echo "+self._end_token)
        self.pipein.write(command+f" > {self._server_call_out}; echo "+self._end_token)
        self.pipein.flush()
        if command=="run":
            return
        output=""
        while True:
            line=self.pipeout.readline()
            print(line)
            if line==self._end_token:
                break
        with open(self._server_call_out,"r") as out:
            while True:
                line=out.readline()
                print("line",line)
                #line=self.pipeout.readline()
                if not line:
                    break
                #if line=='\x1b[?2004l\n':
                #    continue
                #
                #line=self._ansi_filter.sub("",line)
                #if re.search(self._prompt,line):
                #    continue
                #elif self._end_token==line:
                #    break
                #elif self._end_token in line:
                #    continue
                else:
                    print(line)
                    output+=line

        return output

    def __del__(self):
        self.pipein.close()
        self.pipeout.close()

class ASGS_API:
    """This is becuase of DOGE. Fuck me."""

    @staticmethod
    def _check_dirname(name:str):
        if not name or len(name) > 255:
            raise ValueError(f"{name} is not a valid name")
        
        if not re.match(r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$", name):
            raise ValueError(f"{name} is not a valid name")

    @classmethod
    def _shell_command(cls,command:str,capture_output=True) -> str:
        #TODO each new command needs to be as a security threat to prevent command line injection attacks
        print(f"running command: {command}")
        if capture_output:
            result=cls._server.run(command)
            return result
            #errout=result.stderr.decode("utf-8")
            #if errout:
            #    warnings.warn(errout)
            
            #return result.stdout.decode("utf-8")
        else:
            cls._server.run(command)

    @classmethod
    def _get_mesh(cls,config_path=None):
        print("_get_mesh")
        if config_path is None:
            config_path=cls._get_config_path()
        with open(config_path, 'r') as f:
            for line in f:
                if "GRIDNAME=" in line:
                    return line.strip().split("=")[1]
    
    @classmethod
    def _get_config_years(cls):
        return cls.config_years.value

    @classmethod
    def _get_config_path(cls):
        print("_get_config_path")
        return cls._config_path#Path(cls._pro_file.variables["ASGS_HOME"].value)/"config"/cls._get_config_years()/cls.config.value


    @classmethod
    def _get_config(cls):
        print("_get_config")
        return cls._pro_file.variables["ASGS_CONFIG"].value
        #return re.findall(r"(?<=').*(?=')",cls.show("config").strip())[0]
    
    @classmethod
    def _get_profile(cls):
        print("_get_profile")
        return ASGS_API.profile.value
        return re.findall(r"(?<=').*(?=')",cls.show("profile").strip())[0]
    
    @classmethod
    def _get_adcirc(cls):
        print("_get_adcirc")
        return cls._pro_file.variables["ADCIRC_PROFILE_NAME"].value
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
        cls.adcirc.value=adcirc

    @classmethod
    def _set_config_path(cls,config_path=None):
        print("naisfj")
        if config_path is None:
            config_path=cls._get_config_path()
        if not isinstance(config_path,Path):
            config_path=Path(config_path)
        
        print(config_path)
        cls._config_path=config_path
        cls._set_config(config_path.name)
        #cls._set_mesh(cls._get_mesh())

    @classmethod
    def _set_config(cls,config=None):
        print("setting config",config)
        #if config is None:
            #year,config=str(cls._get_config()).split("/")[-2:]
            #print(year)
            #cls._set_config_years(year)

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
            print("reult",[val.split()[-1].strip() for val in result])
            var.options=[val.split()[-1].strip() for val in result]
        else:
            #TODO Add a config dirs option
            var.options=[config for config in os.listdir(cls._ASGS_HOME/"config"/cls.config_years.value) if ".sh" in config]

    @classmethod
    def _init(cls):
        cls._PARAM_PLURALS={"profile":"profiles","mesh":"meshes","adcirc":"adcircs"}

        cls._server=_Server_Handler()

        cls._ASGS_HOME=Path(cls._server.run("echo $ASGS_HOME").strip())

        print("running")
        #cls.load("profile","default-asgs")
        current_profile=re.findall(r"(?<=').*(?=')",cls.show("profile").strip())[0]
        cls.profile=Variable("profile",current_profile,"Profile",current_profile)
        print(cls._ASGS_HOME/"profiles"/cls.profile.value)
        cls._pro_file=ENV_Var_File.load(cls._ASGS_HOME/"profiles"/cls.profile.value)
        print(cls._pro_file)
        cls._set_options(cls.profile)
        print(cls.profile)

        current_config=cls._pro_file.variables["ASGS_CONFIG"].value#cls._get_config()

        #year_check=re.compile(r"20[0-2][0-9]")
        #years=[year for year in os.listdir(Path(cls._pro_file.variables["ASGS_HOME"].value)/"config") if re.search(year_check,year) is not None]
        #years.sort(reverse=True)

        #year=re.search(r"20[0-2][0-9](?=/.+\.sh)",current_config)
        #if year is None:
        #    year=years[0]
        #else:
        #    year=year.group()

        #cls.config_years=Variable("config_years",year,default_value=year)
        #cls.config_years.options=years
        current_config=Path(current_config)
        cls._config_path=current_config
        cls.config=Variable("config",current_config.name,"Config")
        #cls._set_options(cls.config)

        print(cls.config)


        #echo $ADCIRC_PROFILE_NAME
        current_adcirc=cls._pro_file.variables["ADCIRC_PROFILE_NAME"].value#cls._get_adcirc()
        cls.adcirc=Variable("adcirc",current_adcirc,"ADCIRC",current_adcirc)
        cls._set_options(cls.adcirc)
        #cls._adc_file=ENV_Var_File.load(Path(cls._pro_file.variables["ADCIRC_META_DIR"].value)/cls.adcirc.value)
        print(cls.adcirc)


        current_mesh=cls._get_mesh()
        cls.mesh=Variable("mesh",current_mesh,"Mesh",current_mesh)
        cls._set_options(cls.mesh)
        print(cls.mesh)

        cls._run_proc=None

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
        #cls._check_dirname(name)
        #cls._shell_command(f"load {param} {name}")

        if param=="profile":
            cls._pro_file.update(Path(cls._pro_file.variables["ASGS_META_DIR"].value)/name,delete_diff=True)
            cls._set_profile(name)
        elif param=="adcirc":
            cls._pro_file.update(Path(cls._pro_file.variables["ADCIRC_META_DIR"].value)/name)
            cls._set_adcirc(cls._get_adcirc())

    @classmethod
    def run(cls):
        #cls._shell_command(f"run",capture_output=False)
        cls._run_proc=sp.Popen(f"load profile {cls.profile.value}; run",shell=True,start_new_session=True)


    @classmethod
    def define(cls,param:Literal["adcircdir", "adcircbranch", "adcircremote", "config", "editor", "hostfile", "scratchdir", "scriptdir", "workdir"], value: str):
        #cls._shell_command(f"define {param} {value}")
        
        if param=="config":
            cls._set_config(value)

    @classmethod
    def init(cls):
        ...

    @classmethod    
    def save(cls,param:str,name:str,update_adcirc=False):
        #cls._check_dirname(name)
        #cls._shell_command(f"save {param} {name}")

        if param=="profile":
            if update_adcirc:
                cls._pro_file.update(Path(cls._pro_file.variables["ADCIRC_META_DIR"].value)/cls.adcirc.value)
            cls._pro_file.variables["ASGS_CONFIG"].value=str(cls._config_path)
            cls._pro_file.save(Path(cls._pro_file.variables["ASGS_META_DIR"].value)/name)
            if name not in cls.profile.options:
                cls.profile.add_option(name)
            cls._set_profile(name)
        
    
    @classmethod
    def show(cls,param:Literal["config","adcircbase","adcircdir","adcircbranch","adcircremote","asgslocaldir","asgsversion","machinename","adcirccompiler","asgscompiler","home","hostfile","installpath","brewflags","editor","exported","instancename","ld_include_path","ld_library_path","path","profile","rundir","scratchdir","scriptdir","statefile","syslog","workdir","platform_init","age","info"]):
        return cls._shell_command(f"show {param}")

    @classmethod    
    def list(cls,param: Literal['adcirc', 'configs', 'meshes', 'platforms', 'profiles']) -> list[str]:
        return [val for val in cls._shell_command(f"list {param}").split("\n") if val]

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

class ASGS_Settings_Bin(Var_Bin):
    def __init__(self):
        super().__init__(
            "ASGS Settings Bin",
            local_assets=Variable("local_assets","","Local Assets"),
            asgs_home=Variable("asgs_home",os.getenv("ASGS_HOME"),"ASGS Home")
        )

class ASGS_Settings_Handlers(Generic_Handler,var_names=[
    "local_assets",
"asgs_home"
]):
    def __init__(self,var_input_type:dict[str,DIALOGUE_INPUT_TYPE]={},immutable_vars: list[str]=[]):
        super().__init__(ASGS_Settings_Bin(),var_input_type,immutable_vars)
