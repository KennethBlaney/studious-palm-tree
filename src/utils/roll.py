from random import randint
from math import fabs


def roll_d100(advantage: int = 0) -> int:
    """
    Makes a percentile dice roll
    :param advantage: a measure of advantage, positive or negative, taking the best or worst of multiple rolls
    :return: a value from the dice roll
    """
    rolls = []
    for _ in range(0, int(fabs(advantage))+1):
        rolls.append(randint(1, 100))
    if advantage > 0:
        return min(rolls)
    return max(rolls)


def roll_ndm(n: int = 0, m: int = 0) -> int:
    """
    Makes a roll of n copies of dice with m sides each
    :return: the sum from the dice roll
    """
    s = 0
    for _ in range(0, n):
        s += randint(1, m)
    return s


def roll_str(roll: str = ""):
    _roll = roll.lower().split("d")
    if len(_roll) == 2:
        try:
            return roll_ndm(int(_roll[0]), int(_roll[1]))
        except ValueError:
            raise ValueError(f"{roll} is not a valid string roll")
    raise ValueError(f"{roll} is not a valid string roll")
