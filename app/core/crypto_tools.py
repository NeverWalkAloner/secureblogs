import base64

from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    aead,
    algorithms,
    modes,
)


def generate_symmetric_key() -> bytes:
    """Generate symmetryc key."""
    return aead.AESCCM.generate_key(128)


def symmetric_encryption(message: str, key: bytes) -> str:
    """Encrypt message using symmetric encryption."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode('utf-8'))
    padded_data += padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ct).decode('utf-8')


def symmetric_decryption(ciphertext: str, key: bytes) -> str:
    """Decrypt message using symmetric encryption."""
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    message = (
        decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()
    )
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(message)
    data += unpadder.finalize()
    return data.decode('utf-8')


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
    return pem.decode('utf-8')


def serialize_public_key(keypair: RSAPrivateKey) -> str:
    """Serialize public key and return PEM format."""
    public_key = keypair.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode('utf-8')


def asymmetric_encryption(message: bytes, public_key: RSAPublicKey) -> str:
    """Encrypt message using RSA public key."""
    ciphertext = public_key.encrypt(
        message,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(ciphertext).decode('utf-8')
