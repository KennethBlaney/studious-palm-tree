from dataclasses import dataclass, field

from ..utils import roll_d100, roll_ndm


@dataclass
class BasicRoleplayCharacter:
    # biographical information
    name: str = ""
    gender: str = ""
    age: int = 0
    tough: bool = False  # use optional total hit points rule
    use_category_bonus: bool = True  # use optional normal category bonus
    use_simple_category_bonus: bool = False  # use optional simple category bonus, will be overridden by category_bonus
    personality_type: str = ""
    profession: str = ""

    # equipment
    wealth: str = ""

    # characteristics
    STR: int = 10
    CON: int = 10
    POW: int = 10
    DEX: int = 10
    CHA: int = 10
    INT: int = 10
    SIZ: int = 10
    EDU: int = 10
    MOV: int = 10
    max_species_pow = 18
    min_species_pow = 3
    pow_improvement_check = False

    # powers
    magic: bool = False
    mutation: bool = False
    psychic: bool = False
    sorcery: bool = False
    superpower: bool = False

    # skills
    skills: set = field(default_factory=lambda: {

        })
    skill_defaults: set = field(default_factory=lambda: {

    })

    # health
    damage: int = 0
    damage_location: dict = field(default_factory=lambda: {
        "left_leg": 0,
        "right_leg": 0,
        "abdomen": 0,
        "head": 0,
        "left_arm": 0,
        "right_arm": 0,
        "chest": 0
    })

    def __post_init__(self):
        self._derived_characteristics()
        self._set_default_skills()
        if self.use_category_bonus or self.use_simple_category_bonus:
            self._set_category_bonuses()

    def improve_pow(self):
        if self.pow_improvement_check:
            target = 5*(self.max_species_pow+self.min_species_pow-self.POW)
            if roll_d100() < target:
                self.POW += roll_ndm(1, 3)-1

    def _derived_characteristics(self):
        self.damage_modifier = self._calc_damage_modifier()
        self.max_hit_points = self._calc_hit_points()
        self.major_wound_level = -(self.max_hit_points // -2)
        self.power_points, self.max_power_points = self.POW, self.POW
        self.experience_bonus = -(self.INT // -2)
        self.max_hp_location = {
            "left_leg": -(self.max_hit_points // -3),
            "right_leg": -(self.max_hit_points // -3),
            "abdomen": -(self.max_hit_points // -3),
            "head": -(self.max_hit_points // -3),
            "left_arm": -(self.max_hit_points // -4),
            "right_arm": -(self.max_hit_points // -4),
            "chest": -(self.max_hit_points // -(10/4))
        }
        self.fatigue = self.STR + self.CON
        self.sanity = min(5 * self.POW, 100)

    def _calc_damage_modifier(self) -> str:
        s = self.STR + self.SIZ
        if s <= 12:
            return "-1d6"
        elif s <= 16:
            return "-1d4"
        elif s <= 24:
            return "0"
        elif s <= 32:
            return "1d4"
        elif s <= 40:
            return "1d6"
        else:
            return f"{(s-41)//16+2}d6"

    def _calc_hit_points(self) -> int:
        if self.tough:
            return self.CON + self.SIZ
        return -((self.CON + self.SIZ)//-2)

    def _set_default_skills(self):
        for key in self.default_skills:
            if key not in self.skills:
                self.skills[key] = self.default_skills[key]

    def _set_category_bonuses(self):
        self.category_bonuses = {"combat": _set_category_bonus(self.DEX, self.INT, self.STR),
                                 "communication": _set_category_bonus(self.INT, self.POW, self.CHA),
                                 "manipulation": _set_category_bonus(self.DEX, self.INT, self.STR),
                                 "mental": _set_category_bonus(self.INT, self.POW, self.EDU),
                                 "perception": _set_category_bonus(self.INT, self.POW, self.CON),
                                 "physical": _set_category_bonus(self.DEX, self.STR, self.CON, self.SIZ)}


def _set_category_bonus(primary: int = 10,
                        secondary1: int = 10,
                        secondary2: int = 10,
                        negative: int = 10) -> int:
    return (primary-10) + (secondary1-10)//2 + (secondary2-10)//2 + (10-negative)




