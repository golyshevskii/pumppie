class ReprEnum:
    """Base enum for all enums."""

    @classmethod
    def values(cls) -> list[str]:
        return [attr.value for attr in cls]
