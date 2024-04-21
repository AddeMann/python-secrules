from enum import Enum
from typing import (
    TypeVar, TYPE_CHECKING, Generic, Any, Iterator, Tuple
)

if TYPE_CHECKING:
    from .attribute import VariableAttribute
    from .attribute import ActionAttribute
    from .attribute import OperatorAttribute
    from .rule import Rule
    
_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_Model = TypeVar('_Model', bound=object)

class _RuleModels(Enum):
    ACTION = 'action'
    OPERATOR = 'operator'
    VARIABLE = 'variable'
    
class RuleModel:
    __baseclass__: "Rule"
    __model__: _Model
    def __init__(self, base_class: "Rule", model: _Model):
        self.__baseclass__ = base_class
        self.__model__ = model
        
class Regex(RuleModel):
    def __init__(self, base_class: "Rule", **kwargs: Any):
        super().__init__(base_class=base_class, model=self)
        
class Variable(RuleModel):
    def __init__(self, base_class: "Rule", **kwargs: Any):
        super().__init__(base_class=base_class, model=self)
        
        self.__variable__ = kwargs
            
    def __getattribute__(self, name: str) -> "VariableAttribute":
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        if name in self.__variable__:
            setattr(self, name, self.__variable__[name])
        else:
            raise AttributeError(name)
        return getattr(self, name)
    
    def __iter__(self) -> Iterator[Tuple[_KT, _VT]]:
        return iter(self.__variable__.items())
    
class Action(RuleModel):
    def __init__(self, base_class: "Rule", **kwargs: Any):
        super().__init__(base_class=base_class, model=self)
        
        self.__action__ = kwargs
            
    def __getattribute__(self, name: str) -> "ActionAttribute":
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        if name in self.__action__:
            setattr(self, name, self.__action__[name])
        else:
            raise AttributeError(name)
        return getattr(self, name)
    
    def __iter__(self) -> Iterator[Tuple[_KT, _VT]]:
        return iter(self.__action__.items())
        
class Operator(RuleModel, Generic[_T]):
    def __init__(self, base_class: "Rule", **kwargs: Any):
        super().__init__(base_class=base_class, model=self)
        
        self.__operator__ = kwargs
            
    def __getattribute__(self, name: str) -> "OperatorAttribute":
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        if name in self.__operator__:
            setattr(self, name, self.__operator__[name])
        else:
            raise AttributeError(name)
        return getattr(self, name)
    
    def __iter__(self) -> Iterator[Tuple[_KT, _VT]]:
        return iter(self.__operator__.items())