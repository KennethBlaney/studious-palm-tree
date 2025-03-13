import os
import unittest
import json

from src.sheets import BasicRoleplayCharacter, BasicRoleplaySkill, load_character_from_json, save_character_to_json
from src.utils import roll_d100, roll_ndm, roll_str


class TestStringMethods(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_character_load(self):
        alice = load_character_from_json(os.path.join("test_characters", "alice.json"))
        self.assertEqual(alice.name, "Alice")

    def test_character_create_with_options(self):
        # fly, drive, energy, tough, education, category bonus
        pass

    def test_character_create_with_simple_options(self):
        # category bonus
        pass

    def test_character_create_without_options(self):
        # fly, drive, energy, tough, education, category bonus
        pass

    def test_character_create_own_language(self):
        pass

    def test_skill_roll(self):
        # fumble, fail, success, special, critical
        # fall back to general
        # with modifier, lucky, difficulty, fatigue, category, armor penalty
        pass

    def test_experience_rolls(self):
        # some skills marked for improve, some not
        pass

    def test_opp_roll_highest(self):
        # test primary char success and failure
        pass

    def test_opp_roll_subtract(self):
        # test primary char success and failure
        pass

    def test_opp_roll_resist_table(self):
        # test primary char success and failure
        pass

    def test_opp_roll_resist_notable(self):
        # test primary char success and failure
        pass

    def test_opp_pow(self):
        # test primary char success and failure
        pass

    def test_pow_improve(self):
        # with and without pow improve flag
        pass

    def test_take_damage_small(self):
        # with and without armor
        # with and without target
        pass

    def test_take_damage_med(self):
        # without target two hits less than major wound level and cause a minor wound
        # without target three hits to bring to 0 hp
        # with target to bring to unconscious
        pass

    def test_take_damage_large(self):
        # with target to disable body part
        # without target to cause major wound
        pass

    def test_take_damage_huge(self):
        # with target to sever body part
        # without target to cause fatal wound
        pass

    def test_heal_damage(self):
        pass

    def test_sanity_roll(self):
        # success and failure
        pass

    def test_recover_sanity(self):
        # test with Blasphemous Lore reducing max SAN
        pass

    def test_modify_fatigue(self):
        # positive and negative
        pass
