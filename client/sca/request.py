# -*- coding: UTF8 -*-

from dataclasses import dataclass

from .encryption import Encryption
from .structures import Structures
from .utils import Utils


@dataclass
class Request:
    status: str
    data: dict
    timestamp: int = None

    @staticmethod
    def is_request_valid(req_data: dict) -> bool:
        """
        Takes a request information (as a dictionary) and checks wether it is valid.

        :param req_data:
        :return bool: True if the request is valid, False otherwise.
        """
        if not Utils.validate_fields(req_data, Structures.request_standard_structure):
            return False
        return True

    @classmethod
    def from_dict(cls, req_data: dict):
        """
        Returns a new object instance from the passed data.

        :param dict req_data: A valid request as a dictionary.
        :return: A Request object.
        """
        status = req_data["status"]
        data = req_data["data"]
        timestamp = req_data["status"]
        return cls(status, data, timestamp)

    @classmethod
    def from_json(cls, json_data: str):
        """
        Returns a new object instance from the passed data.

        !!! DEPRECATED !!!

        :param str json_data:
        :return: A Request object.
        """
        req_data = Utils.decode_json(json_data)
        return cls.from_dict(req_data)

    def set_timestamp(self):
        """
        Sets instance attribute "timestamp".
        """
        self.timestamp = Utils.get_timestamp()

    def to_dict(self) -> dict:
        """
        Returns the Request as a dictionary.
        """
        pass

    def to_json(self) -> str:
        """
        Returns the Request as a json-encoded string.
        """
        return Utils.encode_json(self.to_dict())

    def get_id(self) -> str:
        """
        This method derives an ID from this request.

        :return str: An hexadecimal identifier.
        """
        h = Encryption.hash_iterable(self.to_json())
        return h.hexdigest()
