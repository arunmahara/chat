from typing import Type, Optional
from django.db.models import Model


def get_or_none(model: Type[Model], *args, **kwargs) -> Optional[Model]:
    """
    Return object if exists, otherwise None.
    """
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
