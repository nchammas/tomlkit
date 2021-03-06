import pytest

import tomlkit

from tomlkit import dumps
from tomlkit import loads
from tomlkit import parse
from tomlkit.exceptions import InvalidNumberOrDateError
from tomlkit.exceptions import MixedArrayTypesError
from tomlkit.exceptions import UnexpectedCharError
from tomlkit.items import AoT
from tomlkit.items import Array
from tomlkit.items import Bool
from tomlkit.items import Date
from tomlkit.items import DateTime
from tomlkit.items import Float
from tomlkit.items import InlineTable
from tomlkit.items import Integer
from tomlkit.items import Key
from tomlkit.items import Table
from tomlkit.items import Time
from tomlkit.toml_document import TOMLDocument


@pytest.mark.parametrize(
    "example_name", ["example", "fruit", "hard", "sections_with_same_start"]
)
def test_parse_can_parse_valid_toml_files(example, example_name):
    assert isinstance(parse(example(example_name)), TOMLDocument)
    assert isinstance(loads(example(example_name)), TOMLDocument)


@pytest.mark.parametrize(
    "example_name,error",
    [
        ("section_with_trailing_characters", UnexpectedCharError),
        ("key_value_with_trailing_chars", UnexpectedCharError),
        ("array_with_invalid_chars", UnexpectedCharError),
        ("mixed_array_types", MixedArrayTypesError),
        ("invalid_number", InvalidNumberOrDateError),
    ],
)
def test_parse_raises_errors_for_invalid_toml_files(
    invalid_example, error, example_name
):
    with pytest.raises(error):
        parse(invalid_example(example_name))


@pytest.mark.parametrize("example_name", ["example", "fruit", "hard"])
def test_original_string_and_dumped_string_are_equal(example, example_name):
    content = example(example_name)
    parsed = parse(content)

    assert content == dumps(parsed)


def test_integer():
    i = tomlkit.integer("34")

    assert isinstance(i, Integer)


def test_float():
    i = tomlkit.float_("34.56")

    assert isinstance(i, Float)


def test_boolean():
    i = tomlkit.boolean("true")

    assert isinstance(i, Bool)


def test_date():
    dt = tomlkit.date("1979-05-13")

    assert isinstance(dt, Date)

    with pytest.raises(ValueError):
        tomlkit.date("12:34:56")


def test_time():
    dt = tomlkit.time("12:34:56")

    assert isinstance(dt, Time)

    with pytest.raises(ValueError):
        tomlkit.time("1979-05-13")


def test_datetime():
    dt = tomlkit.datetime("1979-05-13T12:34:56")

    assert isinstance(dt, DateTime)

    with pytest.raises(ValueError):
        tomlkit.time("1979-05-13")


def test_array():
    a = tomlkit.array()

    assert isinstance(a, Array)

    a = tomlkit.array("[1,2, 3]")

    assert isinstance(a, Array)


def test_table():
    t = tomlkit.table()

    assert isinstance(t, Table)


def test_inline_table():
    t = tomlkit.inline_table()

    assert isinstance(t, InlineTable)


def test_aot():
    t = tomlkit.aot()

    assert isinstance(t, AoT)


def test_key():
    k = tomlkit.key("foo")

    assert isinstance(k, Key)


def test_key_value():
    k, i = tomlkit.key_value("foo = 12")

    assert isinstance(k, Key)
    assert isinstance(i, Integer)
