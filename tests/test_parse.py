"""Tests for the ijson.parse method"""

from .test_base import ARRAY_JSON, ARRAY_JSON_PARSE_EVENTS, JSON, JSON_PARSE_EVENTS

def test_parse(adaptor):
    assert JSON_PARSE_EVENTS == adaptor.parse(JSON)

def test_parse_array(adaptor):
    assert ARRAY_JSON_PARSE_EVENTS == adaptor.parse(ARRAY_JSON)
