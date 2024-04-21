import textx
from typing import (
    MutableMapping, TypeVar, Optional, TYPE_CHECKING,
    Union, Generic, Dict, List, Any, Iterator
)
import textx.model

from .models import Variable
from .models import Action
from .models import Operator

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_Config = TypeVar('_Config', bound=object)
_Rule = TypeVar('_Rule', bound=object)
    
class Rule:
    @property
    def variables(self) -> List[Variable]:
        return self._variables
    @property
    def actions(self) -> List[Action]:
        return self._actions
    @property
    def operator(self) -> Operator[str]:
        return self._operator
    
    def __init__(self, rule: _Rule):
        self._variables = []
        self._actions = []
        self._operator = Operator(base_class=self, **vars(rule.operator))
        for variable in rule.variables:
            self._variables.append(Variable(self, **vars(variable)))
        for action in rule.actions:
            self._actions.append(Action(self, **vars(action)))
        
class Config(Generic[_T]):
    #__secaction__: Optional[List[SecAction]]
    #__secmarker__: Optional[List[SecMarker]]
    __secrules__: List[Rule]
    def __init__(self, config: _Config):
        self.__secrules__ = []
        self.config = config
        for rule in self.config.rules:
            if rule.__class__.__name__ != 'SecRule':
                continue
            else:
                self.__secrules__.append(Rule(rule))