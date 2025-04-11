import pytest
import language


@pytest.mark.parametrize("code,result", [
    ("2 + 2", "4"),
    ("2 + 3", "5"),
    ("10 + 1", "11"),
    ("10 * 2", "20"),
])
def test_interpret(code, result):
    assert language.interpret(code) == result
