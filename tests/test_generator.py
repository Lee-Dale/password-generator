import pytest

from src.generator import ALPHABET, generate_password


def test_default_length():
    assert len(generate_password()) == 21


def test_custom_length():
    assert len(generate_password(32)) == 32


def test_only_allowed_characters():
    password = generate_password()
    assert all(c in ALPHABET for c in password)


def test_character_mix():
    for _ in range(100):
        password = generate_password()
        assert sum(c.islower() for c in password) >= 4
        assert sum(c.isupper() for c in password) >= 4
        assert sum(c.isdigit() for c in password) >= 4


def test_too_short_raises_error():
    with pytest.raises(ValueError):
        generate_password(5)