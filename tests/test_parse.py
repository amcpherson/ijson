"""Tests for the ijson.parse method"""

import pytest

from .test_base import ARRAY_JSON, ARRAY_JSON_PARSE_EVENTS, JSON, JSON_PARSE_EVENTS

def test_parse(adaptor):
    assert JSON_PARSE_EVENTS == adaptor.parse(JSON)

def test_parse_array(adaptor):
    assert ARRAY_JSON_PARSE_EVENTS == adaptor.parse(ARRAY_JSON)

def test_coro_needs_input_with_two_elements(backend):
    int_element_basic_parse_events = list(backend.basic_parse(b'0', use_float=True))
    # all good
    assert [('', 'number', 0)] == list(backend.parse(int_element_basic_parse_events))
    # one more element in event
    with pytest.raises(ValueError, match="too many values"):
        next(backend.parse(event + ('extra dummy',) for event in int_element_basic_parse_events))
    # one less
    with pytest.raises(ValueError, match="not enough values"):
        next(backend.parse(event[:-1] for event in int_element_basic_parse_events))
    # not an iterable
    with pytest.raises(TypeError, match="cannot unpack"):
        next(backend.parse([None]))
