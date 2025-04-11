import pytest
import language


@pytest.mark.parametrize("code,result", [
    ("2 + 2", "4"),
    ("2 + 3", "5"),
    ("10 + 1", "11"),
    ("10 * 2", "20"),
    ("1 + 2 + 3 + 4 + 5", "15"),
    ("1*1", "1"),
    ("1-1", "0"),
    # ("1 + 2 * 3", "7"),
])
def test_interpret(code, result):
    assert language.interpret(code) == result
