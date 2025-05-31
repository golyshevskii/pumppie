from enum import StrEnum

from core.fields.base import ReprEnum


class LLModel(ReprEnum, StrEnum):
    """The model to use for the agent."""

    TEST = "test"
    GPT_4_1_MINI = "gpt-4.1-mini"


if __name__ == "__main__":
    print(LLModel.values())
