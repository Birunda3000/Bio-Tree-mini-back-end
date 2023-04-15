import pytest

from app.main.service import create_code


@pytest.mark.parametrize(
    "input, expected", [("admin.;/,^~][{}", "admin"), ("ADMIN123", "admin123")]
)
def test_create_code(input, expected):
    code = create_code(input)

    assert code == expected
