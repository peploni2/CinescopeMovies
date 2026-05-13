import pytest

@pytest.mark.ui
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.db
def test_subtraction():
    assert 5-3 == 2

skip_test = True
@pytest.mark.skipif(skip_test, reason="Тест отключен вручную")
def test_multiplication():
    assert 2 * 3 == 6

@pytest.mark.slow
def test_division():
    assert 10/2==5