from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_date_greater_than_today(value):
    if value < timezone.now().date():
        raise ValidationError("Date must be greater than or equal to today.")