from src.auth.security import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    password = "Admin@123"
    digest = hash_password(password)
    assert digest != password
    assert verify_password(password, digest)

