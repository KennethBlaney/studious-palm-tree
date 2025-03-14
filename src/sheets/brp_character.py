import json
from typing import Union, Dict
from dataclasses import dataclass, field, asdict

from .brp_skill import BasicRoleplaySkill
from ..utils import roll_d100, roll_ndm, roll_str

skill_defaults: dict = {
    # Combat Skills
    "Artillery (various)": BasicRoleplaySkill(**{"name": "Artillery (various)", "category": "combat", "chance": 5}),
    "Brawl": BasicRoleplaySkill(**{"name": "Brawl", "category": "combat", "chance": 25}),
    "Energy Weapon (various)": BasicRoleplaySkill(
        **{"name": "Energy Weapon (various)", "category": "combat", "chance": 5}),
    "Firearm (various)": BasicRoleplaySkill(**{"name": "Firearm (various)", "category": "combat", "chance": 5}),
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
}


@dataclass
class BasicRoleplayCharacter:
    """
    The BasicRoleplayCharacter is the base class that you should use for a character class in your game.
    It contains the variables for a player character from the Basic Roleplaying - Universal Game Engine rule set
    and includes functions for skill rolls, opposed roles, sanity rolls, etc.

    NPCs are, functionally, scaled back PCs. With that in mind, feel free to set only the relevant variables for an NPC
    and leave the others as default.
    """
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
    improvement_die: int = 6
    primary_language: str = ""
    literate: bool = True
    can_drive: bool = True
    can_fly: bool = True
    energy_projection: bool = False

    # equipment
    wealth: str = ""
    armor: str = ""
    armor_protection: int = 0  # can also be given as a roll string in the form ndm, should usually be positive
    armor_category_penalty: dict = field(default_factory=lambda: {"combat": 0,
                                                                  "communication": 0,
                                                                  "manipulation": 0,
                                                                  "mental": 0,
                                                                  "perception": 0,
                                                                  "physical": 0})
    primary_weapon_damage: str = "0"
    secondary_weapon_damage: str = "0"
    ranged_weapon_damage: str = "0"

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
    SkillClass: bool = False
    skills: dict = field(default_factory=lambda: {})  # used for skills that this character had increased from defaults
    new_skill_defaults: dict = field(default_factory=lambda: {})  # used to add new skills unique to the setting
    spells: list = field(default_factory=lambda: list())
    mutations: list = field(default_factory=lambda: list())
    psychic_powers: list = field(default_factory=lambda: list())
    sorceries: list = field(default_factory=lambda: list())
    superpowers: list = field(default_factory=lambda: list())

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
    minor_wound: bool = False
    major_wound: bool = False
    fatal_wound: bool = False
    sanity: int = 100
    recent_san_loss: int = 0
    temporarily_insane: bool = False
    permanently_insane: bool = False

    def __post_init__(self):
        self.SkillClass = BasicRoleplaySkill
        self._derived_characteristics()
        self._objectify_skills()
        self._set_default_skills()
        if self.use_category_bonus:
            self._set_category_bonuses()
        elif self.use_simple_category_bonus:
            self._set_simple_category_bonuses()
        else:
            self.category_bonuses = {"combat": 0,
                                     "communication": 0,
                                     "manipulation": 0,
                                     "mental": 0,
                                     "perception": 0,
                                     "physical": 0}

    def set_skill_class(self, SkillClass: dataclass = BasicRoleplaySkill):
        self.SkillClass = SkillClass
        if not issubclass(self.SkillClass, BasicRoleplaySkill):
            raise TypeError("A character's SkillClass should be a subclass of BasicRoleplaySkill.")
        self._change_class_for_skills()

    def _change_class_for_skills(self):
        for skill in self.skills:
            self.skills[skill] = self.SkillClass(**asdict(self.skills[skill]))

    def _derived_characteristics(self):
        self.damage_modifier = self._calc_damage_modifier()
        self.max_hit_points = self._calc_hit_points()
        self.major_wound_level = -(self.max_hit_points // -2)
        self.power_points, self.max_power_points = self.POW, self.POW
        self.max_hp_location = {
            "left_leg": -(self.max_hit_points // -3),
            "right_leg": -(self.max_hit_points // -3),
            "abdomen": -(self.max_hit_points // -3),
            "head": -(self.max_hit_points // -3),
            "left_arm": -(self.max_hit_points // -4),
            "right_arm": -(self.max_hit_points // -4),
            "chest": -(self.max_hit_points // -(10 / 4))
        }

        self.fatigue = self.STR + self.CON
        self.sanity = min(5 * self.POW, 100)
        self.temp_insanity_score = -(self.sanity // -2)

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
            return f"{(s - 41) // 16 + 2}d6"

    def _calc_hit_points(self) -> int:
        if self.tough:
            return self.CON + self.SIZ
        return -((self.CON + self.SIZ) // -2)

    def _set_default_skills(self):
        # skills that depend on attributes
        skill_defaults["Dodge"].chance = 2 * self.DEX
        if self.can_drive:
            skill_defaults["Drive (various)"].chance = 20
        if not self.use_education:
            skill_defaults[f"Language ({self.primary_language}"] = BasicRoleplaySkill(
                **{"name": "Language (own)", "category": "communication", "chance": 5 * self.INT})
        else:
            skill_defaults[f"Language ({self.primary_language}"] = BasicRoleplaySkill(
                **{"name": "Language (own)", "category": "communication", "chance": 5 * max(self.INT, self.EDU)})
        if self.literate:
            skill_defaults["Literacy"].chance = skill_defaults[f"Language ({self.primary_language}"].chance
        skill_defaults["Gaming"] = BasicRoleplaySkill(
            **{"name": "Gaming", "category": "communication", "chance": self.INT + self.POW})
        if self.can_fly:
            skill_defaults["Fly"].chance = 4 * self.DEX
        else:
            skill_defaults["Fly"].chance = .5 * self.DEX
        if self.energy_projection:
            skill_defaults["Projection"].chance = 2 * self.DEX

        # characteristic rolls are treated as skill rolls
        skill_defaults["Effort"] = BasicRoleplaySkill(
            **{"name": "Effort", "category": "", "chance": 5 * self.STR, "can_be_improved_through_experience": False})
        skill_defaults["Stamina"] = BasicRoleplaySkill(
            **{"name": "Stamina", "category": "", "chance": 5 * self.CON, "can_be_improved_through_experience": False})
        skill_defaults["Idea"] = BasicRoleplaySkill(
            **{"name": "Idea", "category": "", "chance": 5 * self.INT, "can_be_improved_through_experience": False})
        skill_defaults["Luck"] = BasicRoleplaySkill(
            **{"name": "Luck", "category": "", "chance": 5 * self.POW, "can_be_improved_through_experience": False})
        skill_defaults["Agility"] = BasicRoleplaySkill(
            **{"name": "Agility", "category": "", "chance": 5 * self.DEX, "can_be_improved_through_experience": False})
        skill_defaults["Charm"] = BasicRoleplaySkill(
            **{"name": "Charm", "category": "", "chance": 5 * self.CHA, "can_be_improved_through_experience": False})
        skill_defaults["Know"] = BasicRoleplaySkill(
            **{"name": "Know", "category": "", "chance": 5 * self.EDU, "can_be_improved_through_experience": False})

        # incorporate passed in skills
        skill_defaults.update(self.new_skill_defaults)

        # set defaults for undefined skills for the character
        for key in skill_defaults:
            if key not in self.skills:
                self.skills[key] = skill_defaults[key]

    def _set_category_bonuses(self):
        self.category_bonuses = {"combat": _set_category_bonus(self.DEX, self.INT, self.STR),
                                 "communication": _set_category_bonus(self.INT, self.POW, self.CHA),
                                 "manipulation": _set_category_bonus(self.DEX, self.INT, self.STR),
                                 "mental": _set_category_bonus(self.INT, self.POW, self.EDU),
                                 "perception": _set_category_bonus(self.INT, self.POW, self.CON),
                                 "physical": _set_category_bonus(self.DEX, self.STR, self.CON, self.SIZ)}

    def _set_simple_category_bonuses(self):
        self.category_bonuses = {"combat": -(self.DEX // -2),
                                 "communication": -(self.CHA // -2),
                                 "manipulation": -(self.DEX // -2),
                                 "mental": -(self.INT // -2),
                                 "perception": -(self.POW // -2),
                                 "physical": -(self.STR // -2)}

    def _objectify_skills(self):
        for key, value in self.new_skill_defaults.items():
            self.new_skill_defaults[key] = self.SkillClass(**value)
        for key, value in self.skills.items():
            self.skills[key] = self.SkillClass(**value)

    def make_skill_roll(self,
                        skill: str = "",
                        difficulty: int = 1,
                        modifier: int = 0,
                        advantage: int = 0,
                        lucky: bool = False):
        if skill in self.skills:
            return self.skills[skill].skill_roll(category_bonus=self.category_bonuses,
                                                 armor_penalty=self.armor_category_penalty,
                                                 fatigue_points=self.fatigue,
                                                 diff_multi=difficulty,
                                                 modifier=modifier,
                                                 advantage=advantage,
                                                 lucky=lucky)
        else:
            _skill = " ".join(skill.split(" ")[0:-1] + ["(various)"])
            try:
                return self.skills[_skill].skill_roll(category_bonus=self.category_bonuses,
                                                      armor_penalty=self.armor_category_penalty,
                                                      fatigue_points=self.fatigue,
                                                      diff_multi=difficulty,
                                                      modifier=modifier,
                                                      advantage=advantage,
                                                      lucky=lucky)
            except KeyError:
                raise KeyError(f"Selected skill {skill} is not a valid skill and has no generic type")

    def opposed_roll_highest_success(self,
                                     opponent: Union[BasicRoleplaySkill, int] = 0,
                                     opponent_category_bonus: Dict[str, int] = None,
                                     opponent_armor_penalty: Dict[str, int] = None,
                                     my_skill: str = "",
                                     i_win_ties: bool = None) -> Dict[str, bool]:
        """
        Uses the highest success method to resolve a skill roll. Also, useful for combat.
        :param opponent: A skill from an opponent's character class or a static chance
        :param opponent_category_bonus: opponent's category bonus dict
        :param opponent_armor_penalty: opponent's armor penalty dict
        :param my_skill: The skill this character is using
        :param i_win_ties: Does this character win the tie? If None, ties are determined by highest skill level.
        :return: A dictionary containing if this character won, if they critical'd, if they failed, if they fumbled
        """
        # Make rolls, opponent is either a skill from character or fixed chance
        my_success = self.make_skill_roll(skill=my_skill)
        if opponent_category_bonus is None:
            opponent_category_bonus = {}
        if opponent_armor_penalty is None:
            opponent_armor_penalty = {}
        if isinstance(opponent, int):
            their_success = BasicRoleplaySkill(chance=opponent).skill_roll(category_bonus=opponent_category_bonus,
                                                                           armor_penalty=opponent_armor_penalty)
        else:
            their_success = opponent.skill_roll(category_bonus=opponent_category_bonus,
                                                armor_penalty=opponent_armor_penalty)
            opponent = opponent.chance

        # Turn rolls into digestible form
        my_success_int = _intify_success(my_success)
        their_success_int = _intify_success(their_success)

        # Compare success results
        if my_success_int > their_success_int:
            return {"i_won": True,
                    "is_critical": my_success["critical"],
                    "is_fail": my_success["is_fail"],
                    "is_fumble": my_success["fumble"]}
        if their_success_int > my_success_int:
            return {"i_won": False,
                    "is_critical": their_success["critical"],
                    "is_fail": my_success["is_fail"],
                    "is_fumble": their_success["fumble"]}
        if i_win_ties is not None:
            return {"i_won": i_win_ties,
                    "is_critical": my_success["critical"],
                    "is_fail": my_success["is_fail"],
                    "is_fumble": my_success["fumble"]}
        return {"i_won": self.skills[my_skill].chance >= opponent,
                "is_critical": my_success["fumble"],
                "is_fail": my_success["is_fail"],
                "is_fumble": my_success["fumble"]}

    def opposed_roll_subtraction(self,
                                 opponent: Union[BasicRoleplaySkill, int] = 0,
                                 opponent_category_bonus: Dict[str, int] = None,
                                 opponent_armor_penalty: Dict[str, int] = None,
                                 my_skill: str = "") -> Dict[str, bool]:
        """
        An opposed skill check using the subtraction method. This should be called by the active character.
        :param opponent: A skill from an opponent's character class or a static chance
        :param opponent_category_bonus: opponent's category bonus dict
        :param opponent_armor_penalty: opponent's armor penalty dict
        :param my_skill: The skill this character is using
        :return: A success dictionary from a regular skill roll
        """
        if opponent_category_bonus is None:
            opponent_category_bonus = {}
        if opponent_armor_penalty is None:
            opponent_armor_penalty = {}
        if isinstance(opponent, int):
            their_success = BasicRoleplaySkill(chance=opponent).skill_roll(category_bonus=opponent_category_bonus,
                                                                           armor_penalty=opponent_armor_penalty)
        else:
            their_success = opponent.skill_roll(category_bonus=opponent_category_bonus,
                                                armor_penalty=opponent_armor_penalty)
            opponent = opponent.chance

        their_success_int = _intify_success(their_success)
        if their_success_int > 2:
            if abs(self.skills[my_skill].chance - opponent) <= 5:
                return BasicRoleplaySkill(chance=5).skill_roll(lucky=True)
            return self.make_skill_roll(skill=my_skill,
                                        modifier=-1*opponent)

        if their_success_int == 1:
            return self.make_skill_roll(skill=my_skill, difficulty=2)
        return self.make_skill_roll(skill=my_skill)

    def opposed_roll_resistance_table(self,
                                      opponent: Union[BasicRoleplaySkill, int] = 0,
                                      my_skill: str = "") -> Dict[str, bool]:
        """
        Makes an opposing roll using the resistance table method
        :param opponent: A skill from an opponent's character class or a static chance
        :param my_skill: The skill this character is using
        :return:
        """
        if not isinstance(opponent, int):
            opponent = opponent.chance // 5
        vs = self.skills[my_skill].chance // 5 - opponent
        chance = 50 + 5 * vs
        return roll_d100() <= chance

    def opposed_roll_resistance(self,
                                opponent: Union[BasicRoleplaySkill, int] = 0,
                                my_skill: str = "") -> Dict[str, bool]:
        """
        Makes an opposing roll using the resistance table method
        :param opponent: A skill from an opponent's character class or a static chance
        :param my_skill: The skill this character is using
        :return:
        """
        if not isinstance(opponent, int):
            opponent = opponent.chance
        vs = self.skills[my_skill].chance - opponent
        chance = 50 + vs
        return roll_d100() <= chance

    def opposed_pow_check(self,
                          opponent: Union[BasicRoleplaySkill, int] = 0) -> Dict[str, bool]:
        result = self.opposed_roll_resistance_table(opponent=opponent, my_skill="Luck")
        if result["success"]:
            self.pow_improvement_check = True
        return result

    def improve_pow(self):
        if self.pow_improvement_check:
            target = 5 * (self.max_species_pow + self.min_species_pow - self.POW)
            if roll_d100() < target:
                self.POW += roll_ndm(1, 3) - 1

    def make_experience_rolls(self):
        for skill in self.skills:
            self.skills[skill].experience_roll(int_characteristic=self.INT,
                                               improvement_dice=self.improvement_die)

    def characteristic_roll(self, characteristic: str = "", multiplier: int = 0, advantage: int = 0, modifier: int = 0):
        if characteristic not in {"STR", "CON", "INT", "DEX", "POW", "CHA", "SIZ", "EDU"}:
            raise ValueError(f"Characteristic {characteristic} not a valid choice.")
        return roll_d100(advantage=advantage) - modifier <= multiplier * self.__getattribute__(characteristic)

    def take_damage(self, amount: int = 0, bypass_armor: bool = False, target: str = None):
        condition = {
            "unconscious": False,
            "major_wound_timer": None,
            "permanent_injury": False,
            "disabled_body_part": None,
            "maimed_body_part": None,
            "severed_body_part": None,
            "dying": False
        }
        if not bypass_armor:
            if isinstance(self.armor_protection, str):
                protection = roll_str(self.armor_protection)
            else:
                protection = self.armor_protection
            amount -= protection
        if amount <= 0:
            return condition

        if target not in self.damage_location:
            self.damage += amount
            if not self.minor_wound and self.damage >= self.major_wound_level:
                self.minor_wound = True
                if self.skills["Luck"].skill_roll(lucky=True)["failure"]:
                    condition["unconscious"] = True
            if amount >= self.major_wound_level:
                self.major_wound = True
                condition["major_wound_timer"] = self.max_hit_points - self.damage
                if self.skills["Luck"].skill_roll(lucky=True)["failure"]:
                    condition["permanent_injury"] = True
            if self.damage >= self.max_hit_points:
                self.fatal_wound = True
                condition["unconscious"] = True
                condition["dying"] = True
        else:
            if self.max_hit_points - self.damage <= 2:
                condition["unconscious"] = True
            if self.max_hit_points - self.damage <= 0:
                condition["dying"] = True
            self.damage_location[target] += amount
            self.damage += min(amount, 2 * self.max_hp_location[target])
            if self.max_hp_location[target] <= self.damage_location[target] < 2 * self.max_hp_location[target]:
                condition["disabled_body_part"] = target
            elif 2 * self.max_hp_location[target] <= self.damage_location[target] < 3 * self.max_hp_location[target]:
                condition["disabled_body_part"] = target
                condition["unconscious"] = True
            elif 3 * self.max_hp_location[target] <= self.damage_location[target] < 4 * self.max_hp_location[target]:
                condition["disabled_body_part"] = target
                condition["unconscious"] = True
                condition["maimed_body_part"] = target
            elif 4 * self.max_hp_location[target] <= self.damage_location[target]:
                condition["disabled_body_part"] = target
                condition["unconscious"] = True
                condition["maimed_body_part"] = target
                condition["severed_body_part"] = target
        return condition

    def heal_damage(self, amount: int = 0, heal_wounds: bool = False, target: str = None):
        self.damage = max(0, self.damage - amount)
        if heal_wounds:
            self.minor_wound = False
            self.major_wound = False
            self.fatal_wound = False
        if target:
            self.damage_location[target] = max(0, self.damage_location[target] - amount)

    def sanity_roll(self, loss_on_success: str = "0", loss_on_fail: str = "0"):
        if roll_d100() <= self.sanity:
            try:
                self.sanity -= int(loss_on_success)
                self.recent_san_loss += int(loss_on_success)
            except ValueError:
                self.sanity -= roll_str(loss_on_success)
                self.recent_san_loss += roll_str(loss_on_success)
        else:
            try:
                self.sanity -= int(loss_on_fail)
                self.recent_san_loss += int(loss_on_fail)
            except ValueError:
                self.sanity -= roll_str(loss_on_fail)
                self.recent_san_loss += roll_str(loss_on_fail)
        if self.recent_san_loss >= self.temp_insanity_score:
            self.temporarily_insane = True
        if self.sanity <= 0:
            self.permanently_insane = True

    def recover_sanity(self, amount: str = "0"):
        """
        Use this to recover sanity or with default amounts to just remove temporary insanity
        """
        try:
            self.sanity += int(amount)
        except ValueError:
            self.sanity += roll_str(amount)
        self.sanity = min(self.sanity, 100 - self.skills["Blasphemous Lore"])
        self.temporarily_insane = False

    def modify_fatigue(self, amount: int = 0):
        self.fatigue += amount


def _intify_success(success: dict = None):
    if success["fumble"]:
        return 1
    if success["failure"]:
        return 2
    if success["critical"]:
        return 5
    if success["special"]:
        return 4
    if success["success"]:
        return 3


def _set_category_bonus(primary: int = 10,
                        secondary1: int = 10,
                        secondary2: int = 10,
                        negative: int = 10) -> int:
    return (primary - 10) + (secondary1 - 10) // 2 + (secondary2 - 10) // 2 + (10 - negative)


def load_character_from_json(filepath: str,
                             CharacterClass: dataclass = BasicRoleplayCharacter,
                             SkillClass: dataclass = BasicRoleplaySkill) -> BasicRoleplayCharacter:
    if issubclass(CharacterClass, BasicRoleplayCharacter):
        with open(filepath, "r") as fh:
            character = CharacterClass(**json.loads(fh.read()))
            character.set_skill_class(SkillClass)
            return character
    raise TypeError("On load a CharacterClass should be a subclass of BasicRoleplayCharacter")


def save_character_to_json(character: BasicRoleplayCharacter, filepath: str):
    temp_var = character.SkillClass
    del character.SkillClass
    data = json.dumps(asdict(character))
    with open(filepath, "w") as fh:
        fh.write(data)
    character.SkillClass = temp_var
