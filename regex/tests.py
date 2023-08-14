import pytest

from regex import *


@pytest.mark.parametrize(
    "text, expec_result",
    [("AA12345", True), ("aA12345", False), ("AA1234", False), ("A12345", False)],
)
def test_is_passport_number(text, expec_result):
    assert is_passport_number(text) == expec_result


@pytest.mark.parametrize(
    "text, expec_result",
    [("1234567890", True), ("12345", False), ("123456789A", False)],
)
def test_is_ipn(text, expec_result):
    assert is_ipn(text) == expec_result


@pytest.mark.parametrize(
    "text, expec_result",
    [
        ("AE1234BB", True),
        ("KE1234AB", True),
        ("AX1234BB", False),
        ("ke1234bb", False),
        ("AA12341AB", False),
    ],
)
def test_is_car_number_dnipro(text, expec_result):
    assert is_car_number_dnipro(text) == expec_result


@pytest.mark.parametrize(
    "text, expec_result",
    [
        ("AX1234BB", True),
        ("KX1234BB", True),
        ("AE1234AB", False),
        ("AA12341AB", False),
        ("aX1234BB", False),
    ],
)
def test_is_car_number_kharkiv(text, expec_result):
    assert is_car_number_kharkiv(text) == expec_result
