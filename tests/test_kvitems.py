"""Tests for the ijson.kvitems method"""

from .test_base import ARRAY_JSON, EMPTY_MEMBER_TEST_CASES, JSON, JSON_KVITEMS, JSON_KVITEMS_META, JSON_OBJECT

import pytest


def test_kvitems(adaptor):
    assert JSON_KVITEMS == adaptor.kvitems(JSON, 'docs.item')


def test_kvitems_toplevel(adaptor):
    kvitems = adaptor.kvitems(JSON, '')
    assert 1 == len(kvitems)
    key, value = kvitems[0]
    assert 'docs' == key
    assert JSON_OBJECT['docs'] == value


def test_kvitems_empty(adaptor):
    assert [] == adaptor.kvitems(JSON, 'docs')


def test_kvitems_twodictlevels(adaptor):
    json = b'{"meta":{"view":{"columns":[{"id": -1}, {"id": -2}]}}}'
    view = adaptor.kvitems(json, 'meta.view')
    assert 1 == len(view)
    key, value = view[0]
    assert 'columns' == key
    assert [{'id': -1}, {'id': -2}] == value


def test_kvitems_different_underlying_types(adaptor):
    assert JSON_KVITEMS_META == adaptor.kvitems(JSON, 'docs.item.meta')


def test_kvitems_array(adaptor):
    assert JSON_KVITEMS == adaptor.kvitems(ARRAY_JSON, 'item.docs.item')


@pytest.mark.parametrize("test_case", [
    pytest.param(value, id=name) for name, value in EMPTY_MEMBER_TEST_CASES.items()
])
def test_kvitems_empty_member(adaptor, test_case):
    assert test_case.kvitems == adaptor.kvitems(test_case.json, test_case.prefix)


def test_coro_needs_input_with_three_elements(backend):
    int_element_parse_events = list(backend.parse(b'{"a": 0}'))
    # all good
    assert [('a', 0)] == list(backend.kvitems(int_element_parse_events, ''))
    # one more element in event
    with pytest.raises(ValueError, match="too many values"):
        next(backend.kvitems((event + ('extra dummy',) for event in int_element_parse_events), ''))
    # one less
    with pytest.raises(ValueError, match="not enough values"):
        next(backend.kvitems((event[:-1] for event in int_element_parse_events), ''))
    # not an iterable
    with pytest.raises(TypeError, match="cannot unpack"):
        next(backend.kvitems([None], ''))