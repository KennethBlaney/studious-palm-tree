import os

import pytest
from unittest.mock import patch, MagicMock

from src.sheets import BasicRoleplayCharacter, BasicRoleplaySkill, load_character_from_json, save_character_to_json
from tests.sample.raven_game import RavenSkill, RavenCharacter


def test_character_load_save():
    alice = load_character_from_json(os.path.join("tests", "test_characters", "alice.json"))
    assert alice.name == "Alice"
    save_character_to_json(alice, os.path.join("tests", "test_characters", "alice2.json"))


def test_character_load_save_subclass():
    edgar = load_character_from_json(os.path.join("tests", "test_characters", "edgar.json"),
                                     RavenCharacter,
                                     RavenSkill)
    assert edgar.name == "Edgar"
    save_character_to_json(edgar, os.path.join("tests", "test_characters", "edgar2.json"))


class NotACharacter:
    # Dummy class for testing
    pass


def test_load_character_invalid_class_type(tmp_path):
    # Create a temporary JSON file with minimal valid structure
    test_file = tmp_path / "test_char.json"
    test_file.write_text('{}')  # empty JSON content

    # Expect a TypeError when using an invalid CharacterClass
    with pytest.raises(TypeError, match="CharacterClass should be a subclass"):
        load_character_from_json(str(test_file), CharacterClass=NotACharacter)


@pytest.mark.parametrize("current_guilt, guilt_input, expected_failure", [
    (100, 100, True),  # Equal guilt, should fail due to guilt
    (90, 100, True),  # Input exceeds current guilt, should fail
    (100, 0, False),  # No guilt input, should succeed normally
])
def test_guilt_roll_behavior(monkeypatch, current_guilt, guilt_input, expected_failure):
    skill = RavenSkill(name="Confession", chance=75, guilt=current_guilt)

    # Patch skill_roll to return a successful outcome when needed
    monkeypatch.setattr(RavenSkill, "skill_roll", lambda self, *a, **kw: {
        "fumble": False, "failure": False, "success": True,
        "special": False, "critical": False, "roll": 50
    })

    result = skill.guilt_roll(guilt=guilt_input)

    assert result["failure"] == expected_failure
    assert result["guilt"] == expected_failure
    if not expected_failure:
        assert result["success"] is True


def test_add_guilt_positive():
    char = RavenCharacter(name="Crow")
    original_guilt = char.guilt
    char.add_guilt(5)
    assert char.guilt == original_guilt + 5


def test_add_guilt_zero():
    char = RavenCharacter(name="Crow")
    original_guilt = char.guilt
    char.add_guilt(0)
    assert char.guilt == original_guilt  # No change expected


def test_add_guilt_negative():
    char = RavenCharacter(name="Crow")
    original_guilt = char.guilt
    char.add_guilt(-10)
    assert char.guilt == original_guilt  # Negative guilt should not apply


def test_reset_guilt():
    char = RavenCharacter(name="Crow", guilt=42)
    char.reset_guilt()
    assert char.guilt == 0
