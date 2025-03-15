from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json, Undefined

from src.sheets import BasicRoleplaySkill, BasicRoleplayCharacter


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RavenSkill(BasicRoleplaySkill):
    guilt: int = 100

    def guilt_roll(self,
                   category_bonus: dict = None,
                   armor_penalty: dict = None,
                   fatigue_points: int = 0,
                   diff_multi: int = 1,
                   modifier: int = 0,
                   advantage: int = 0,
                   lucky: bool = False,
                   guilt: int = 0) -> Dict:
        if guilt >= self.guilt:
            return {
                "fumble": False,
                "failure": True,
                "success": False,
                "special": False,
                "critical": False,
                "guilt": True
            }
        result = self.skill_roll(category_bonus,
                                 armor_penalty,
                                 fatigue_points,
                                 diff_multi,
                                 modifier,
                                 advantage,
                                 lucky)
        result.update({"guilt": False})


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RavenCharacter(BasicRoleplayCharacter):
    guilt: int = 10

    def add_guilt(self, amount: int = 0):
        if amount < 0:
            return
        self.guilt += amount

    def reset_guilt(self):
        self.guilt = 0
