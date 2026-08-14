"""Smoke tests: package imports and core-model integrity checks."""

import pytest

import ibrt_cce
from ibrt_cce.core.model import StructuralModel


def test_version() -> None:
    assert ibrt_cce.__version__


def test_model_rejects_unknown_references() -> None:
    model = StructuralModel()
    model.add_node("N1", 0, 0, 0)
    with pytest.raises(KeyError):
        model.add_member("M1", "N1", "MISSING", "steel", "sec")
    with pytest.raises(ValueError):
        model.add_node_load("N1", "SIDEWAYS", 1.0)
