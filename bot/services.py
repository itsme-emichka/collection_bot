from models import User


async def get_or_create_user(
        username: str,
        first_name: str = None,
        last_name: str = None) -> User:
    user, is_created = await User.get_or_create(
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    return user
