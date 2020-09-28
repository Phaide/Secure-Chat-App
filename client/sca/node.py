# -*- coding: UTF8 -*-

import random

from .conversations import Conversations
from .encryption import Encryption
from .structures import Structures
from .contacts import Contacts
from .lib import dictionary
from .config import Config
from .utils import Utils


class Node:

    def __init__(self):
        # Initialize attributes.
        self.rsa_public_key = None
        self.hash = None
        self.sig = None

        self.aes = None

        self.name = None
        self.id = None

    @staticmethod
    def is_valid(node_data: dict) -> bool:
        """
        Validates all the fields of a node.

        :param dict node_data: The dict containing the information to validate.
        :return bool: True if the node information is correct, False otherwise.
        """

        if not Utils.validate_fields(node_data, Structures.node_structure):
            return False

        # Verify the RSA pubkey
        try:
            node_pubkey = Encryption.construct_rsa_object(node_data['rsa_n'], node_data['rsa_e'])
        except ValueError:
            return False  # Invalid modulus and/or exponent -> invalid RSA key.

        # Verify that the pubkey RSA modulus length is corresponding to the expected key length.
        # Note : with L being the key length in bits, 2**(L-1) <= N < 2**L
        if node_pubkey.size_in_bits() != Config.rsa_keys_length:
            return False  # RSA keys are not the correct size.

        # Create a hash of the node's information.
        hash_object = Node.get_node_hash(node_pubkey)

        # Verify hash
        if hash_object.hexdigest() != node_data['hash']:
            return False  # Hash is incorrect.

        # Verify signature
        if not Encryption.is_signature_valid(node_pubkey, hash_object, Encryption.deserialize_string(node_data['sig'])):
            return False  # Signature is invalid

        return True

    @classmethod
    def from_dict(cls, node_data: dict):
        """
        Takes node information as a dictionary and returns a Node object.
        The dictionary must contain valid information. This check should be done beforehand.

        :param node_data: Node information as a dictionary. Must be valid.
        :return: A Node object.
        """
        new_node = cls()
        new_node.__initialize(node_data)
        return new_node

    def __initialize(self, node_data: dict) -> None:
        """
        Sets:
        - RSA public key
        - Instance's ID
        - Instance's name
        - Hash
        - Signature

        :param dict node_data: Node information as a dictionary. Must be valid.
        """
        self.set_rsa_public_key(Encryption.construct_rsa_object(int(node_data["rsa_n"]), int(node_data["rsa_e"])))
        self.set_hash(node_data["hash"])
        self.set_signature(node_data["sig"])

        self.set_id()
        self.set_name()

    # ID section

    def set_id(self) -> None:
        """
        Sets Node's ID.
        This ID is derived from the RSA key.
        """
        assert self.rsa_public_key is not None
        self.id = Node.get_id_from_rsa_key(self.rsa_public_key)

    def get_id(self) -> str or None:
        """
        Returns the Node's ID.

        :return str|None: The Node's ID if set, None otherwise.
        """
        return self.id

    @staticmethod
    def get_id_from_rsa_key(rsa_key) -> str:
        """
        Returns an ID based on a RSA key.

        :param rsa_key: A RSA key, private or public.
        :return str: An identifier.
        """
        hash_object = Encryption.hash_iterable([rsa_key.n, rsa_key.e])
        hex_digest = hash_object.hexdigest()
        return hex_digest[:Config.id_len]

    # Name section

    @staticmethod
    def get_name_from_node(identifier: str) -> str:
        """
        Derive a name from an hexadecimal value.

        :param str identifier: Hexadecimal identifier.
        :return str: A name.
        """
        # Sets the random number generator's seed.
        random.seed(int(identifier, 16))

        name_parts = []

        # First word, choose an adjective.
        adjectives = dictionary.dictionary["adjectives"]
        index = random.randrange(0, len(adjectives))
        adjective = adjectives[index]
        name_parts.append(adjective)

        # Second word, an animal name.
        animals = dictionary.dictionary["animals"]
        index = random.randrange(0, len(adjectives))
        animal = animals[index]
        name_parts.append(animal)

        for i, word in enumerate(name_parts):
            # Capitalize the first letter of the word
            name_parts[i] = word[0].upper() + word[1:]

        return "".join(name_parts)

    def get_name(self) -> str or None:
        """
        Returns Node's name.

        :return str|None: The Node's name if set, None otherwise.
        """
        return self.name

    def set_name(self) -> None:
        """
        Sets Node's name.
        """
        self.name = Node.get_name_from_node(self.id)

    # RSA section

    def set_rsa_public_key(self, rsa_public_key) -> None:
        """
        Sets the instance attribute "self.rsa_public_key".

        :param rsa_public_key: A RSA public key.
        """
        self.rsa_public_key = rsa_public_key

    def get_rsa_public_key(self) -> object:
        """
        Returns the Node's RSA public key.
        The instance must have a valid "rsa_public_key" attribute.

        :return object: A RSA public key object.
        """
        return Encryption.get_public_key_from_private_key(self.rsa_public_key)

    def get_signature(self) -> str:
        """
        Returns Node's signature.

        :return str: Node's signature.
        """
        return self.sig

    def set_signature(self, signature: str) -> None:
        """
        Sets Node's signature.
        """
        self.sig = signature

    def is_signature_valid(self, rsa_public_key, sig: bytes) -> bool:
        """
        Verifies a signature is valid.
        Refer to "Encryption.is_signature_valid()" for more information.

        :param rsa_public_key: A RSA public key.
        :param bytes sig: A signature, as bytes.
        """
        return Encryption.is_signature_valid(self.rsa_public_key, rsa_public_key, sig)

    # Hash section

    def set_hash(self, h: str) -> None:
        """
        Sets the Node's hash.
        """
        self.hash = h

    @staticmethod
    def get_node_hash(rsa_public_key):
        """
        Returns a hash of the public key's n and e.
        Please refer to "Encryption.hash_iterable()" for more information.

        :return: A hash object.
        """
        return Encryption.hash_iterable([rsa_public_key.n, rsa_public_key.e])

    def get_own_hash(self) -> str:
        """
        Returns a hash of the self.rsa_public_key's n and e.
        Please refer to "Encryption.hash_iterable()" for more information.

        :return str: The hash's hexdigest.
        """
        h = Node.get_node_hash(self.rsa_public_key)
        return h.hexdigest()

    # Export section

    def as_dictionary(self) -> dict:
        dic = {
            "rsa_n": self.rsa_public_key.n,
            "rsa_e": self.rsa_public_key.e,
            "hash": self.get_own_hash(),
            "sig": self.get_signature()
        }
        return dic

    def to_json(self) -> str:
        """
        Returns the Node's information as a JSON-encoded string.

        :return str: JSON string containing the information of the node.
        """
        return Utils.encode_json(self.as_dictionary())


class MasterNode(Node):

    def __init__(self):
        Node.__init__(self)
        self.rsa_private_key = None
        self.conversations = None
        self.contacts = None

    def open_databases(self) -> None:
        """
        Opens the databases objects and stores them as instance attributes.
        This function must only be called once self.id is set.
        """
        self.conversations = Conversations(pre=self.id + "_")
        self.contacts = Contacts()

    def get_messages(self, conversation_id: str) -> list:
        """
        Gathers all messages of a conversation from the database.

        :param str conversation_id:
        :return list:
        """
        return self.conversations.get_all_messages_of_conversation(self.rsa_private_key, conversation_id)

    def __initialize(self, rsa_private_key) -> None:
        """
        Sets:
        - RSA private key
        - RSA public key
        - Instance's ID
        - Instance's name
        - Databases instances

        :param rsa_private_key: A RSA private key.
        """
        self.set_rsa_private_key(rsa_private_key)
        self.set_rsa_public_key(Encryption.get_public_key_from_private_key(rsa_private_key))
        self.set_id()
        self.set_name()
        self.open_databases()

    # RSA section

    def set_rsa_private_key(self, rsa_private_key: object) -> None:
        """
        Sets attribute "self.rsa_private_key".

        :param object rsa_private_key: A RSA private key object.
        """
        self.rsa_private_key = rsa_private_key

    def sign_self(self) -> bytes:
        """
        Signs this node's information.

        :return bytes: A signature, as bytes.
        """
        return Encryption.get_rsa_signature(self.rsa_private_key, self.get_own_hash())

    # AES section

    def set_aes(self) -> None:
        """
        Sets the Node's AES values.
        """
        assert self.id is not None
        self.aes = self.conversations.get_aes(self.get_id())
