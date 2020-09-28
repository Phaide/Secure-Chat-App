from dataclasses import dataclass

from .encryption import Encryption
from .structures import Structures
from .config import Config
from .utils import Utils


@dataclass
class Contact:
    address: str
    port: int
    last_seen: int  # A timestamp, as POSIX seconds.

    # Validation section

    @staticmethod
    def is_valid(contact_data: dict) -> bool:
        """
        Checks if the data passed is valid contact information.

        :param dict contact_data: A contact, as a dictionary.
        :return bool: True if is valid, False otherwise.
        """
        if not Utils.validate_fields(contact_data, Structures.simple_contact_structure):
            return False

        # Validate address and port.
        address = contact_data["address"].split(':')

        if len(address) != 2:
            return False

        ip_address, port = address

        if not Utils.is_ip_address_valid(ip_address):
            return False
        if not Utils.is_network_port_valid(port):
            return False

        # Validate last_seen.
        #try:
        #    if int(contact_data["last_seen"]) not in range(0, Utils.get_timestamp() + 1):
        #        return False  # Node is from the future ! Ask him about WW3 !
        #except ValueError:
        #    return False  # last_seen in not an integer, therefore not a valid timestamp.

        return True

    # Class methods section

    @classmethod
    def from_dict(cls, contact_data: dict, last_seen: int = None):
        address, port = contact_data["address"].split(":")
        if last_seen is None:
            try:
                last_seen = contact_data["last_seen"]
            except KeyError:
                last_seen = Utils.get_timestamp()
        return cls(address, port, last_seen)

    @classmethod
    def from_raw_address(cls, raw_address: str):
        address, port = raw_address.split(":")
        return cls(address, port, 0)  # 0 ??!!!

    # ID section

    def get_id(self) -> str:
        h = Encryption.hash_iterable(":".join([self.address, self.port]))
        return h.hexdigest()[:Config.id_len]

    # Last seen section

    def set_last_seen(self) -> None:
        self.last_seen = Utils.get_timestamp()

    def get_last_seen(self) -> int:
        return self.last_seen

    # Export section

    def to_dict(self) -> dict:
        return {
            "address": ":".join([self.address, self.port])
        }


class OwnContact:
    def __init__(self):
        self.address = Config.get_local_ip_address()
        self.port = Config.port

    def to_dict(self) -> dict:
        return {
            "address": ":".join([self.address, self.port])
        }
