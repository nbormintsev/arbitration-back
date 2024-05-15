from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


class KeysManager:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()


keys_manager = KeysManager()
