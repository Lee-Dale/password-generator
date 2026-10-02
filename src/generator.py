import secrets
import string

ALPHABET = string.ascii_letters + string.digits + "-_"
MIN_LENGTH = 12  # 4 lowercase + 4 uppercase + 4 digits


def generate_password(length=20):
    if length < MIN_LENGTH:
        raise ValueError(f"length must be at least {MIN_LENGTH}")

    while True:
        password = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if (
            sum(c.islower() for c in password) >= 4
            and sum(c.isupper() for c in password) >= 4
            and sum(c.isdigit() for c in password) >= 4
        ):
            return password