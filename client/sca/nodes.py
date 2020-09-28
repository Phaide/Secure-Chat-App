# -*- coding: UTF8 -*-

from .database import Database
from .node import Node


class Nodes:

    def __init__(self, db_name: str = "db/nodes.db"):
        self.db = NodesDatabase(db_name)

    def add_node(self, node: Node) -> None:
        """
        Stores a node information in the database if it does not exist already.

        :param Node node: A node object, the one to store.
        """
        node_id = node.get_id()
        if not self.db.key_exists(self.db.nodes_table, node_id):
            self.db.insert_dict(self.db.nodes_table, {node_id: node.to_dict()})

    def get_all_node_ids(self) -> list:
        pass

    def get_node_info(self, node_id: str) -> dict:
        pass

    def node_exists(self, node_id: str) -> bool:
        pass


class NodesDatabase(Database):

    """

    This database holds information about the known nodes.

    Database structure:

    self.db = dict{
        nodes: dict{
            node_identifier: dict{
                "rsa_n": 123456789,
                "rsa_e": 123456,
                "hash": "hexdigest",
                "sig": "signature"
            }
        }
    }

    """

    def __init__(self, db_name: str):
        self.nodes_table = "nodes"
        super().__init__(db_name, {self.nodes_table: dict})
