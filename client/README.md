# Introduction

SCA is a decentralized communication application.
The acronym stands for "Secure Chat App".
This application allows for text message exchange.
The network is decentralized, meaning no one can control it, and is end-to-end secured.

It is inspired by [Ethereum Whisper](https://geth.ethereum.org/docs/whisper/how-to-whisper) 
and the [Scuttlebutt protocol](https://ssbc.github.io/scuttlebutt-protocol-guide/).

# Keys and identities

The first thing a user needs to participate in the SCA network is an identity. 
An identity is called a "node" and is roughly a RSA key pair and typically represents a person, a device, 
a server or a bot. 
It’s normal for a person to have several identities.

Because identities are long and random, no coordination or permission is required to create a new one, 
which is essential to the network’s design.

A name is generated from the user's RSA keys, giving it a readable identifier among other nodes.

If a user loses their secret key or has it stolen they will need to generate a new identity.

The public key of an identity is presented to users and transmitted 
in some parts of the network protocol. For more information on this topic, please refer to the "Node" terms section.

Emphasizing on identities: there are two very different entities linked to a node, one explicitly : 
a node identity, identified by a public RSA key, and another hidden: a contact information, 
identified by an address and a port.

# Discovery

After a user has generated their identity they need to find some peers to connect to.
To connect to a peer you need to know its address (IP or DNS name) and a port number.

## Local network

Once a node is registered on a client (see "Terms" section for more information), 
the node will broadcast over the network a specific packet, while listening for answers.
The client will send a packet every 10 seconds.
When a peer sees another peer’s broadcast packet they can connect to exchange messages.
The clients will show discovered peers (nodes) in the user interface.

## Invite code

Not implemented.

## Beacons

A beacon is a node that is assured to run a client at all time.
They are hard-coded inside the project and added and/or removed by the project maintainers.

While this goes against the decentralized design, like Bitcoin, it is a good way to discover new nodes.

# Peer connections

TODO

# Message

When a node receives a message, the first thing it will do is to broadcast it back onto the network.
Next, because we can’t see who the message is addressed to, 
we will attempt to decrypt every private message we come across in case it is for us.

# Protocols

Every request made over the network has this structure:

```json
{
  "status": "REQUEST_NAME",
  "data": {
    ...information...
  },
  "timestamp": "timestamp"
}
```

## What's Up Protocol - "WUP"

```json
{
  "status": "WUP_INI",
  "data": {
    "timestamp": 123456,
    "author": ...simple_contact_structure...
  },
  "timestamp": "timestamp"
}
```

1. We wake up: the user launched the client and loaded his RSA private key.
2. We read the "raw_messages" database, and we get the most recent "time_received".
3. We send a "WHATSUP" request (with above structure) to preferably a Beacon, otherwise a regular node,  
and as "timestamp" the last received message "time_received" value.

```json
{
  "status": "WUP_REP",
  "data": {
    ...request_structure...
  },
  "timestamp": "timestamp"
}
```

1. We receive the "WHATSUP" request.
2. We loop through the "raw_messages" database, and for each message, 
we check if "time_sent" <= request_timestamp ; 
if it is, then we send the message to this specific node with the above request structure.

## Keys Exchange Protocol - "KEP"

- This protocol is used when negotiating a new AES key for a conversation.
    - Note that this key is only used to encrypt and decrypt for network communication.
    Once we decrypt a message, we encrypt it with our own AES key and store it.
- This is similar to the Diffie-Hellman protocol.
- This avoids having one node in charge of deciding the AES key.

1. We detect a new node on the network (we therefore have its public key)
2. We choose a random 16 bytes key (technically, AES key length / 2).
3. We send over the network a new "AES_KEY_NEGO" request:

```json
{
  "status": "AKE",
  "data": {
    "key": {
      "value": "16_bytes_rsa_encrypted_AES_key",
      "hash": "hash_of_the_key",
      "sig": "signature_of_the_above_hash"
    },
    "author": ...node_structure...,
    "recipient": ...node_structure...
  },
  "timestamp": "timestamp"
}
```

4. We wait for the reply, and store the request in the conversation database. Its status is "WAITING" meanwhile.
5. Once we get a response to this request, we verify its content and
we assemble the two binary keys and derive a nonce from the key.
We do not exchange that key over the network. If the protocol has been respected by both party, 
they should both have the same key and nonce.

1. If we receive a new "AES_KEY_NEGO" request (we have not sent one yet).
2. We verify the content.
3. We then generate a new 16 bytes random value, and send it over with the same structure as above.
4. We construct the key and derive the nonce, then we store it.
5. At this point, we have a working key, and so should the recipient.

1. If the key is already defined (it has already been negotiated with the node before)
2. We deny the negotiation, but we send our key part to the node.

1. We sent our key part to the node, but we didn't get any response.
2. If the timestamp is greater than 3 months, we delete the entry.

: Comment savoir de qui viens le message ? Comment choisir la bonne clef AES ?

## Message Propagation Protocol - "MPP".

This protocol is called when a message is received.
A typical JSON-encoded network message looks like this:

```json
{
  "status": "MPP",
  "data": {
    ...message_structure...
  },
  "timestamp": "timestamp"
}
```

Requirements:
\
AKE protocol must be complete with the conversation node.

1. We receive a message.
2. We check if we already received that message, using its ID.
3. If not, we broadcast the message.
4. We store the message in the "raw_messages" database.
5. We try to decrypt its content.
6. If we're able to access the decrypted content, 
we re-encrypt the message with our own AES key, and we store it in the "conversations" database.

## Node Publication Protocol - "NPP"

This protocol is used when sending a node identity over the network.

1. We have an identity to broadcast.
2. We broadcast it with this request form:

```json
{
  "status": "NPP",
  "data": {
    ...node_structure...
  },
  "timestamp": "timestamp"
}
```

## Contact Sharing Protocol - "CSP"

## Discover Pub Protocol - "DPP"

## Discover Contact Protocol - "DCP"

# *Terms*

## Client

- The client is the SCA software.
- One client can host multiple nodes, while not at the same time.
- It is a relay on a network via its contact information.

## Node

### "Simple" node

- A node is an individual on the network, identified by a RSA public key.
    - Two values are derived from this key (modulus (n) and public exponent (e)):
        - Its ID ; which length is defined by the config attribute "id_len".
        - Its name ; a series of words picked the file "dictionary".
- Its structure is defined as:

```json
{
    "rsa_n": 1234567890,
    "rsa_e": 123456,
    "hash": "Hash_of_the_above_information",
    "sig": "Signature of the above hash"
}
```

### Master node

- A master node is our own client.
- Unlike the simple node, we have the RSA private key.

## Messages

- Messages are python objects that can be exported to JSON for network communication and storage.
- Theses messages are structured as follows:

```json
{
    "content": "aes_encrypted_message",
    "meta": {
        "time_sent": "123456780",
        "digest": "hash_digest"
    },
    "author": ...node_architecture...
}
```



# Databases

## Raw messages database

- This database contains every single message received and sent by the client.
- When stored, these messages looks like this:

```json
{
    "content": "aes_encrypted_message",
    "meta": {
        "time_sent": "123456780",
        "time_received": "123456789",
        "digest": "hash_digest",
        "id": "identifier"
    },
    "author": ...node_architecture...
}
```

- The messages are not sorted. (maybe they should be ?)

## Conversations database

- This database contains each node's conversation (messages and aes keys).
    - Messages are stored in the "conversation" table.
    - AES keys are stored in the "keys" table.
        - Each key is used to decrypt messages received ; once they are decrypted, 
        we encrypt and store them using our own AES key, which is referenced under our own ID in the database.
        - The "key" is the 32 bytes key concatenated with the 16 bytes nonce.
        - Each key is unique to the conversation.
        - Keys are negotiated with an asynchronous handshake. 
        More on that in the "AKE" protocol section.
        - In the keys table is a key referenced with our own ID.
- The database is structured as follows:

```json
{
    "conversations": {
        "node_identifier": {
            "message_identifier": {
                "content": "aes_encrypted_message",
                "meta": {
                    "time_sent": "123456780",
                    "time_received": "123456789",
                    "digest": "hash_digest",
                    "id": "identifier"
                }
            }
        }
    },
    "keys": {
        "node_identifier": {
            "key": "aes_key",
            "status": "DONE | IN_PROGRESS",
            "timestamp": "123456789"
        }
    }
}
```

## Contacts database

- This database holds information about all the contacts (the devices that runs a client) we know.
- Note that a contact is not a node nor are they related.
- The database is structured as follows:

```json
{
    "contacts": {
        "contact_identifier": {
            "address": "address:port",
            "last_seen": "timestamp"
        }
    }
}
```
