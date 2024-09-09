"""Tests for the ijson.items method"""

import collections
import pytest

from .test_base import ARRAY_JSON, ARRAY_JSON_OBJECT, EMPTY_MEMBER_TEST_CASES, JSON, JSON_OBJECT

from ijson import JSONError

def test_items(adaptor):
    assert [JSON_OBJECT] == adaptor.items(JSON, '')


def test_items_array(adaptor):
    assert [ARRAY_JSON_OBJECT] == adaptor.items(ARRAY_JSON, '')


def test_items_twodictlevels(adaptor):
    json = b'{"meta":{"view":{"columns":[{"id": -1}, {"id": -2}]}}}'
    ids = adaptor.items(json, 'meta.view.columns.item.id')
    assert 2 == len(ids)
    assert [-2,-1], sorted(ids)


@pytest.mark.parametrize(
    "json, prefix, expected_items",
    (
        (b'{"0.1": 0}', '0.1', [0]),
        (b'{"0.1": [{"a.b": 0}]}', '0.1.item.a.b', [0]),
        (b'{"0.1": 0, "0": {"1": 1}}', '0.1', [0, 1]),
        (b'{"abc.def": 0}', 'abc.def', [0]),
        (b'{"abc.def": 0}', 'abc', []),
        (b'{"abc.def": 0}', 'def', []),
    )
)
def test_items_with_dotted_name(adaptor, json, prefix, expected_items):
    assert expected_items == adaptor.items(json, prefix)


def test_map_type(adaptor):
    obj = adaptor.items(JSON, '')[0]
    assert isinstance(obj, dict)
    obj = adaptor.items(JSON, '', map_type=collections.OrderedDict)[0]
    assert isinstance(obj, collections.OrderedDict)


@pytest.mark.parametrize("test_case", [
    pytest.param(value, id=name) for name, value in EMPTY_MEMBER_TEST_CASES.items()
])
def test_items_empty_member(adaptor, test_case):
    assert test_case.items == adaptor.items(test_case.json, test_case.prefix)


def test_multiple_values_raises_if_not_supported(adaptor):
    """Test that setting multiple_values raises if not supported"""
    if not adaptor.backend.capabilities.multiple_values:
        with pytest.raises(ValueError):
            adaptor.items("", "", multiple_values=True)


def test_multiple_values(adaptor):
    """Test that multiple_values are supported"""
    multiple_json = JSON + JSON + JSON
    with pytest.raises(JSONError):
        adaptor.items(multiple_json, "")
    with pytest.raises(JSONError):
        adaptor.items(multiple_json, "", multiple_values=False)
    result = adaptor.items(multiple_json, "", multiple_values=True)
    assert [JSON_OBJECT, JSON_OBJECT, JSON_OBJECT] == result
