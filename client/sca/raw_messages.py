# -*- coding: UTF8 -*-

from .encryption import Encryption
from .database import Database
from .message import Message
from .config import Config
from .node import Node


class RawMessages:

    def __init__(self, repo: str = "db/", pre: str = "", db_name: str = "conversations.db"):
        """
        Initiate the Conversation object, as well as its database.

        :param str repo: Repository under which we will store the database. eg: "db/" (relative) | "/db/" (absolute)
        :param str pre: Prefix for the conversation database name. Usually, the node ID.
        :param str db_name: The database name. Gets appended to "pre".
        """
        self.db = RawMessagesDatabase(repo + pre + db_name)

    def add_new_raw_message(self, message: Message, node: Node):
        """
        Adds a new message to the database.

        :param Message message: A Message object.
        :param Node node: A Node object.
        """
        if self.db.key_exists(self.db.messages_table, message.get_id()):
            # In this case, the message is either a duplicate (we already received it)
            # or there was a collision (very unlikely).
            return
        if not Message.is_message_valid_for_raw_storage(message.as_dictionary()):
            return

        self.db.add_new_raw_message(message.as_dictionary())

    def get_all_raw_messages(self) -> list:
        return self.db.query_column(self.db.messages_table)

    def get_raw_message(self, message_id: str) -> dict:
        if self.db.key_exists(self.db.messages_table, message_id):
            return self.db.query(self.db.messages_table, message_id)
        return {}


class RawMessagesDatabase(Database):

    """

    This database holds information on every message received.

    Database structure:

    self.db = dict{
        messages: dict{
            message_id: {
                "content": encrypted_message,
                "meta": {
                    "date_sent": timestamp,  # Timestamp in POSIX seconds.
                    "date_received": timestamp,
                    "digest": digest,  # Digest of the encrypted message.
                    "aes": key,  # 48 bytes key containing both the AES key and the nonce.
                },
                "author": ...node architecture...
            }
        }
    }

    """

    def __init__(self, db_name: str):
        self.messages_table = "messages"
        super().__init__(db_name, {self.messages_table: dict})

    def add_new_raw_message(self, raw_message: dict) -> None:
        self.db.insert_dict(self.messages_table, raw_message)
