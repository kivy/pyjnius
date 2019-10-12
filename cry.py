from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def gen(key_name):
    'generate a public/private keypair'
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open(f'{key_name}_priv.pem', 'wb') as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(f'{key_name}_pub.pem', 'wb') as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def decrypt(key_name, message):
    'decrypt a base64 encoded version of an encoded message passed as a parameter'
    message = b64decode(message)

    with open(f"{key_name}_priv.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    print(
        private_key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf8')
    )



def encrypt(key_name, message):
    'print a base64 encoded version of a message encrypted with the key'
    message = message.encode('utf8')

    with open(f"{key_name}_pub.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print(b64encode(encrypted).decode('utf8'))


if __name__ == '__main__':
    import fire
    fire.Fire({
        'gen': gen,
        'decrypt': decrypt,
        'encrypt': encrypt
    })
