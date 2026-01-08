from enum import Enum


class Priority(Enum):
    """
    Enum representing the priority levels for tasks.
    """
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str):
        """
        Create a Priority enum from a string value.

        Args:
            value: String representation of the priority

        Returns:
            Priority enum value

        Raises:
            ValueError: If the string doesn't match a valid priority
        """
        value = value.lower().capitalize()
        for priority in cls:
            if priority.value.lower() == value.lower():
                return priority
        raise ValueError(f"'{value}' is not a valid Priority. Valid values are: {[p.value for p in cls]}")