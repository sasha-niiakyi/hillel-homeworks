from drunk_polish_calculator import *
import pytest


@pytest.mark.parametrize(
    "x, y, expec_result", [(2, 2, 4), (5, -3, 2), (3.2, 7, 10.2), (-3, -2, -5)]
)
def test_op_plus(x, y, expec_result):
    assert op_plus(x, y) == expec_result


@pytest.mark.parametrize(
    "x, y, expec_exception",
    [("2", 2, TypeError), ("2", "3", TypeError), ((2, 3), -3, TypeError)],
)
def test_op_plus_error(x, y, expec_exception):
    with pytest.raises(expec_exception):
        op_plus(x, y)


@pytest.mark.parametrize(
    "x, y, expec_result", [(2, 3, -1), (5, -3, 8), (3, 2.8, 0.2), (-4, -2, -2)]
)
def test_op_minus(x, y, expec_result):
    assert op_minus(x, y) == expec_result


@pytest.mark.parametrize(
    "x, y, expec_exception",
    [("2", 2, TypeError), ("2", "3", TypeError), ((2, 3), -3, TypeError)],
)
def test_op_minus_error(x, y, expec_exception):
    with pytest.raises(expec_exception):
        op_minus(x, y)


@pytest.mark.parametrize(
    "x, y, expec_result", [(2, 3, 6), (5, -3, -15), (1, 7, 7), (10, 0.3, 3), (-2, -2, 4)]
)
def test_op_multiply(x, y, expec_result):
    assert op_multiply(x, y) == expec_result


@pytest.mark.parametrize(
    "x, y, expec_exception",
    [("2", 2, TypeError), ("2", "3", TypeError), ((2, 3), -3, TypeError)],
)
def test_op_multiply_error(x, y, expec_exception):
    with pytest.raises(expec_exception):
        op_multiply(x, y)


@pytest.mark.parametrize(
    "x, y, expec_result",
    [(6, 2, 3), (0, 5, 0), (5, -3, -15), (-7, -1, 7), (10, 0.5, 20.0)],
)
def test_op_divide(x, y, expec_result):
    assert op_divide(x, y) == expec_result


@pytest.mark.parametrize(
    "x, y, expec_exception",
    [
        ("2", 2, TypeError),
        (2, 0, ZeroDivisionError),
        ("2", "3", TypeError),
        ((2, 3), -3, TypeError),
    ],
)
def test_op_divide_error(x, y, expec_exception):
    with pytest.raises(expec_exception):
        op_divide(x, y)


@pytest.mark.parametrize(
    "value, expec_result",
    [
        ("2 2 +", "4.0"),
        ("3 2 -", "1.0"),
        ("3 2 *", "6.0"),
        ("6 2 /", "3.0"),
        ("2 2 + 4 +", "8.0"),
        ("4 2 + 3 * 2 / 8 -", "1.0"),
    ],
)
def test_main(monkeypatch, capsys, value, expec_result):
    def mock_input(less):
        return value

    monkeypatch.setattr("builtins.input", mock_input)

    main()
    result = capsys.readouterr().out
    assert result == (expec_result + "\n")


@pytest.mark.parametrize(
    "value, expec_exception",
    [
        ("2 2", SyntaxError),
        ("2 +", SyntaxError),
        ("a 2 +", ValueError),
        ("", SyntaxError),
    ],
)
def test_main_error(monkeypatch, capsys, value, expec_exception):
    def mock_input(less):
        return value

    monkeypatch.setattr("builtins.input", mock_input)

    with pytest.raises(expec_exception):
        main()
