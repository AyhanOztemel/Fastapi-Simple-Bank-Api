# utils/value_objects.py
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        object.__setattr__(self, 'amount', Decimal(self.amount).quantize(Decimal('0.01')))

    def __add__(self, other: 'Money') -> 'Money':
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount + other.amount, self.currency)
        raise ValueError("Cannot add different currencies")

    def __sub__(self, other: 'Money') -> 'Money':
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount - other.amount, self.currency)
        raise ValueError("Cannot subtract different currencies")

    def __mul__(self, multiplier: Union[int, float, Decimal]) -> 'Money':
        return Money(self.amount * Decimal(multiplier), self.currency)

    def __truediv__(self, divisor: Union[int, float, Decimal]) -> 'Money':
        return Money(self.amount / Decimal(divisor), self.currency)

    def __str__(self):
        return f"{self.amount} {self.currency}"

@dataclass(frozen=True)
class AccountNumber:
    value: str

    def __post_init__(self):
        if not self.value.isdigit(): # or len(self.value) != 10:
            raise ValueError("Account number must be a 10-digit number")

    def __str__(self):
        return self.value
