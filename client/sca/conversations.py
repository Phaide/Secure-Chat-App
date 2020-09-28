# -*- coding: UTF8 -*-

from .encryption import Encryption
from .database import Database
from .message import Message
from .config import Config


class Conversations:

    def __init__(self, repo: str = "db/", pre: str = "", db_name: str = "conversations.db"):
        """
        Initiate the Conversation object, as well as its database.

        :param str repo: Repository under which we will store the database. eg: "db/" (relative) | "/db/" (absolute)
        :param str pre: Prefix for the conversation database name. Usually, the node ID.
        :param str db_name: The database name. Gets appended to "pre".
        """
        self.db = ConversationsDatabase(repo + pre + db_name)

    # Conversations section

    def does_conversation_exist_with_node(self, node_id: str) -> bool:
        return self.db.key_exists(self.db.keys_table, node_id)

    def get_all_conversations(self) -> list:
        """
        Gets from the database a list of all the ids of the nodes with whom a conversation has been established.

        :return list: List of node identifiers.
        """
        return list(self.db.query_column(self.db.conversation_table).keys())

    def get_all_messages_of_conversation(self, rsa_private_key, conversation_id: str) -> list:
        """
        Returns all messages of a conversation, all decrypted.

        :param rsa_private_key: A RSA private key, used to decrypt messages.
        :param str conversation_id: A node ID
        :return list: A list of all the messages (as Message objects) in the conversation, from oldest to latest.
        """
        aes_key, nonce = self.get_aes(rsa_private_key, conversation_id)
        messages = []
        # Messages are stored from the oldest to the latest, and we gather them in this order.
        for msg in self.db.query(self.db.conversation_table, conversation_id):
            # Creates a new AES object during every iteration.
            # We do this because the AES cipher depends on the last message(s) encrypted.
            # Therefore, there is a relationship between every message (if we use the same object).
            aes = Encryption.construct_aes_object(aes_key, nonce)
            decrypted_message = Encryption.decrypt_symmetric(aes, msg["content"], msg["metadata"]["digest"])
            message_object = Message(Encryption.decode_bytes(decrypted_message),
                                     msg["metadata"]["message_sent"],
                                     msg["metadata"]["message_received"])
            messages.append(message_object)
        return messages

    def get_last_conversation_message(self, rsa_private_key, conversation_id: str) -> dict:
        """
        Gets the last message of a conversation.

        :param rsa_private_key: A RSA private key, used to decrypt the message.
        :param str conversation_id: A node ID.
        :return dict: A message, as a dict.
        """
        raise NotImplemented

    # Keys section

    def get_aes(self, rsa_private_key, node_id: str) -> tuple or None:
        """
        This function returns an AES cipher (aes_key and nonce).
        If the key does exist in the database, reads its values and returns it.
        If it does not exist, return None.

        :param rsa_private_key: RSA private key object.
        :param str node_id: A node ID.
        :return tuple|None: 2-tuple: (bytes: the AES key, bytes: the nonce) or None if the key doesn't exist.
        """
        if self.db.key_exists(self.db.keys_table, node_id):
            # Get values from the database.
            key = self.db.query(self.db.keys_table, node_id)
            # Decrypts and deserialize the key
            key = Encryption.decrypt_asymmetric(rsa_private_key, key)
            # Unpack the values from the key
            aes_key = key[:Config.aes_keys_length]
            nonce = key[Config.aes_keys_length:]
        else:
            return
        return aes_key, nonce

    def store_aes(self, node_id: str, rsa_public_key, aes_key: bytes, nonce: bytes) -> None:
        """
        This function takes a new AES and either updates or creates it in the database.

        :param str node_id: A node ID
        :param rsa_public_key: A RSA public key
        :param bytes aes_key: A raw AES key
        :param bytes nonce: A nonce.
        """
        key = aes_key + nonce  # Results in a 48 bytes "key"
        key = Encryption.encrypt_asymmetric(rsa_public_key, key)
        if self.db.key_exists(self.db.keys_table, node_id):
            self.db.modify_aes(node_id, key)
        else:
            self.db.store_new_aes(node_id, key)


class ConversationsDatabase(Database):

    """

    This database holds information about conversations with known nodes.
    This includes: aes key and nonce, messages (content, timestamps, hash, sig, etc)

    Database structure:

    self.db = dict{
        conversations: dict{
            node_identifier: dict{
                message_identifier: dict{
                    ...message_structure...
                }
            }
        },
        keys: dict{
            node_identifier: key  # Value containing the AES key and the nonce, encrypted and serialized]
        }
    }

    """

    def __init__(self, db_name: str):
        self.conversation_table = "conversations"
        self.keys_table = "keys"
        super().__init__(db_name, {self.conversation_table: dict, self.keys_table: dict})

    def modify_aes(self, node_id: str, key: str):
        """
        Modifies an existing AES key.
        Does not care if it exists or not. This verification must be done beforehand.

        :param str node_id: A node ID.
        :param str key: A value containing the AES key and the nonce, encrypted and serialised for storage.
        :return:
        """
        self.update("keys", node_id, key)

    def store_new_aes(self, node_id: str, key: str) -> None:
        """
        Stores a new aes key.
        Does not care if it already exists ; this verification must be done beforehand.

        :param bytes node_id: A node ID.
        :param str key: A value containing the AES key and the nonce, encrypted and serialised for storage.
        """
        self.insert_dict("keys", {node_id: key})
