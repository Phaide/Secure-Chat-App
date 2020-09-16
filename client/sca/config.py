# -*- coding: UTF8 -*-

import socket
import re

from urllib.request import urlopen

from Crypto.Cipher import AES


class Config:
    message_fields: tuple = ("author", "ciphertext", "sent")

    # The maximum number of contacts we should know of.
    max_contacts = 50

    # List of Beacons.
    # An entry must be made of an address (IP or DNS) and a port, separated by a colon (:).
    # Example : ["192.168.0.100:12345"]
    servers: list = []

    @staticmethod
    def get_local_ip_address() -> str:
        host_name = socket.gethostname()
        local_ip_address = socket.gethostbyname(host_name)
        return local_ip_address

    @staticmethod
    def get_global_ip_address() -> str:
        url = "http://checkip.dyndns.org"
        request = urlopen(url).read().decode("utf-8")
        global_ip = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", request)[0]
        return global_ip

    # ---------------------------------------------
    # ----- DO NOT MODIFY ANYTHING UNDER THIS -----
    # ---------------------------------------------

    # Length an hexadecimal ID should have. DO NOT modify unless you know what you are doing.
    id_len: int = 16

    # RSA keys length, in bits.
    rsa_keys_length: int = 4096

    # Length of the AES object in bytes. Therefore, multiply by 8 to get the AES protocol used.
    # e.g. 32 * 8 = 256 ; we use AES256.
    aes_keys_length: int = 32

    # AES mode. Default is EAX.
    aes_mode: int = AES.MODE_EAX

    # Network buffer.
    network_buff_size = 4096

    # Maximum connections at once.
    network_max_conn = 5
