from ..base.var import Variable,Var_Bin,Validated_Var_Bin
from pathlib import Path
import re

def fix_path(path):
    if not isinstance(path,Path):
        path=Path(path)
    return str(path.expanduser().resolve())

def fix_int(val):
    return int(val)

# TODO
def fix_url(url):
    return url

class ENV_Variable(Variable):
    def __str__(self):
        return f"export {self.name}={f"'{self.value}'" if isinstance(self.value,str) else str(self.value)}"

class ENV_Var_File(Var_Bin,var_type=ENV_Variable):
    def __init__(self,name,path=None,**kwargs):
        self.path=path
        super().__init__(name,**kwargs)

    @staticmethod
    def _read(path):
        vars={}
        
        num_test_start="0123456789+-."
        num_test_second="0123456789.ij"
        
        key_regex=re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*(?==)",flags=re.MULTILINE)
        val_regex=re.compile(r"(?<==[\"']).+(?=[\"']$)|(?<==)[^\"'].*$",flags=re.MULTILINE)

        with open(path,"r") as file:
            for line in file:
                if len(line)<6 or line.strip()[0:6]!="export":
                    continue

                val: str=re.findall(val_regex,line)
                if val:
                    val=val[0]
                    if "#" in val:
                        val=val.split("#")[0].strip()
                else:
                    val=""

                # This looks like shit but should be performant way to check for a number.
                if val and val[0] in num_test_start:
                    if len(val)==1 or val[1] in num_test_second:
                        try:
                            val=int(val)
                        except ValueError:
                            try:
                                val=float(val)
                            except ValueError:
                                try:
                                    val=complex(val.replace(" ",""))
                                except:
                                    pass
                vars[re.findall(key_regex,line)[0]]=val
        return vars

    # TODO Stress test to detirmine if multiproc is needed
    @classmethod
    def load(cls,path: Path | str):
        if isinstance(path,str):
            path=Path(path)
        
        
        return cls(path.name,path,**cls._read(path))

    def update(self,path: Path | str,delete_diff: bool=False):
        """Updates variables in place so all object refs stay the say."""
        if isinstance(path,str):
            path=Path(path)

        new_vars=self._read(path)
        
        if not delete_diff:
            for key in self.variables.keys() - new_vars.keys():
                self.variables[key].value=""
        else:
            for key in self.variables.keys() - new_vars.keys():
                del self.variables[key]

        for key in new_vars.keys():
            var=new_vars[key]
            
            if key in self.variables:
                self.variables[key].value=var if not isinstance(var,ENV_Variable) else var.value
            else:
                self.variables[key]=var if isinstance(var,ENV_Variable) else ENV_Variable(key,var)
        


    def __repr__(self):
        return "\n".join((str(val) for val in self.variables.values()))

    def save(self,name: Path | str):
        if isinstance(name,str):
            name=Path(name)

        # TODO Use this as a test for a dev package
        if name.exists():
            raise FileExistsError(f"Adcirc meta data file already exists at {name}.\nPlease contact ASGS admin.")
        
        with open(name,"x") as adcirc_met_file:
            adcirc_met_file.write("\n".join((str(val) for val in self.variables.values())))

# Load a profile then check for the variables. This will assist in dealing with logic of the bash scripts
# Do like sp.Popen([".","var_file"])
class ADC_Profile_File(ENV_Var_File,valid_vars={
                    "ASGS_HOME":fix_path,
                    "ASGS_MACHINE_NAME":None,
                    "NETCDFHOME":fix_path,
                    "ADCIRCBASE":fix_path,
                    "ADCIRCDIR":fix_path,
                    "SWANDIR":fix_path,
                    "ADCIRC_COMPILER":None,
                    "ADCIRC_BUILD_INFO":fix_path,
                    "ADCIRC_GIT_BRANCH":None,
                    "ADCIRC_GIT_URL":fix_url,
                    "ADCIRC_GIT_REPO":None,
                    "ASGS_MAKEJOBS":fix_int,
                    "ADCIRC_MAKE_CMD":None,
                    "SWAN_UTIL_BINS_MAKE_CMD":None,
                    "ADCSWAN_MAKE_CMD":None,
                    "ADCIRC_PROFILE_NAME":None,
                    "ADCIRC_BINS":None,
                    "ADCSWAN_BINS":None,
                    "SWAN_UTIL_BINS":None
                    }):
    def __init__(self,name,path=None,**kwargs):
        self.path=path
        super().__init__(name,**kwargs)
