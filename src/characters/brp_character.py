from dataclasses import dataclass, field
from json import loads

from .brp_skill import BasicRoleplaySkill
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
    use_education: bool = True  # use optional education rule
    personality_type: str = ""
    profession: str = ""
    power_level: str = ""
    primary_language: str = ""
    literate: bool = True
    can_drive: bool = True
    can_fly: bool = True
    energy_projection: bool = False

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
    skills: dict = field(default_factory=lambda: {})  # used for skills that this character had increased from defaults
    new_skill_defaults: dict = field(default_factory=lambda: {})  # used to add new skills unique to the setting
    skill_defaults: dict = field(default_factory=lambda: {
        # Combat Skills
        "Artillery (various)": BasicRoleplaySkill(**{"name": "Artillery (various)", "category": "combat", "chance": 5}),
        "Brawl": BasicRoleplaySkill(**{"name": "Brawl", "category": "combat", "chance": 25}),
        "Energy Weapon (various)": BasicRoleplaySkill(
            **{"name": "Energy Weapon (various)", "category": "combat", "chance": 5}),
        "Firearm (varios)": BasicRoleplaySkill(**{"name": "Firearm (varios)", "category": "combat", "chance": 5}),
        "Grapple": BasicRoleplaySkill(**{"name": "Grapple", "category": "combat", "chance": 25}),
        "Heavy Weapon (various)": BasicRoleplaySkill(
            **{"name": "Heavy Weapon (various)", "category": "combat", "chance": 5}),
        "Martial Arts": BasicRoleplaySkill(**{"name": "Martial Arts", "category": "combat", "chance": 1}),
        "Melee Weapon (various)": BasicRoleplaySkill(
            **{"name": "Melee Weapon (various)", "category": "combat", "chance": 5}),
        "Missile Weapon (various)": BasicRoleplaySkill(
            **{"name": "Missile Weapon (various)", "category": "combat", "chance": 5}),
        "Parry (various)": BasicRoleplaySkill(**{"name": "Parry (various)", "category": "combat", "chance": 5}),
        "Shield": BasicRoleplaySkill(**{"name": "Shield", "category": "combat", "chance": 5}),
        # Communication Skills
        "Bargain": BasicRoleplaySkill(**{"name": "Bargain", "category": "communication", "chance": 5}),
        "Command": BasicRoleplaySkill(**{"name": "Command", "category": "communication", "chance": 5}),
        "Disguise": BasicRoleplaySkill(**{"name": "Disguise", "category": "communication", "chance": 1}),
        "Etiquette (various)": BasicRoleplaySkill(
            **{"name": "Etiquette (various)", "category": "communication", "chance": 5}),
        "Fast Talk": BasicRoleplaySkill(**{"name": "Fast Talk", "category": "communication", "chance": 5}),
        "Language (various)": BasicRoleplaySkill(
            **{"name": "Language (own)", "category": "communication", "chance": 0}),
        "Perform": BasicRoleplaySkill(**{"name": "Perform", "category": "communication", "chance": 5}),
        "Persuade": BasicRoleplaySkill(**{"name": "Persuade", "category": "communication", "chance": 15}),
        "Status": BasicRoleplaySkill(
            **{"name": "Status", "category": "communication", "chance": 15,
               "can_be_improved_through_experience": False}),
        "Teach": BasicRoleplaySkill(**{"name": "Teach", "category": "communication", "chance": 10}),
        # Manipulation Skills
        "Art (various)": BasicRoleplaySkill(**{"name": "Art (various)", "category": "manipulation", "chance": 5}),
        "Craft (various)": BasicRoleplaySkill(**{"name": "Craft (various)", "category": "manipulation", "chance": 5}),
        "Demolition": BasicRoleplaySkill(**{"name": "Demolition", "category": "manipulation", "chance": 1}),
        "Fine Manipulation": BasicRoleplaySkill(
            **{"name": "Fine Manipulation", "category": "manipulation", "chance": 5}),
        "Heavy Machine (various)": BasicRoleplaySkill(
            **{"name": "Heavy Machine (various)", "category": "manipulation", "chance": 1}),
        "Repair (various)": BasicRoleplaySkill(
            **{"name": "Repair (various)", "category": "manipulation", "chance": 15}),
        "Sleight of Hand": BasicRoleplaySkill(**{"name": "Sleight of Hand", "category": "manipulation", "chance": 5}),
        # Mental Skills
        "Appraise": BasicRoleplaySkill(**{"name": "Appraise", "category": "mental", "chance": 15}),
        "Blasphemous Lore": BasicRoleplaySkill(
            **{"name": "Blasphemous Lore", "category": "mental", "chance": 0,
               "can_be_improved_through_experience": False}),
        "First Aid": BasicRoleplaySkill(**{"name": "First Aid", "category": "mental", "chance": 30}),
        "Gaming": BasicRoleplaySkill(**{"name": "Gaming", "category": "mental", "chance": 0}),
        "Knowledge (various)": BasicRoleplaySkill(**{"name": "Knowledge (various)", "category": "mental", "chance": 5}),
        "Literacy": BasicRoleplaySkill(**{"name": "Literacy", "category": "mental", "chance": 0}),
        "Medicine": BasicRoleplaySkill(**{"name": "Medicine", "category": "mental", "chance": 5}),
        "Psychotherapy": BasicRoleplaySkill(**{"name": "Psychotherapy", "category": "mental", "chance": 1}),
        "Science (various)": BasicRoleplaySkill(**{"name": "Science (various)", "category": "mental", "chance": 1}),
        "Strategy": BasicRoleplaySkill(**{"name": "Strategy", "category": "mental", "chance": 1}),
        "Technical Skill (various)": BasicRoleplaySkill(
            **{"name": "Technical Skill (various)", "category": "mental", "chance": 5}),
        # Perception Skills
        "Insight": BasicRoleplaySkill(**{"name": "Insight", "category": "perception", "chance": 5}),
        "Listen": BasicRoleplaySkill(**{"name": "Listen", "category": "perception", "chance": 25}),
        "Navigate": BasicRoleplaySkill(**{"name": "Navigate", "category": "perception", "chance": 10}),
        "Research": BasicRoleplaySkill(**{"name": "Research", "category": "perception", "chance": 25}),
        "Sense": BasicRoleplaySkill(**{"name": "Sense", "category": "perception", "chance": 10}),
        "Spot": BasicRoleplaySkill(**{"name": "Spot", "category": "perception", "chance": 25}),
        "Track": BasicRoleplaySkill(**{"name": "Track", "category": "perception", "chance": 10}),
        # Physical Skills
        "Climb": BasicRoleplaySkill(**{"name": "Climb", "category": "physical", "chance": 40}),
        "Dodge": BasicRoleplaySkill(**{"name": "Dodge", "category": "physical", "chance": 0}),
        "Drive (various)": BasicRoleplaySkill(**{"name": "Drive (various)", "category": "physical", "chance": 0}),
        "Fly": BasicRoleplaySkill(**{"name": "Fly", "category": "physical", "chance": 0}),
        "Hide": BasicRoleplaySkill(**{"name": "Hide", "category": "physical", "chance": 10}),
        "Jump": BasicRoleplaySkill(**{"name": "Jump", "category": "physical", "chance": 25}),
        "Pilot (various)": BasicRoleplaySkill(**{"name": "Pilot (various)", "category": "physical", "chance": 1}),
        "Projection": BasicRoleplaySkill(**{"name": "Projection", "category": "physical", "chance": 0}),
        "Ride (various)": BasicRoleplaySkill(**{"name": "Ride (various)", "category": "physical", "chance": 5}),
        "Stealth": BasicRoleplaySkill(**{"name": "Stealth", "category": "physical", "chance": 10}),
        "Swim": BasicRoleplaySkill(**{"name": "Swim", "category": "physical", "chance": 25}),
        "Throw": BasicRoleplaySkill(**{"name": "Throw", "category": "physical", "chance": 25})
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
        # skills that depend on attributes
        self.skill_defaults["Dodge"].chance = 2 * self.DEX
        if self.can_drive:
            self.skill_defaults["Drive (various)"].chance = 20
        if not self.use_education:
            self.skill_defaults[f"Language ({self.primary_language}"] = BasicRoleplaySkill(
                **{"name": "Language (own)", "category": "communication", "chance": 5 * self.INT})
        else:
            self.skill_defaults[f"Language ({self.primary_language}"] = BasicRoleplaySkill(
                **{"name": "Language (own)", "category": "communication", "chance": 5 * max(self.INT, self.EDU)})
        if self.literate:
            self.skill_defaults["Literacy"].chance = self.skill_defaults[f"Language ({self.primary_language}"].chance
        self.skill_defaults["Gaming"] = BasicRoleplaySkill(
            **{"name": "Language (own)", "category": "communication", "chance": self.INT + self.POW})
        if self.can_fly:
            self.skill_defaults["Fly"].chance = 4 * self.DEX
        else:
            self.skill_defaults["Fly"].chance = .5 * self.DEX
        if self.energy_projection:
            self.skill_defaults["Projection"].chance = 2 * self.DEX

        # incorporate passed in skills
        self.skill_defaults.update(self.new_skill_defaults)

        # set defaults for undefined skills for the character
        for key in self.skill_defaults:
            if key not in self.skills:
                self.skills[key] = self.skill_defaults[key]

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

