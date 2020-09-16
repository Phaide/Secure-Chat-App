# -*- coding: UTF8 -*-

import ipaddress
import datetime
import time
import json


class Utils:

    @staticmethod
    def encode_json(dictionary: dict) -> str:
        """
        Takes a dictionary and returns a JSON-encoded string.

        :param dict dictionary: A dictionary.
        :return str: A JSON-encoded string.
        """
        return json.JSONEncoder().encode(dictionary)

    @staticmethod
    def decode_json(json_string: str) -> dict:
        """
        Takes a message as a JSON string and unpacks it to get a dictionary.

        :param str json_string: A message, as a JSON string.
        :return dict: An unverified dictionary. Do not trust this data.
        """
        return json.JSONDecoder().decode(json_string)

    @staticmethod
    def get_timestamp() -> int:
        """
        Returns the actual time as a POSIX seconds timestamp.

        :return int: A timestamp, as POSIX seconds.
        """
        return int(time.time())

    @staticmethod
    def get_date_from_timestamp(timestamp: int) -> str:
        """
        Returns a readable date from the timestamp.

        :param int timestamp: A timestamp, as POSIX seconds.
        :return str: A readable date.
        """
        return datetime.datetime.utcfromtimestamp(timestamp).strftime("%X %x")

    @staticmethod
    def validate_fields(dictionary: dict, arch: dict) -> bool:
        """
        Takes a dictionary and an architecture and checks if the types and structure are valid.

        Example arch: {"content": str, "meta": {"time_sent": int, "digest": str, "aes": str}}

        :param dict dictionary: A dictionary to check.
        :param dict arch: Dictionary containing the levels of architecture.
        :return bool: True if the fields are valid, False otherwise.
        """
        if len(dictionary) != len(arch):
            return False
        for field_name, field_value in arch.items():
            if type(field_value) is not type:
                if type(dictionary[field_name]) is not type(field_value):
                    return False
                if not Utils.validate_fields(arch[field_name], field_value):
                    return False
            else:
                try:
                    if type(field_value) == int:
                        if not Utils.is_int(dictionary[field_name]):
                            return False
                    elif type(dictionary[field_name]) is not field_value:
                        return False
                except KeyError:
                    return False
        return True

    @staticmethod
    def is_int(value) -> bool:
        """
        Tests a value to check if it is an integer or not.
        "value" can be of any type, as long as it can be converted to int.
        """
        try:
            int(value)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def is_ip_address_valid(ip_address: str) -> bool:
        """
        Tests if the IP address is valid.

        :param str ip_address: An IP address.
        :return bool: True if it is, False otherwise.
        """
        # Tries to convert the first part to an IP address.
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            # If it doesn't work, tries to check if it can be a DNS name.
            # First, check if there are any special characters except dots and hyphens.
            from string import punctuation
            invalid_chars = set(punctuation.replace(".", "").replace("-", ""))
            if any(c in invalid_chars for c in ip_address):
                return False  # Is not a valid DNS Name nor a valid IP address.

        return True

    @staticmethod
    def is_network_port_valid(port: str) -> bool:
        """
        Tests if the port is valid.

        :param str port: An network port.
        :return bool: True if it is, False otherwise.
        """
        try:
            port = int(port)
        except ValueError:
            return False

        if int(port) not in range(0, 65536):
            return False  # The port is not in the acceptable range.

        return True
