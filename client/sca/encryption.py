# -*- coding: UTF8 -*-

import base64
import os

from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

from .config import Config
from .node import Node


class Encryption:

    # RSA section

    @staticmethod
    def create_rsa_pair(bits: int = Config.rsa_keys_length) -> RSA.RsaKey:
        """
        Creates a new RSA key pair.

        :param int bits: Length of the keys in bits.
        :return RSA.RsaKey: A RSA private key
        """
        return RSA.generate(bits)

    @staticmethod
    def is_key_private(rsa_key: RSA.RsaKey) -> bool:
        return rsa_key.has_private()

    @staticmethod
    def get_public_key_from_private_key(private_key: RSA.RsaKey) -> RSA.RsaKey:
        """
        Takes a RSA private keys and returns a corresponding RSA public key.

        :param RSA.RsaKey private_key: A RSA private key.
        :return RSA.RsaKey: A matching RSA public key.
        """
        if not Encryption.is_key_private(private_key):
            raise ValueError("Passed RSA key is not private.")
        return private_key.publickey()

    @staticmethod
    def construct_rsa_object(n, e, d=None, p=None, q=None) -> RSA.RsaKey:
        """
        Construct and returns a RSA key.
        If you want a public key, pass n and e.
        If you want a private key, also pass d, p and q.

        :param n: Modulus.
        :param e: Public exponent.
        :param p: First factor.
        :param q: Second factor.
        :param d: Private exponent.
        :return RSA.RsaKey: A RSA key, public or private depending on the arguments passed.
        """
        # If d, p and q are set
        if d and p and q:
            # Construct and return a private key
            return RSA.construct((int(n), int(e), int(d), int(p), int(q)), True)
        # Construct and return a public key.
        return RSA.construct((int(n), int(e)), True)

    @staticmethod
    def import_rsa_private_key_from_file(file_location: str, passphrase: str or None = None):
        """
        Opens a file and reads its content to get

        :param str file_location: Path to the file.
        :param str passphrase: The passphrase used to read the key.
        :return: None or a RSA private key.
        """
        with open(file_location, "rb") as k:
            try:
                rsa_private_key = RSA.import_key(k.read(), passphrase=passphrase)
            except (ValueError, IndexError, TypeError):
                return

        if not Encryption.is_key_private(rsa_private_key):
            return

        return rsa_private_key

    @staticmethod
    def export_rsa_private_key_to_file(rsa_private_key: RSA.RsaKey, location: str, passphrase: str or None = None):
        """
        :param RSA.RsaKey rsa_private_key: A RSA private key.
        :param str location: Directory to which the private key should be exported to.
        :param str|None passphrase: A passphrase to encrypt the private key. Will be needed when importing it.
        """
        identifier = Node.get_id_from_rsa_key(rsa_private_key)
        file_name = f"rsa_public_key-{identifier}.pem"
        path = os.path.join(location, file_name)
        with open(path, "wb") as fl:  # Might raise OSError, PermissionError, UnicodeError
            fl.write(Encryption.get_public_key_from_private_key(rsa_private_key).export_key(passphrase=passphrase))

    @staticmethod
    def export_rsa_public_key_to_file(rsa_private_key: RSA.RsaKey, location: str) -> None:
        """
        :param RSA.RsaKey rsa_private_key: A RSA private key.
        :param str location: Directory to which the public key should be exported to.
        """
        identifier = Node.get_id_from_rsa_key(rsa_private_key)
        file_name = f"rsa_public_key-{identifier}.pem"
        path = os.path.join(location, file_name)
        with open(path, "wb") as fl:  # Might raise OSError, PermissionError, UnicodeError
            fl.write(Encryption.get_public_key_from_private_key(rsa_private_key).export_key())

    @staticmethod
    def is_rsa_private_key_valid(rsa_private_key: RSA.RsaKey) -> bool:
        """
        Tests the RSA key to check if it is valid, according to our configuration.

        :param RSA.RsaKey rsa_private_key:
        :return bool: True if it is, False otherwise.
        """
        if not Encryption.is_key_private(rsa_private_key):
            return False
        if not rsa_private_key.size_in_bits() != Config.rsa_keys_length:
            return False
        return True

    @staticmethod
    def encrypt_asymmetric_raw(rsa_public: RSA.RsaKey, data: bytes) -> bytes:
        """
        Encrypts data using RSA.
        Must be reversible with Encryption.decrypt_asymmetric_raw().

        :param RSA.RsaKey rsa_public: A RSA public key.
        :param bytes data: Data, as bytes.
        :return bytes: The encrypted data as bytes.
        """
        return PKCS1_OAEP.new(rsa_public).encrypt(data)

    @staticmethod
    def decrypt_asymmetric_raw(rsa_private: RSA.RsaKey, en_data: bytes) -> bytes:
        """
        Decrypts data using RSA.
        Must be reversible with Encryption.encrypt_asymmetric_raw().

        :param RSA.RsaKey rsa_private: A RSA private key.
        :param bytes en_data: Encrypted data, as bytes.
        :return bytes: The decrypted data as bytes.

        :raises: ValueError or KeyError: When the decryption fails.
        """
        return PKCS1_OAEP.new(rsa_private).decrypt(en_data)

    @staticmethod
    def encrypt_asymmetric(rsa_public: RSA.RsaKey, data: bytes) -> str:
        """
        Encrypts and serializes data.
        Must be reversible with Encryption.decrypt_asymmetric().

        :param RSA.RsaKey rsa_public: A RSA public key.
        :param bytes data: The data to encrypt.
        :return string: The encrypted and serialized data.
        """
        en_data = Encryption.encrypt_asymmetric_raw(rsa_public, data)
        se_en_data = Encryption.serialize_bytes(en_data)
        return se_en_data

    @staticmethod
    def decrypt_asymmetric(rsa_private: RSA.RsaKey, se_en_data: str) -> bytes:
        """
        Deserialized and decrypts data.
        Must be reversible with Encryption.encrypt_asymmetric().

        :param RSA.RsaKey rsa_private: A RSA private key.
        :param str se_en_data: Encrypted and serialized data.
        :return bytes: The decrypted and deserialized data.
        """
        en_data = Encryption.deserialize_string(se_en_data)
        data = Encryption.decrypt_asymmetric_raw(rsa_private, en_data)
        return data

    @staticmethod
    def get_rsa_signature(rsa_private: RSA.RsaKey, hash_object) -> bytes:
        """
        Get a signature of a hash object.

        :param RSA.RsaKey rsa_private:
        :param hash_object:
        :return bytes: A signature, as bytes.
        """
        return pkcs1_15.new(rsa_private).sign(hash_object)

    @staticmethod
    def is_signature_valid(rsa_public: RSA.RsaKey, hash_object: SHA256.SHA256Hash, sig: bytes) -> bool:
        """
        Takes a MAC tag and verifies it is valid.

        :param RSA.RsaKey rsa_public: A RSA public key.
        :param SHA256.SHA256Hash hash_object: The hash object.
        :param bytes sig: A signature of the above hash.
        :return: True if it can be trusted, False otherwise.
        """
        try:
            pkcs1_15.new(rsa_public).verify(hash_object, sig)
        except (ValueError, TypeError):
            return False
        else:
            return True

    @staticmethod
    def get_max_rsa_enc_msg_length(sha: int = 256) -> int:
        """
        Returns the maximum length a message can have when doing RSA encryption.

        :param int sha: Number of bits in the SHA algorithm used. Default is 256.
        :return int: Corresponds to the max length a message can have to be encrypted with RSA.
        """
        # Gets the keys length in bytes.
        keys_length = Config.rsa_keys_length / 8
        sha_length = sha / 8

        return int(keys_length - (2 + sha_length * 2))

    # Hashing section

    @staticmethod
    def hash_iterable(iterable) -> SHA256.SHA256Hash:
        """
        Returns a hash object of the iterable passed.
        Note that every item in the iterable should have a __str__ method, except if it's of bytes type.

        :param iterable: An iterable of any type, or a bytes object.
        :return SHA256.SHA256Hash: A hash object.
        """
        if type(iterable) == bytes:
            b = iterable
        else:
            b = "".join(str(i) for i in iterable).encode("utf-8")
        hash_object = SHA256.new(b)
        return hash_object

    # Serialisation section

    @staticmethod
    def serialize_bytes(b: bytes) -> str:
        """
        Takes a bytes object and serialize it.
        Must be reversible with Encryption.deserialize_string().

        :param bytes b: Data, as bytes.
        :return str: A serialized string of the passed data.
        """
        return base64.b64encode(b).decode("utf-8")

    @staticmethod
    def deserialize_string(s: str) -> bytes:
        """
        Takes a string and deserialize it.
        Must be reversible with Encryption.serialize_bytes().

        :param str s: Data, as a string.
        :return bytes: The deserialized string of the passed data.
        """
        return base64.b64decode(s)

    @staticmethod
    def encode_string(data: str) -> bytes:
        """
        Takes a string and return a bytes encoded version of the data.
        Must be reversible with Encryption.decode_bytes().

        :param str data: Data, as a string.
        :return bytes: The encoded data.
        """
        return data.encode("utf-8")

    @staticmethod
    def decode_bytes(data: bytes) -> str:
        """
        Takes a bytes object and return a decoded version of the data.
        Must be reversible with Encryption.encode_string().

        :param bytes data: Data, as bytes.
        :return str: The decoded data.
        """
        return data.decode("utf-8")

    # AES section

    @staticmethod
    def create_aes(length: int = Config.aes_keys_length, mode: int = Config.aes_mode) -> tuple:
        """
        Creates a new AES key.

        :param int length: Length of the keys (in bytes).
        :param int mode: The AES mode.
        :return: A 2-tuple: (bytes: aes_key, bytes: nonce).
        """
        aes_key = get_random_bytes(length)
        aes = AES.new(key=aes_key, mode=mode)
        nonce = aes.nonce
        return aes_key, nonce

    @staticmethod
    def construct_aes_object(aes_key: bytes, nonce: bytes, mode: int = Config.aes_mode):
        """
        Constructs a new AES cipher.
        Note that AES objects are stateful, meaning that one instance can only encrypt or decrypt.

        :param bytes aes_key: The AES key.
        :param bytes nonce: The nonce.
        :param int mode: The AES mode.
        :return: The AES cipher.
        """
        return AES.new(key=aes_key, nonce=nonce, mode=mode)

    @staticmethod
    def encrypt_symmetric_raw(aes_key, data: bytes) -> tuple:
        """
        Encrypts data using AES.
        Must be reversible with Encryption.decrypt_symmetric_raw().

        :param aes_key: An AES key.
        :param bytes data: Data, as bytes.
        :return tuple: The encrypted data and the corresponding tag, both as bytes.
        """
        en_data, tag = aes_key.encrypt_and_digest(data)
        return en_data, tag

    @staticmethod
    def decrypt_symmetric_raw(aes_key, en_data: bytes, tag: bytes) -> bytes:
        """
        Decrypts data using AES.
        Must be reversible with Encryption.encrypt_symmetric_raw().

        :param aes_key: An AES key.
        :param bytes en_data: Encrypted data, as bytes.
        :param bytes tag: Tag, as bytes.
        :return bytes: The decrypted data as bytes.

        :raises: ValueError or KeyError: When the decryption fails.
        :raises: ValueError or KeyError: When the tag is incorrect.
        """
        data = aes_key.decrypt_and_verify(en_data, tag)
        return data

    @staticmethod
    def encrypt_symmetric(aes_key, data: bytes) -> tuple:
        """
        Encrypts and serializes data.
        Must be reversible with Encryption.decrypt_symmetric().

        :param aes_key: An AES key.
        :param bytes data: The data to encrypt and serialize.
        :return tuple: The encrypted and serialized data and the corresponding tag (both strings).
        """
        en_data, tag = Encryption.encrypt_symmetric_raw(aes_key, data)
        se_en_data = Encryption.serialize_bytes(en_data)
        se_tag = Encryption.serialize_bytes(tag)
        return se_en_data, se_tag

    @staticmethod
    def decrypt_symmetric(aes_key, se_en_data: str, se_tag: str) -> bytes:
        """
        Deserialized and decrypts data.
        Must be reversible with Encryption.encrypt_symmetric().

        :param aes_key: An AES key.
        :param str se_en_data: Encrypted and serialized data.
        :param str se_tag: Serialized tag.
        :return bytes: The decrypted and deserialized data.
        """
        en_data = Encryption.deserialize_string(se_en_data)
        tag = Encryption.deserialize_string(se_tag)
        data = Encryption.decrypt_symmetric_raw(aes_key, en_data, tag)
        return data
