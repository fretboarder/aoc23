import hashlib
import os
from pathlib import Path
from typing import Protocol, TypeVar

import keyring
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

T_co = TypeVar("T_co", covariant=True)


class LineParser(Protocol[T_co]):
    def __call__(self, line: str) -> T_co:
        ...


def default_parser(line: str) -> str:
    return line


def get_input(
    inputfile: Path,
    line_parser: LineParser[T_co] = default_parser,  # type: ignore  # noqa: PGH003
) -> list[T_co]:
    if inputfile.exists():
        content = inputfile.open("r").read()
    elif (encrypted_file := Path(str(inputfile) + ".enc")).exists():
        key = get_aoc_secret("aoc2023", "encryptionkey")
        if key:
            content = decrypted_content(encrypted_file, bytes.fromhex(key)).decode()
        else:
            msg = "aoc2023/encryptionkey not found in keyring"
            raise Exception(msg)  # noqa: TRY002

    else:
        content = ""

    return [line_parser(line) for line in content.split("\n")]


def sha256(input_string: str) -> str:
    # Convert the input string to bytes
    if isinstance(input_string, float | int):
        input_string = str(input_string)
    input_bytes = input_string.encode("utf-8")
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    # Update the hash object with the input bytes
    sha256_hash.update(input_bytes)
    # Get the hexadecimal digest
    return sha256_hash.hexdigest()


def encrypted_content(input_path: Path, key: bytes) -> bytes:
    assert input_path.exists()  # noqa: S101

    input_bytes = input_path.open().read().encode()

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Pad the input bytes to a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()  # type: ignore  # noqa: PGH003
    padded_input_bytes = padder.update(input_bytes) + padder.finalize()

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded input bytes
    encrypted_bytes = encryptor.update(padded_input_bytes) + encryptor.finalize()

    # Return the IV and encrypted bytes
    return iv + encrypted_bytes


def decrypted_content(input_path: Path, key: bytes) -> bytes:
    assert input_path.exists()  # noqa: S101

    encrypted_bytes = input_path.open("rb").read()

    # Extract the IV from the first 16 bytes of the encrypted data
    iv = encrypted_bytes[:16]

    # The remaining bytes are the actual ciphertext
    ciphertext = encrypted_bytes[16:]

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()  # type: ignore  # noqa: PGH003
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()


def store_aoc_secret(service_name: str, secret_name: str, secret: str) -> None:
    # Store the secret in the keychain
    keyring.set_password(service_name, secret_name, secret)


def get_aoc_secret(service_name: str, secret_name: str) -> str | None:
    # Retrieve the secret from the keychain
    return keyring.get_password(service_name, secret_name)
