from typing import Any, Hashable

class Variable:
    def __init__(self, name: str | int | Hashable, value: Any=None, pretty_name: str=None, default_value: Any=None, options: list=None):
        self._name = name
        self._value = value 
        self._default=default_value
        self._pretty_name = pretty_name
        self._options=options

    __slots__=("_name","_value","_default","_pretty_name","_options")

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,value):
        self._value=value

    @property
    def name(self):
        return self._name
    
    @property
    def pretty_name(self):
        return self._pretty_name if self._pretty_name is not None else self.name
    
    @pretty_name.setter
    def pretty_name(self,pretty_name):
        self._pretty_name=pretty_name

    @property
    def default(self):
        return self._default
    
    def set_default(self):
        self.value=self.default

    @property
    def options(self):
        return self._options
    
    @options.setter
    def options(self,options):
        self._options=options

    def add_option(self,option):
        self._options.append(option)

    # This can be helpful for managing a lot of variables
    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, val={self.value}, pretty name={self.pretty_name})"

class Unvalidated_Var_Bin:
    def __init__(self,name,**kwargs):
        self.name=name
        self.variables: dict[str,Variable]={}
        for var_name,val in kwargs.items():
            if not issubclass(type(val),Variable):
                val=self.VAR_TYPE(var_name,val)
            self.variables[var_name]=val

    def set(self,var_name,val):
        if not issubclass(type(val),Variable):
            val=self.VAR_TYPE(var_name,val)
            
        self.variables[var_name]=val

class Validated_Var_Bin:
    def __init__(self,name,**kwargs):
        self.name=name
        self.variables={}
        for var_name,val in kwargs.items():
            if self.VALID_VARS:
                if var_name in self.VALID_VARS:
                    if self.VALID_VARS[var_name] is not None:
                        val=self.VALID_VARS[var_name](val)
                else:
                    raise ValueError(f"{var_name} is not a valid variable for {type(self)}")

            if not issubclass(type(val),Variable):
                val=self.VAR_TYPE(var_name,val)

            self.variables[var_name]=val

    def set(self,var_name,val):
        if self.VALID_VARS:
            if var_name in self.VALID_VARS:
                val=self.VALID_VARS[var_name](val)
            else:
                raise ValueError(f"{var_name} is not a valid variable for {type(self)}")

        if not issubclass(type(val),Variable):
            val=self.VAR_TYPE(var_name,val)

        self.variables[var_name]=val

class Var_Bin:
    VALID_VARS=None
    VAR_TYPE=Variable
    def __init_subclass__(cls,var_type: type[Variable]=None,valid_vars=None,*args,**kwargs):
        if valid_vars is not None:
            cls.VALID_VARS=valid_vars
            cls.__bases__=(Validated_Var_Bin,) + cls.__bases__
        else:
            cls.__bases__=(Unvalidated_Var_Bin,) + cls.__bases__

        if var_type is not None:
            if issubclass(var_type,Variable):
                cls.VAR_TYPE=var_type

    
    def __iter__(self):
        return (var for var in self.variables.values())
    
    def __getitem__(self,key) -> Variable:
        return self.variables[key]
    
    def __setitem__(self,key,val: Variable):
        self.variables[key]=val