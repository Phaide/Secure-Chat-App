# -*- coding: UTF8 -*-


class Structures:

    request_standard_structure = {
        "status": str,
        "data": dict,
        "timestamp": int
    }

    node_structure = {
        "rsa_n": int,
        "rsa_e": int,
        "hash": str,
        "sig": str
    }

    contact_structure = {
        "address": str,
        "last_seen": int
    }

    received_message_structure = {
        "content": str,
        "meta": {
            "time_sent": int,
            "digest": str,
            "aes": str
        }
    }

    raw_stored_message_structure = {
        "content": str,
        "meta": {
            "time_sent": int,
            "time_received": int,
            "digest": str,
            "aes": str},
        "author": node_structure
    }

    prepared_message_structure = {
        "content": str,
        "meta": {
            "time_sent": int,
            "time_received": int,
            "digest": str,
            "aes": str,
            "id": int},
        "author": node_structure
    }
