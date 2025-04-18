import pytest
import language


@pytest.mark.parametrize("code,result", [
    ("1.0", "1.0"),
    ("3.14", "3.14"),
    ("2 + 2", "4"),
    ("2 \n+ 2", "4"),
    ("2 +\n 2", "4"),
    ("2 + 3", "5"),
    ("10 + 1", "11"),
    ("10 * 2", "20"),
    ("1 + 2 + 3 + 4 + 5", "15"),
    ("1*1", "1"),
    ("1/1", "1.0"),
    ("1/0", "ZeroDivisionError: division by 0"),
    ("(1 + 1)", "2"),
    ("(1 + 1) + 1", "3"),
    ("1 + (2 * 3)", "7"),
    ("2 ++ 3", "SyntaxError: expected digit found '+'"),
])
def test_interpret(code, result):
    assert language.interpret(code)["message"] == result
