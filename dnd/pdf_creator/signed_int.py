from __future__ import annotations


class SignedInt:
    def __init__(self, integer: int):
        self.integer = integer

    def __str__(self):
        return ("+" if self.integer >= 0 else "") + str(self.integer)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError
        return type(self)(self.integer + other)
