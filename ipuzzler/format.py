import dataclasses
import json
import typing

@dataclasses.dataclass
class Dimensions():
	width:int
	height:int

@dataclasses.dataclass
class Clue():
	number:int
	clue:str

@dataclasses.dataclass
class Clues():
	across:typing.List[Clue] = dataclasses.field(default_factory=list)
	down:typing.List[Clue] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class IPUZCrosswordFile():
	version:str = "http://ipuz.org/v2"
	kind:typing.List[str] = dataclasses.field(default_factory=lambda: ["http://ipuz.org/crossword#1"])
	title:typing.Optional[str] = None
	author:typing.Optional[str] = None
	dimensions:Dimensions = dataclasses.field(default_factory=lambda: Dimensions(0,0))
	puzzle:typing.List[typing.List[typing.Union[int, str]]] = dataclasses.field(default_factory=list)
	clues:Clues = dataclasses.field(default_factory=Clues)

class Encoder(json.JSONEncoder):
	def default(self, o):
		if dataclasses.is_dataclass(o) and not isinstance(o, type):
			return dataclasses.asdict(o)
		return super().default(o)
