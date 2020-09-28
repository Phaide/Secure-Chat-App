# -*- coding: UTF8 -*-

from .database import Database
from .contact import Contact


class Contacts:

    def __init__(self, db_name: str = "db/contacts.db"):
        self.db = ContactsDatabase(db_name)

    def add_contact(self, contact: Contact) -> None:
        """
        Adds a new contact to the contacts database.

        :param Contact contact: A contact object.
        """
        contact_id = contact.get_id()
        if not self.db.key_exists(self.db.contacts_table, contact_id):
            self.db.insert_dict(self.db.contacts_table, {contact_id: contact.to_dict()})

    def get_all_contacts_ids(self) -> list:
        return list(self.db.query_column(self.db.contacts_table).keys())

    def get_contact_info(self, contact_id: str) -> dict:
        """
        Tries to get the information of a contact.

        :param str contact_id: A node ID.
        :return: A dictionary containing the node's information.
        """
        if self.contact_exists(contact_id):
            return self.db.query(self.db.contacts_table, contact_id)
        else:
            return {}

    def contact_exists(self, contact_id: str) -> bool:
        """
        Checks if a contact exists in the database.

        :param str contact_id: A node ID.
        :return: True if it does, False otherwise.
        """
        return self.db.key_exists(self.db.contacts_table, contact_id)


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
