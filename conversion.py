from dataclasses import dataclass
import random
from typing import List

bindigits = "01"
hexdigits = "0123456789ABCDEF"


def randbin() -> str:
    return "".join(random.choice(bindigits) for _ in range(8))


def randdec() -> int:
    return random.randint(0, 255)


def randhex() -> str:
    return "".join(random.choice(hexdigits) for _ in range(2))


def isbin(value: str) -> bool:
    if len(value) < 2:
        return False
    if not value.startswith("0b"):
        return False
    for char in value[2:]:
        if char not in "01":
            return False
    return True


def isdec(value: str) -> bool:
    return value.isdecimal()


def ishex(value: str) -> bool:
    if len(value) < 2:
        return False
    if not value.startswith("0x"):
        return False
    for char in value[2:]:
        if char not in hexdigits:
            return False
    return True


def generate_questions(num: int) -> "List[Question]":
    questions = []
    for i in range(1, num + 1):
        Question = random.choice((BinaryQuestion,
                                  DecimalQuestion,
                                  HexadecimalQuestion))
        questions.append(Question.random(label=str(i)))
    return questions


@dataclass(kw_only=True)
class Question:
    label: str
    value: str


class BinaryQuestion(Question):
    type: str = "bin"

    @classmethod
    def random(cls, label: str) -> "BinaryQuestion":
        return cls(label=label, value=randbin())


class DecimalQuestion(Question):
    type: str = "dec"

    @classmethod
    def random(cls, label: str) -> "DecimalQuestion":
        return cls(label=label, value=randdec())


class HexadecimalQuestion(Question):
    type: str = "hex"

    @classmethod
    def random(cls, label: str) -> "HexadecimalQuestion":
        return cls(label=label, value=randhex())
