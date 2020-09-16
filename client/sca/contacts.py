# -*- coding: UTF8 -*-

from .database import Database
from .utils import Utils


class Contacts:

    structure = {"address": str, "last_seen": str}  # See ContactsDatabase's docstring.

    def __init__(self, db_name: str = "db/contacts.db"):
        self.db = ContactsDatabase(db_name)

    @staticmethod
    def check_contact_info(contact_info: dict) -> bool:
        """
        Performs basic checks on a contact to see if the information is correct.

        :param dict contact_info: A contact, as a dictionary.
        :return bool: True if is, False otherwise.
        """
        # Validate fields.

        if not Utils.validate_fields(contact_info, Contacts.structure):
            return False

        # Validate address and port.

        address = contact_info["address"].split(':')

        if len(address) != 2:
            return False

        ip_address, port = address

        if not Utils.is_ip_address_valid(ip_address):
            return False
        if not Utils.is_network_port_valid(port):
            return False

        # Validate last_seen.

        try:
            if int(contact_info["last_seen"]) not in range(0, Utils.get_timestamp() + 1):
                return False  # Node is from the future ! Ask him about WW3 !
        except ValueError:
            return False  # last_seen in not an integer, therefore not a valid timestamp.

        return True

    def add_contact(self, contact_info: dict) -> None:
        """
        Adds a new contact to the contacts database.
        The contact_info should be checked to be valid beforehand.

        :param dict contact_info: A dictionary containing a node's information.
        This information should be checked to be valid beforehand
        """
        node_id = contact_info["id"]
        if not self.db.column_exists(node_id):
            self.db.insert_new_column(node_id, dict)
        self.db.insert_dict(node_id, contact_info)

    def get_node_info(self, node_id: str) -> dict:
        """
        Tries to get the information of a contact.

        :param str node_id: A node ID.
        :return: A dictionary containing the node's information.
        """
        if self.node_exists(node_id):
            return self.db.query(self.db.contacts_table, node_id)
        else:
            return {}

    def node_exists(self, node_id: str) -> bool:
        """
        Checks if a contact exists in the database.

        :param str node_id: A node ID.
        :return: True if it does, False otherwise.
        """
        return self.db.key_exists(self.db.contacts_table, node_id)


class ContactsDatabase(Database):

    """

    This database holds information about the contacts of the client.
    This includes: address, port, last seen datetime.

    Database structure:

    self.db = dict{
        contacts: dict{
            contact_identifier: dict{
                "address": "address:port"  # An IP address and a port.
                "last_seen": "timestamp"  # Timestamp of the last time the node was seen.
            }
        }
    }

    """

    def __init__(self, db_name: str):
        self.contacts_table = "contacts"
        super().__init__(db_name, {self.contacts_table: dict})
