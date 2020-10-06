# -*- coding: UTF8 -*-

import threading

from .conversations import Conversations
from .encryption import Encryption
from .controller import Controller
from .structures import Structures
from .contacts import Contacts
from .database import Database
from .message import Message
from .network import Network
from .node import MasterNode
from .lib import dictionary
from .config import Config
from .node import Node


class Main:
    def __init__(self):
        self.master_node = MasterNode()
        self.network = Network(self.master_node, "192.168.0.48", 62489)  # !!! DEV ONLY !!!
        self.controller = Controller(self.master_node, self.network)

        self.start_server()
        self.controller.app.MainLoop()

    def start_server(self) -> None:
        """
        Instantiate server as a new thread.
        """
        t_net = threading.Thread(target=self.network.listen_for_message, name="net_thread", daemon=True)
        t_net.start()

        self.controller.mainFrame.serverStatus_staticText.SetForegroundColour(wx.Colour(0, 255, 0))
        self.controller.mainFrame.serverStatus_staticText.SetLabel("Up")
