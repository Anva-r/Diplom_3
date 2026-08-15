from uuid import uuid4


def generate_user_data() -> dict:
    suffix = uuid4().hex
    return {
        "email": f"diplom_ui_{suffix}@yandex.ru",
        "password": f"Password-{suffix}",
        "name": f"Pilot-{suffix[:8]}",
    }
