import io
import chardet
import os
from typing import overload, Optional, Union, Any, List
from . import resources
from . import parser
from secrules.src.datastructures import Config
        
class SecRuleLoader:
    def __init__(self):
        self._process_from_str = parser.process_from_str
        self._get_correctness = parser.get_correctness
        
    def _read(self, file: Union[str, os.PathLike[str]], encoding: str):
        if isinstance(file, os.PathLike):
            file = os.fsdecode(file)
        try:
            with open(file, encoding=encoding) as file_reader:
                lines = file_reader.read()
        except OSError:
            return
        rule = self._process_from_str(lines)
        self._get_correctness([file], models=[rule])
        return Config(config=rule)
    
    def _read_from_buffer(self, buffer: Union[bytes, bytearray, memoryview]):
        text_buffer = ''
        if isinstance(buffer, bytearray):
            buffer = bytes(buffer)
        if isinstance(buffer, memoryview):
            buffer = buffer.tobytes()
        encoding = chardet.detect(buffer)['encoding']
        if encoding != 'utf-8':
            raise UnicodeError()
        for chunk in range(0, len(buffer), 1024):
            chunk = buffer[chunk:chunk + 1024]
            try:
                text_buffer.join(chunk.decode(encoding))
            except UnicodeDecodeError:
                return
        rule = self._process_from_str(text_buffer)
        self._get_correctness([0], models=[rule])
        return Config(config=rule)
    
class SecRuleParser(SecRuleLoader):
    def __init__(self):
        super().__init__()
        
    @overload
    def read(self, file: Union[str, os.PathLike[str]], encoding: Optional[str] = None) -> Config:
        ...
        
    @overload
    def read(self, buffer: Union[bytes, bytearray, memoryview]) -> Config:
        ...
        
    def read(self, **kwargs: Any):
        if 'file' in kwargs and not 'buffer' in kwargs:
            encoding = io.text_encoding(kwargs.get('encoding'))
            config = self._read(file=kwargs.get('file'), encoding=encoding)
            return config
        elif 'buffer' in kwargs and not 'file' in kwargs:
            config = self._read_from_buffer(buffer=kwargs.get('buffer'))
            return config
    def read_files(self, files: List[Union[str, os.PathLike[str]]], encoding: Optional[str] = None) -> List[Config]:
        config_instances = []
        for file in files:
            config = self.read(file, encoding=encoding)
            config_instances.append(config)
        return config_instances