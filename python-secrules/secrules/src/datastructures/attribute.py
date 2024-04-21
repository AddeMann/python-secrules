from typing import Generic, TypeVar
    
_T = TypeVar('_T')
class VariableAttribute(Generic[_T]):
    __name__: str
    
class ActionAttribute(Generic[_T]):
    __name__: str
    
class OperatorAttribute(Generic[_T]):
    __name__: str