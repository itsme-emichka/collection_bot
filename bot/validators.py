from typing import Any
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError


AVAILABLE_FOR_SLUG: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_-'


class SlugValidator(Validator):
    '''
    A validator to check if value is slug or not
    '''
    def __call__(self, value: Any):
        if len(value.split()) > 1:
            raise ValidationError(
                'Value can only be one word and ' +
                'contain english letters and symbols: "_-"'
            )
        for letter in value:
            if letter not in AVAILABLE_FOR_SLUG:
                raise ValidationError(
                    'Value can only be one word and ' +
                    'contain english letters and symbols: "_-"'
                )
