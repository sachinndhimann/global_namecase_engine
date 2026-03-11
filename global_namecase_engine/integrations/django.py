"""Optional Django integration."""

from __future__ import annotations

from django.db import models

from ..engine import NameCaseEngine

_engine = NameCaseEngine()


class NameCaseField(models.CharField):
    """A CharField that normalizes names before persistence."""

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            return _engine.normalize(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, str):
            value = _engine.normalize(value)
        return super().get_prep_value(value)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if isinstance(value, str):
            normalized = _engine.normalize(value)
            setattr(model_instance, self.attname, normalized)
            return normalized
        return value
