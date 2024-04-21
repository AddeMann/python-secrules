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

class _RuleModels(Enum):
    ACTION = 'action'
    OPERATOR = 'operator'
    VARIABLE = 'variable'
    
class RuleModel:
    __baseclass__: "Rule"
    __model__: _RuleModels
    def __init__(self, base_class: "Rule", model: _RuleModels = _RuleModels.ACTION, model_class: object = object):
        self.__baseclass__ = base_class
        self.__model__ = model
        self.__modelclass__ = model_class
        
class Variable(RuleModel):
    def __init__(self, base_class: "Rule", **kwargs: Any):
        super().__init__(base_class=base_class, model=_RuleModels.VARIABLE, model_class=self)
        
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
        super().__init__(base_class=base_class, model=_RuleModels.ACTION, model_class=self)
        
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
        super().__init__(base_class=base_class, model=_RuleModels.OPERATOR, model_class=self)
        
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