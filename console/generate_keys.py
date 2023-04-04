from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


def generate_asymmetric_keys() -> RSAPrivateKey:
    """Generate new RSA keypair."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def serialize_private_key(keypair: RSAPrivateKey) -> str:
    """Serialize private key and return PEM format."""
    pem = keypair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem


def serialize_public_key(keypair: RSAPrivateKey) -> str:
    """Serialize public key and return PEM format."""
    public_key = keypair.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem


keypair = generate_asymmetric_keys()
print(serialize_public_key(keypair))
print(serialize_private_key(keypair))
