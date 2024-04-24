import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, hashed_password, status_code",
    [
        ("user@example.com", "stringst", 201),
        ("user@example.com", "stringst", 409),
        ("incorrectEmail", "stringst", 422),
        ("user@example.com", "wrngPas", 422),  # меньше 8 символов
    ],
)
async def test_register(email, hashed_password, status_code, ac: AsyncClient):
    response = await ac.post(
        url="/auth/reg", json={"email": email, "hashed_password": hashed_password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, hashed_password, status_code",
    [
        ("test@test.ru", "testtest", 200),
        ("test@test.ru", "incorrect", 400),
        ("incorrect", "testtest", 422),
    ],
)
async def test_login(email, hashed_password, status_code, ac: AsyncClient):
    response = await ac.post(
        url="/auth/signup", json={"email": email, "hashed_password": hashed_password}
    )
    assert response.status_code == status_code


async def test_get_all(auth_ac: AsyncClient):
    response = await auth_ac.get(url="/auth/", params={"withtasks": True})
    assert response.status_code == 200
