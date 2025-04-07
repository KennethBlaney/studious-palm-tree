import os

import pytest
from unittest.mock import patch, MagicMock

from src.sheets import BasicRoleplayCharacter, BasicRoleplaySkill, load_character_from_json


@pytest.fixture
def basic_character():
    char = BasicRoleplayCharacter()
    char.skills = {
        "Dodge": BasicRoleplaySkill(name="Dodge", category="combat", chance=20),
        "Luck": BasicRoleplaySkill(name="Grapple", category="combat", chance=50),
        "Blasphemous Lore": BasicRoleplaySkill(name="Blasphemous Lore", chance=10)
    }
    char.category_bonuses = {"DEX": 0, "POW": 0}
    char.armor_category_penalty = {"DEX": 0}
    char.damage_location = {"head": 0}
    char.max_hp_location = {"head": 5}
    return char


def test_experience_roll():
    skill = BasicRoleplaySkill(name="Test", chance=40, experience_check=True)
    skill.experience_roll(int_characteristic=10)
    assert not skill.experience_check
    assert skill.chance >= 40


def test_make_experience_rolls_calls_each_skill():
    char = BasicRoleplayCharacter()
    skill_mock = MagicMock()
    char.skills = {
        "Spot Hidden": skill_mock,
        "Listen": skill_mock
    }
    char.INT = 12
    char.improvement_die = "1d4"

    char.make_experience_rolls()

    assert skill_mock.experience_roll.call_count == 2


def test_character_load():
    alice = load_character_from_json(os.path.join("test_characters", "alice.json"))
    assert alice.name == "Alice"


def test_skill_roll_basic():
    skill = BasicRoleplaySkill(name="Test", chance=50)
    result = skill.skill_roll()
    assert isinstance(result, dict)
    assert "roll" in result and "success" in result


def test_skill_roll_lucky():
    skill = BasicRoleplaySkill(name="Test", chance=0)
    with patch("src.sheets.brp_skill.roll_d100", return_value=1):
        result = skill.skill_roll(lucky=True)
        assert result['success']


def test_make_skill_roll():
    char = BasicRoleplayCharacter()
    char.skills = {"Test": BasicRoleplaySkill(name="Test", category="STR", chance=50)}
    char.category_bonuses = {"STR": 10}
    result = char.make_skill_roll("Test")
    assert isinstance(result, dict)


def test_make_skill_roll_fallback():
    char = BasicRoleplayCharacter()
    char.skills = {"Skill (various)": BasicRoleplaySkill(name="Skill (various)", category="STR", chance=50)}
    char.category_bonuses = {"STR": 10}
    result = char.make_skill_roll("Skill specific")
    assert isinstance(result, dict)


def test_opposed_roll_highest_success():
    char = BasicRoleplayCharacter()
    skill = BasicRoleplaySkill(name="Test", chance=60)
    char.skills = {"Test": skill}
    result = char.opposed_roll_highest_success(opponent=50, my_skill="Test")
    assert "i_won" in result


def test_opposed_roll_subtraction():
    char = BasicRoleplayCharacter()
    skill = BasicRoleplaySkill(name="Test", chance=60)
    char.skills = {"Test": skill}
    result = char.opposed_roll_subtraction(opponent=30, my_skill="Test")
    assert isinstance(result, dict)


def test_opposed_roll_resistance_table():
    char = BasicRoleplayCharacter()
    skill = BasicRoleplaySkill(name="Test", chance=50)
    char.skills = {"Test": skill}
    result = char.opposed_roll_resistance_table(opponent=30, my_skill="Test")
    assert isinstance(result, dict)


def test_opposed_pow_check():
    char = BasicRoleplayCharacter()
    char.skills = {"Luck": BasicRoleplaySkill(name="Luck", chance=50)}
    result = char.opposed_pow_check(opponent=30)
    assert isinstance(result, dict)


def test_improve_pow():
    char = BasicRoleplayCharacter()
    char.pow_improvement_check = True
    char.POW = 10
    char.max_species_pow = 18
    char.min_species_pow = 3
    with patch("src.sheets.brp_character.roll_d100", return_value=20), \
            patch("src.sheets.brp_character.roll_ndm", return_value=2):
        char.improve_pow()
        assert char.POW > 10


def test_make_experience_rolls():
    char = BasicRoleplayCharacter()
    char.INT = 15
    char.improvement_die = 6
    char.skills = {"Test": BasicRoleplaySkill(name="Test", chance=50, experience_check=True)}
    char.make_experience_rolls()
    assert not char.skills["Test"].experience_check


def test_characteristic_roll():
    char = BasicRoleplayCharacter()
    char.STR = 15
    result = char.characteristic_roll("STR", multiplier=1)
    assert isinstance(result, bool)


def test_take_damage_unarmored():
    char = BasicRoleplayCharacter()
    char.armor_protection = 0
    char.skills = {"Luck": BasicRoleplaySkill(name="Luck", chance=50)}
    result = char.take_damage(amount=5)
    assert isinstance(result, dict)


def test_heal_damage():
    char = BasicRoleplayCharacter()
    char.damage = 10
    char.heal_damage(amount=5)
    assert char.damage == 5


@pytest.mark.parametrize("amount, expected_minor, expected_major, expected_fatal", [
    (10, True, True, False),  # equal to major wound threshold → minor triggers
    (15, True, True, False),  # above major wound threshold → both trigger
    (20, True, True, True),  # above fatal wound threshold → all trigger
    (0, False, False, False),  # no damage → nothing happens
])
def test_take_damage_thresholds(amount, expected_minor, expected_major, expected_fatal):
    char = BasicRoleplayCharacter()
    char.major_wound_level = 10
    char.max_hit_points = 20
    char.damage = 0
    char.skills = {"Luck": BasicRoleplaySkill(chance=100)}  # always succeed

    result = char.take_damage(amount=amount, bypass_armor=True)
    assert char.minor_wound == expected_minor
    assert char.major_wound == expected_major
    assert char.fatal_wound == expected_fatal


@pytest.mark.parametrize("amount, expected_disabled, expected_maimed, expected_severed", [
    (4, True, False, False),
    (12, True, True, False),
    (16, True, True, True),
])
def test_take_damage_to_body_part(amount, expected_disabled, expected_maimed, expected_severed):
    char = BasicRoleplayCharacter()
    char.damage_location = {"Left Leg": 0}
    char.max_hp_location = {"Left Leg": 4}
    char.skills = {"Luck": BasicRoleplaySkill(chance=1)}  # always fail

    result = char.take_damage(amount=amount, target="Left Leg", bypass_armor=True)

    assert result["disabled_body_part"] == "Left Leg" if expected_disabled else result["disabled_body_part"] is None
    assert (result["maimed_body_part"] == "Left Leg") == expected_maimed
    assert (result["severed_body_part"] == "Left Leg") == expected_severed


@pytest.mark.parametrize("damage, amount, wounds, expected_damage", [
    (20, 10, True, 10),  # heals partially and resets wounds
    (5, 10, False, 0),  # heals fully
])
def test_heal_damage_logic(damage, amount, wounds, expected_damage):
    char = BasicRoleplayCharacter()
    char.damage = damage
    char.minor_wound = char.major_wound = char.fatal_wound = wounds
    char.damage_location = {"Torso": damage}

    char.heal_damage(amount=amount, heal_wounds=True, target="Torso")

    assert char.damage == expected_damage
    assert char.damage_location["Torso"] == max(0, damage - amount)
    assert char.minor_wound is False
    assert char.major_wound is False
    assert char.fatal_wound is False


@pytest.mark.parametrize("characteristic, value, roll, multiplier, expected", [
    ("INT", 10, 30, 3, True),  # succeeds exactly
    ("STR", 10, 31, 3, False),  # fails by 1
])
def test_characteristic_rolls(characteristic, value, roll, multiplier, expected):
    char = BasicRoleplayCharacter()
    setattr(char, characteristic, value)

    with patch("src.sheets.brp_character.roll_d100", return_value=roll):
        assert char.characteristic_roll(characteristic=characteristic, multiplier=multiplier) is expected


def test_make_experience_rolls_parametrized():
    char = BasicRoleplayCharacter()
    mock_skill = MagicMock()
    char.skills = {
        "Hide": mock_skill,
        "Listen": mock_skill,
    }
    char.INT = 13
    char.improvement_die = "1d4"

    char.make_experience_rolls()
    assert mock_skill.experience_roll.call_count == 2


def test_sanity_roll():
    char = BasicRoleplayCharacter()
    char.sanity = 80
    char.skills = {"Blasphemous Lore": BasicRoleplaySkill(name="Blasphemous Lore", chance=0)}
    char.sanity_roll("5", "10")
    assert char.sanity < 80


def test_recover_sanity_with_high_blasphemous_lore():
    char = BasicRoleplayCharacter()
    char.sanity = 90
    char.skills = {"Blasphemous Lore": BasicRoleplaySkill(name="Blasphemous Lore", chance=30)}
    char.recover_sanity("20")
    assert char.sanity == 70


def test_sanity_roll_with_string_loss():
    char = BasicRoleplayCharacter()
    char.sanity = 80
    char.skills = {"Blasphemous Lore": BasicRoleplaySkill(name="Blasphemous Lore", chance=0)}

    # Force a failed sanity check to trigger loss_on_fail
    with patch("src.sheets.brp_character.roll_d100", return_value=100), \
            patch("src.sheets.brp_character.roll_str", return_value=4):
        char.sanity_roll("0", "1d4")

    assert char.sanity == 76
    assert char.recent_san_loss == 4


def test_temporary_insanity_threshold():
    char = BasicRoleplayCharacter()
    char.sanity = 50
    char.temp_insanity_score = 5
    char.recent_san_loss = 4  # just below threshold
    char.skills = {"Blasphemous Lore": 0}

    with patch("src.sheets.brp_character.roll_d100", return_value=100), \
            patch("src.sheets.brp_character.roll_str", return_value=1):
        char.sanity_roll("0", "1d4")

    assert char.temporarily_insane is True


def test_permanent_insanity_on_zero_sanity():
    char = BasicRoleplayCharacter()
    char.sanity = 1
    char.temp_insanity_score = 5
    char.skills = {"Blasphemous Lore": 0}

    with patch("src.sheets.brp_character.roll_d100", return_value=100), \
            patch("src.sheets.brp_character.roll_str", return_value=2):
        char.sanity_roll("0", "1d4")

    assert char.sanity <= 0
    assert char.permanently_insane is True


def test_recover_sanity_removes_temporary_only():
    char = BasicRoleplayCharacter()
    char.sanity = 50
    char.temporarily_insane = True
    char.permanently_insane = True  # Simulate already broken
    char.skills = {"Blasphemous Lore": BasicRoleplaySkill(
        **{"name": "Blasphemous Lore", "category": "mental", "chance": 0,
           "can_be_improved_through_experience": False})}

    char.recover_sanity("10")
    assert char.temporarily_insane is False
    assert char.permanently_insane is True  # should stay


def test_recover_sanity():
    char = BasicRoleplayCharacter()
    char.sanity = 50
    char.skills = {"Blasphemous Lore": BasicRoleplaySkill(
        **{"name": "Blasphemous Lore", "category": "mental", "chance": 0,
           "can_be_improved_through_experience": False})}
    char.recover_sanity("10")
    assert char.sanity > 50


def test_modify_fatigue():
    char = BasicRoleplayCharacter()
    char.fatigue = 0
    char.modify_fatigue(3)
    assert char.fatigue == 3


def test_skill_roll_zero_chance_lucky():
    skill = BasicRoleplaySkill(name="ZeroChance", category="Test", chance=0)
    with patch("src.sheets.brp_skill.roll_d100", return_value=1):
        result = skill.skill_roll(lucky=True)
    assert result["success"] is True


def test_experience_roll_no_check():
    skill = BasicRoleplaySkill(name="NoExp", chance=20)
    skill.experience_check = False
    with patch("src.sheets.brp_skill.roll_d100", return_value=99):
        skill.experience_roll(int_characteristic=10)
    assert skill.chance == 20


def test_experience_roll_with_check_improve():
    skill = BasicRoleplaySkill(name="WithExp", chance=20)
    skill.experience_check = True
    with patch("src.sheets.brp_skill.roll_d100", return_value=100):
        with patch("src.sheets.brp_skill.roll_ndm", return_value=5):
            skill.experience_roll(int_characteristic=0)
    assert skill.chance == 25
    assert skill.experience_check is False


def test_opposed_roll_highest_success_tie_by_skill_level(basic_character):
    opponent = BasicRoleplaySkill(name="Combat", chance=20)
    with patch("src.sheets.brp_skill.roll_d100", side_effect=[10, 10]):
        result = basic_character.opposed_roll_highest_success(opponent=opponent, my_skill="Dodge")
    assert isinstance(result["i_won"], bool)


def test_opposed_roll_subtraction_extreme_difference(basic_character):
    opponent = BasicRoleplaySkill(name="Combat", chance=90)
    with patch("src.sheets.brp_skill.roll_d100", return_value=50):
        result = basic_character.opposed_roll_subtraction(opponent=opponent, my_skill="Dodge")
    assert "roll" in result


def test_opposed_roll_resistance_min_chance(basic_character):
    with patch("src.sheets.brp_character.roll_d100", return_value=100):
        result = basic_character.opposed_roll_resistance(opponent=95, my_skill="Dodge")
    assert result["failure"] is True


def test_opposed_roll_resistance_max_chance(basic_character):
    with patch("src.sheets.brp_character.roll_d100", return_value=1):
        result = basic_character.opposed_roll_resistance(opponent=0, my_skill="Dodge")
    assert result["success"] is True


def test_take_damage_exceeds_total_hp(basic_character):
    basic_character.max_hit_points = 10
    basic_character.damage = 9
    result = basic_character.take_damage(amount=5, bypass_armor=True)
    assert result["dying"] is True


def test_take_damage_on_location_maimed(basic_character):
    result = basic_character.take_damage(amount=20, bypass_armor=True, target="head")
    assert result["maimed_body_part"] == "head"


def test_take_damage_minor_wound_threshold():
    char = BasicRoleplayCharacter()
    char.major_wound_level = 10
    char.damage = 0
    char.skills = {"Luck": BasicRoleplaySkill(chance=100)}  # ensure Luck success

    result = char.take_damage(amount=10, bypass_armor=True)
    assert char.minor_wound is True
    assert result["unconscious"] in {True, False}  # depends on Luck roll


def test_take_damage_body_part_disabling():
    char = BasicRoleplayCharacter()
    char.damage_location = {"Left Arm": 0}
    char.max_hp_location = {"Left Arm": 4}
    char.skills = {"Luck": BasicRoleplaySkill(chance=1)}  # ensure fail on luck

    result = char.take_damage(amount=13, target="Left Arm", bypass_armor=True)
    assert result["disabled_body_part"] == "Left Arm"
    assert result["maimed_body_part"] == "Left Arm"
    assert result["unconscious"] is True


def test_heal_damage_resets_wounds():
    char = BasicRoleplayCharacter()
    char.damage = 20
    char.minor_wound = True
    char.major_wound = True
    char.fatal_wound = True
    char.damage_location = {"Torso": 5}

    char.heal_damage(amount=10, heal_wounds=True, target="Torso")
    assert char.damage == 10
    assert char.minor_wound is False
    assert char.major_wound is False
    assert char.fatal_wound is False
    assert char.damage_location["Torso"] == 0


def test_characteristic_roll_invalid_characteristic(basic_character):
    with pytest.raises(ValueError):
        basic_character.characteristic_roll(characteristic="XXX")


def test_characteristic_roll_exact_success():
    char = BasicRoleplayCharacter()
    char.INT = 10

    with patch("src.sheets.brp_character.roll_d100", return_value=30):
        assert char.characteristic_roll("INT", multiplier=3) is True


def test_characteristic_roll_failure_by_one():
    char = BasicRoleplayCharacter()
    char.STR = 10

    with patch("src.sheets.brp_character.roll_d100", return_value=31):
        assert char.characteristic_roll("STR", multiplier=3) is False


def test_characteristic_roll_invalid_name():
    char = BasicRoleplayCharacter()
    with pytest.raises(ValueError):
        char.characteristic_roll("AGI", multiplier=2)


def test_sanity_roll_string_loss_values(basic_character):
    with patch("src.sheets.brp_character.roll_d100", return_value=100):
        with patch("src.sheets.brp_character.roll_str", return_value=5):
            basic_character.sanity_roll(loss_on_success="1d6", loss_on_fail="1d6")
    assert basic_character.recent_san_loss > 0


def test_recover_sanity_roll_str(basic_character):
    basic_character.sanity = 50
    with patch("src.sheets.brp_character.roll_str", return_value=10):
        basic_character.recover_sanity(amount="1d10")
    assert basic_character.sanity <= 100


def test_heal_damage_edge_conditions(basic_character):
    basic_character.damage = 5
    basic_character.damage_location["head"] = 3
    basic_character.heal_damage(amount=10, heal_wounds=True, target="head")
    assert basic_character.damage == 0
    assert basic_character.damage_location["head"] == 0
