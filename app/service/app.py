from app import service
from app.models import User, Wallet


def create_user(phone_number: str) -> User:
    wallet_keys = service.create_wallet()
    user = User.objects.create(
        username=phone_number,  # Using phone as username
        handle=phone_number,
        is_staff=True,
        is_superuser=True,
    )
    wallet = Wallet(
        user=user,
        address=str(wallet_keys["address"]),
        private_key=wallet_keys["private_key"]
    )
    user.set_unusable_password()  # Since we're using phone auth
    user.save()
    wallet.save()
    return user