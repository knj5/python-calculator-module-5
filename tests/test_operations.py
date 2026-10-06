import pytest

from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory,
)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 15),
        (-2, 3, 1),
        (0, 0, 0),
        (2.5, 1.5, 4.0),
    ],
)
def test_addition(a, b, expected):
    assert Addition().execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 5),
        (3, 8, -5),
        (0, 0, 0),
    ],
)
def test_subtraction(a, b, expected):
    assert Subtraction().execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 50),
        (-2, 3, -6),
        (0, 100, 0),
    ],
)
def test_multiplication(a, b, expected):
    assert Multiplication().execute(a, b) == expected


def test_division():
    assert Division().execute(10, 2) == 5


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Division().execute(10, 0)


def test_power():
    assert Power().execute(2, 3) == 8


def test_root():
    assert Root().execute(9, 2) == 3


@pytest.mark.parametrize(
    "name,expected_class",
    [
        ("add", Addition),
        ("subtract", Subtraction),
        ("multiply", Multiplication),
        ("divide", Division),
        ("power", Power),
        ("root", Root),
    ],
)
def test_operation_factory(name, expected_class):
    operation = OperationFactory.create_operation(name)
    assert isinstance(operation, expected_class)


def test_operation_factory_invalid():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("invalid")

def test_root_zero_degree():
    with pytest.raises(ValueError):
        Root().execute(9, 0)


def test_root_negative_even():
    with pytest.raises(ValueError):
        Root().execute(-16, 2)


def test_root_negative_odd():
    
    assert Root().execute(-8, 3) == pytest.approx(-2)

def test_abstract_operation_execute():
    assert Operation.execute(None, 1, 2) is None
    
