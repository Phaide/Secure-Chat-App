# Import built-in modules
import socket
import json
import os
import base64
from hashlib import sha256

# Import non-built in modules
import threading
import requests
import wx
import wx.xrc
import rsa # Documentation : https://stuvel.eu/python-rsa-doc/

# Documentation : https://pycryptodome.readthedocs.io/en/latest/
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# Import the display file
import wxdisplay

"""

Naming conventions note :
o_ stands for object
t_ stands for thread

"""

class Display:

    def __init__(self, o_node):
        self.node = o_node
        self.app = wx.App()
        self.mainFrame = self.MainMenu_Wrapper(None, self.node)
        self.mainFrame.Show()

    """

    The following classes depend on their respective equivalent in the wxdisplay.py file.

    When generating a new display from wxFormBuilder, replace every instance of

    def __init__( self, parent ):
    by
    def __init__( self, parent, o_node ):

    """

    class MainMenu_Wrapper(wxdisplay.MainMenu):

        def __init__(self, parent, o_node):
            wxdisplay.MainMenu.__init__(self, parent, o_node)
            self.parent = parent
            self.node = o_node

        def load_public_key(self, event):
            # Every time a new file is entered, we first check it exists
            if os.path.isfile(event.GetPath()):
                with open(event.GetPath(), "rb") as fl:
                    try:
                        pubkey = RSA.importKey(fl.read())
                        # Checks if the RSA key is public and if the lenght is correct
                        if pubkey.has_private() and pubkey.size_in_bytes() == self.node.KEYS_LENGTH:
                            raise TypeError
                    except (ValueError, IndexError, TypeError):
                        self.publicKey_filePicker.SetPath(u"Invalid pubkey file !")
                        return
                    self.node.publicKey = pubkey
                self.post_key_load()

        def load_private_key(self, event):
            # Every time a new file is entered, we first check it exists
            if os.path.isfile(event.GetPath()):
                with open(event.GetPath(), "rb") as fl:
                    try:
                        privkey = RSA.importKey(fl.read())
                        # Checks if the RSA key is private and if the lenght is correct
                        if not privkey.has_private() and privkey.size_in_bytes() == self.node.KEYS_LENGTH:
                            raise TypeError
                    except (ValueError, IndexError, TypeError):
                        self.privateKey_filePicker.SetPath(u"Invalid privkey file !")
                        return
                    self.node.privateKey = privkey
                self.post_key_load()

        def post_key_load(self):
            if self.node.check_enc_dec():
                # Deduce the current node's id and auth (pass) from the private key's RSA modulus' hash (a public value)
                self.node.id = SHA256.new(str(self.node.privateKey.n).encode("utf-8")).hexdigest()[:self.node.ID_LEN]
                print(self.node.id)
                # Set a name for the node
                self.node.set_name()
                # And display it
                self.nodeName_staticText.SetLabel(self.node.name)
                self.showConversations_Button.Enable(True)
            else:
                self.showConversations_Button.Enable(False)

        def open_pair_creation_window(self, event):
            keygen = Display.CreateNewKeyPair_Wrapper(self, self.node)
            keygen.Show()
            self.Hide()

        def show_conversations(self, event):
            if self.node.check_enc_dec():
                self.node.networking.submit_identity_to_node_server()
                self.node.networking.get_nodes_from_server()
                chat = Display.ReceivedMessages_Wrapper(self, self.node)
                chat.Show()
                self.Hide()
            else:
                self.showConversations_Button.Enable(False)

    class CreateNewKeyPair_Wrapper(wxdisplay.CreateNewKeyPair):

        def __init__(self, parent, o_node):
            wxdisplay.CreateNewKeyPair.__init__(self, parent, o_node)
            self.parent = parent
            self.node = o_node
            self.keyPairLocation_dirPicker.SetPath(os.path.dirname(os.path.abspath(__file__)))

        def __del__(self):
            self.parent.Show()

        def create_key_pair(self, event):
            """
            Displays a loading screens, then create a pair of RSA keys.
            Deduces an id from the privatekey before storing them in their respective .pem files.
            """

            self.loadingTitle_staticText.SetForegroundColour(wx.Colour(0, 0, 0))
            self.loadingInfo1_staticText.SetForegroundColour(wx.Colour(0, 0, 0))
            self.loadingInfo2_staticText.SetForegroundColour(wx.Colour(0, 0, 0))
            self.Refresh()

            # Create a new RSA private key.
            privkey = RSA.generate(self.node.KEYS_LENGTH)
            pubkey = privkey.publickey()

            # Deduce an id from the private key's hash.
            id = SHA256.new("".join([pubkey.n, pubkey.e]).encode("utf-8")).hexdigest()[:self.node.ID_LEN]
            print("ID: " + id)

            with open(u"{}/private_{}.pem".format(event.GetPath(), id), "wb") as fl:
                fl.write(privkey.save_pkcs1())
            with open(u"{}/public_{}.pem".format(event.GetPath(), id), "wb") as fl:
                fl.write(pubkey.save_pkcs1())

            self.Close()
            self.__del__()

    class ReceivedMessages_Wrapper(wxdisplay.ReceivedMessages):

        def __init__(self, parent, o_node):
            wxdisplay.ReceivedMessages.__init__(self, parent, o_node)
            self.parent = parent
            self.node = o_node

        def __del__(self):
            self.parent.Show()

        def filter_search(self, event):
            event.Skip()

        def open_chat_id(self, event):
            event.Skip()

        def send_message_to_new_node(self, event):
            event.Skip()

    class Conversation_Wrapper(wxdisplay.Conversation):

        def __init__(self, parent, o_node):
            wxdisplay.Conversation.__init__(self, parent, o_node)
            self.parent = parent
            self.node = o_node

        def send_message_to_current_node(self, event):
            event.Skip()


class Node:

    ID_LEN = 16
    PASS_LEN = 6

    KEYS_LENGTH = 4096

    def __init__(self):
        self.display = Display(self)
        self.privateKey, self.publicKey = None, None
        self.main()
        self.display.app.MainLoop()

    def main(self):
        self.start_server("192.168.0.48", 62489)

    def check_enc_dec(self):
        """
        Checks if the specified private and public keys are corresponding (if they are part of the same pair).
        Returns True if they are, False if not, None if they are not both set.
        """
        if self.privateKey and self.publicKey:
            try:
                testMessage = b"Check"
                if PKCS1_OAEP.new(self.privateKey).decrypt(PKCS1_OAEP.new(self.publicKey).encrypt(testMessage)) == testMessage:
                    return True
                else:
                    raise (ValueError, TypeError)
            except ValueError:
                return False
        else:
            return None

    def start_server(self, host, port):
        """
        Initiate server as a daemon, to manage messages in real-time.
        """
        self.networking = Networking(self, host, port)
        t_net = threading.Thread(target = self.networking.listen_for_message, name = "netThread", daemon = True)
        t_net.start()

    def get_name(self, id) -> str:
        """
        Creates a name depending on the id of the node.
        """

        def hex_to_decimal(number) -> int:
            """
            Converts an hexadecimal value to its decimal equivalent
            """
            finalNumber = 0
            # Flips the value
            number = str(number)[::-1]
            for index, character in enumerate(number):
                try:
                    character = int(character)
                except ValueError:
                    character = ord(character) - 87
                finalNumber += character * (16 ** index)
            return finalNumber

        import dictionnary

        index = 0

        adjectives = dictionnary.dictionnary["adjectives"]
        # Gets a slice of the id
        adjRepr = int(str(hex_to_decimal(id))[index:len(str(len(adjectives))) + index])
        adjective = adjectives[adjRepr % len(adjectives)]
        index += len(str(len(adjectives)))
        # Capitalize the first letter of the word
        adjective = adjective[0].upper() + adjective[1:]

        animals = dictionnary.dictionnary["animals"]
        aniRepr = int(str(hex_to_decimal(id))[index:len(str(len(animals))) + index])
        animal = animals[aniRepr % len(animals)]
        index += len(str(len(animals)))
        animal = animal[0].upper() + animal[1:]

        return "".join([adjective, animal])

    def set_name(self):
        self.name = self.get_name(self.id)


class Message:

    def __init__(self, o_node, charset = "utf-8"):
        self.node = o_node
        self.MAX_MESSAGE_LENGTH = (self.node.KEYS_LENGTH / 8) - 42
        self.CHARSET = charset


class Envelope:

    def __init__(self, o_message):
        self.MESSAGE_OBJECT = o_message

    def encode_to_json(self):
        return

    def proof_of_work(self, ):
        return


class Networking:

    BUFF_SIZE = 4096
    MAX_CONN = 5 # Maximum connections

    # You can either enter your LAN IP, if you only use the tool on a local network, or your WAN IP, in which case you must open a port on your box.
    MY_ADDRESS = "192.168.0.48"

    NODE_SERVER_API_NODES_ENDPOINT = "http://192.168.0.48:42202/nodes"

    def __init__(self, o_node, host, port):
        self.node = o_node
        self.HOST = host
        self.PORT = port
        self.CONNECTION_LIST = []

    def __del__():
        self.node.display.mainFrame.serverStatus_staticText.SetForegroundColour(wx.Colour(255, 0, 0))
        self.node.display.mainFrame.serverStatus_staticText.SetLabel("Down")

    def listen_for_message(self):
        """
        Setup a server and listen on a port
        """

        def recvall(sock):
            """
            Used to receive all parts of a network-sent message
            """
            data = bytes()
            while True:
                part = sock.recv(self.BUFF_SIZE)
                data += part
                if len(part) < self.BUFF_SIZE:
                    # either 0 or end of data
                    break
            return data

        serverSocket = socket.socket()
        serverSocket.bind((self.HOST, self.PORT))
        serverSocket.listen(self.MAX_CONN)

        self.node.display.mainFrame.serverStatus_staticText.SetForegroundColour(wx.Colour(0, 255, 0))
        self.node.display.mainFrame.serverStatus_staticText.SetLabel("Up")

        while True:
            connection, address = serverSocket.accept()
            print(recvall(connection))

    def submit_identity_to_node_server(self):
        """
        Submit own identity to the node registry server, via its API.
        """
        info = {"pubkey_n": str(self.node.publicKey.n), "pubkey_e": str(self.node.publicKey.e), "address": ":".join([str(self.MY_ADDRESS), str(self.PORT)])}

        # Hash object of the pubkey
        h = SHA256.new("".join([info["pubkey_n"], info["pubkey_e"]]).encode("utf-8"))

        # Hexadecimal digest of the above hash
        info["hash"] = h.hexdigest()
        # And its signature encoded in base64
        info["sig"] = base64.b64encode(pkcs1_15.new(self.node.privateKey).sign(h)).decode("utf-8")

        r = requests.post(self.NODE_SERVER_API_NODES_ENDPOINT, data = info)
        if r.status_code != 201:
            print("Could not submit identity to server ({}). Please verify its IP address is correct and that it is running.".format(r.status_code))
            return

        return

    def get_nodes_from_server(self):
        """
        Request the nodes list to the node registry server's API.
        """
        r = requests.get(self.NODE_SERVER_API_NODES_ENDPOINT)
        with open("known_nodes.json", "w") as nl:
            json.dump(r.json()["data"], fp = nl, indent = 4)

    def send_message(self, message):
        """
        Sends a message to all known nodes, except the original sender.
        Message must be a bytes-encoded string.
        """
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((self.HOST, self.PORT))
        clientsocket.send(message)


if __name__ == '__main__':
    client = Node()
