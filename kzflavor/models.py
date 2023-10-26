from django.db import models
from django.core.exceptions import ValidationError
from django.db import models


def validate_iin(value: str) -> None:
    """Проверка на валидность ИИН."""
    if not value.isdigit() or len(value) != 12:
        raise ValidationError('Неверный формат ИИН.')


def validate_id_card(value: str) -> None:
    """Проверка на валидность номера удостоверения."""
    if not value.isdigit() or len(value) != 9:
        raise ValidationError('Неверный формат номера удостоверения.')


class KZIINField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super().__init__(*args, **kwargs)
        self.validators.append(validate_iin)


class KZIDCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9
        super().__init__(*args, **kwargs)
        self.validators.append(validate_id_card)




