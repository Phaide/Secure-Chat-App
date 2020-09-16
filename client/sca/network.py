# -*- coding: UTF8 -*-

import socket
import wx

from .encryption import Encryption
from .structures import Structures
from .message import OwnMessage
from .message import Message
from .config import Config
from .utils import Utils
from .node import Node


class Network:

    api_endpoint_suffix = "/nodes"

    def __init__(self, master_node, host: str, port: int):
        self.master_node = master_node
        self.host = host
        self.port = port

    def __del__(self):
        self.master_node.display.mainFrame.serverStatus_staticText.SetForegroundColour(wx.Colour(255, 0, 0))
        self.master_node.display.mainFrame.serverStatus_staticText.SetLabel("Down")

    # Validation section

    @staticmethod
    def is_request_valid(request: dict) -> bool:
        """
        Takes a request as a JSON-encoded request and checks it is valid.
        Valid does not mean trustworthy.

        :param str request: A JSON-encoded dictionary.
        """
        if not Utils.validate_fields(request, Structures.request_standard_structure):
            return False

        return True

    def listen_for_message(self) -> None:
        """
        Setup a server and listen on a port
        """

        def receive_all(sock: socket.socket) -> bytes:
            """
            Receives all parts of a network-sent message

            :param socket.socket sock:
            :return bytes:
            """
            data = bytes()
            while True:
                part = sock.recv(Config.network_buff_size)
                data += part
                if len(part) < Config.network_buff_size:
                    # Either 0 or end of data
                    break
            return data

        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(Config.network_max_conn)

        while True:
            connection, address = server_socket.accept()
            print(address)
            print(receive_all(connection))

    @staticmethod
    def read_message(msg: str, node: str) -> None or Message:
        """
        Tries to read a message received by a peer, to only check if it is correct (not decrypting it here).

        A raw received message looks like this:

        {
            "content": encrypted_message,
            "meta": {
                "time_sent": timestamp,
                "digest": digest,
                "aes": key
            }
        }

        :param str msg: A message, as a JSON string.
        :param str node: A node, as a JSON string.
        :return None|Message: None if the message is invalid, otherwise returns the message object.
        """
        if not Node.is_valid(Utils.decode_json(node)):
            return

        # Converts the JSON string to a dictionary.
        unpacked_msg = Utils.decode_json(msg)

        if Message.is_received_message_valid(unpacked_msg):
            message_object = Message.from_dict(unpacked_msg)
            message_object.set_time_received()
            message_object.set_id()
        else:
            return

        # At this point, the message is valid and we can relay it to other nodes without danger.
        return message_object

    def broadcast_message(self, message: Message) -> None:
        """
        Broadcast a message to all known contacts.

        :param Message message: Message object
        """
        known_nodes = {}

        for node_id in self.master_node.contacts.list_peers():
            known_nodes.update({node_id: self.master_node.contacts.get_node_info(node_id)})

        for node in known_nodes:
            self.send_network_message(node, message)

    def relay_message(self, message: Message) -> None:
        """
        Relays a message to all known nodes.
        Note: this function must only be used when sending other nodes' messages.

        :param Message message: A message object.
        """
        self.broadcast_message(message)

    def send_message(self, message: Message) -> None:
        """
        Prepare a message for network broadcast.
        Note: this function must only be used when sending own messages.

        :param Message message: A message object.
        """
        message.set_time_sent()
        message.prepare()  # Must be reworked after conversations and aes refactor
        self.broadcast_message(message)

    def send_network_message(self, contact: dict, message: Message) -> None:
        """
        Send a message to a contact.

        :param dict contact: A dictionary containing the information of a contact.
        :param Message message:
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Initiate network connection with the contact.
        # TODO : error handling
        address, port = contact["address"].split(":")
        client_socket.connect((address, port))  # Convert node.port to str ? !!! DEV ONLY !!!
        client_socket.send(Encryption.encode_string(message.to_json()))

    def prepare_message_for_recipient(self, node: Node, message: OwnMessage):
        """
        Prepare a message by encrypting its values.
        This message is addresses to a specific node.
        """
        aes_key, nonce = self.master_node.conversations.get_aes(node.get_id())
        aes = Encryption.construct_aes_object(aes_key, nonce)
        message.prepare(aes)
