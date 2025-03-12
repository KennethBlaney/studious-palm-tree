from typing import Dict
from dataclasses import dataclass
from pydantic import BaseModel

from ..utils import roll_d100, roll_ndm


@dataclass
class BasicRoleplaySkill(BaseModel):
    name: str = ""
    category: str = ""
    chance: int = 0
    experience_check: bool = False
    can_be_improved_through_experience: bool = True  # only false for Blasphemous Knowledge

    def experience_roll(self, int_characteristic: int = 10, improvement_dice: int = 6):
        """
        Rolls an experience check for this skill.
        :param int_characteristic: bonus for character's learning based on their int
        :param improvement_dice: the size of the improvement die to roll, generally 6
        :return: None, acts on self
        """
        if self.experience_check:
            improve_check = roll_d100() + -(int_characteristic//-2)
            if improve_check >= min(self.chance, 100):
                self.improve(roll_ndm(1, improvement_dice))
            self.experience_check = False

    def improve(self, amount: int):
        self.chance += amount

    def skill_roll(self,
                   category_bonus: dict = None,
                   armor_penalty: dict = None,
                   fatigue_points: int = 0,
                   diff_multi: int = 1,
                   modifier: int = 0,
                   advantage: int = 0,
                   lucky: bool = False) -> Dict:
        """
        This rolls the skill and reports a dict of the levels of success
        :param category_bonus: bonus from the calling character's characteristics
        :param armor_penalty: penalty from armor on a skill
        :param fatigue_points: penalty for negative fatigue
        :param diff_multi: easy checks should double the skill, difficult or fatigued checks should half it
        :param modifier: a situational modifier for the skill roll, adds to chance of success
        :param advantage: positive values indicate additional rolls to take lowest,
                          negative values indicate additional rolls to take highest
        :param lucky: allows a 1% chance of success on a skill with 0 chance
        :return: dict of possible success states
        """

        if not category_bonus:
            category_bonus = {}
        if not armor_penalty:
            armor_penalty = {}
        if fatigue_points > 0:
            fatigue_points = 0
        roll = roll_d100(advantage)
        total = (roll
                 + category_bonus.get(self.category, 0)
                 - armor_penalty.get(self.category, 0)
                 + modifier
                 + fatigue_points)
        result = {
            "fumble": False,
            "failure": True,
            "success": False,
            "special": False,
            "critical": False,
            "roll": roll,
            "total": total
        }
        if self.chance == 0 and roll == 1 and lucky:
            result["failure"], result["success"] = False, True
            return result
        if roll >= 100-(100-self.chance)//20:
            result["fumble"] = True
        elif total <= diff_multi * self.chance:
            result["failure"], result["success"] = False, True
            self.experience_check = True
            if total <= -((diff_multi * self.chance)//-5):
                result["special"] = True
                if total <= -((diff_multi * self.chance)//-20):
                    result["critical"] = True
        return result
