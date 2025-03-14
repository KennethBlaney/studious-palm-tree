from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined

from src.sheets import BasicRoleplaySkill, BasicRoleplayCharacter


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RavenSkill(BasicRoleplaySkill):
    guilt: int = 100


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RavenCharacter(BasicRoleplayCharacter):
    guilt: int = 10
