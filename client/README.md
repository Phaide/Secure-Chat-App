# Secure chat app

## Description

Secure Chat App (SCA or another unnamed project) is a Python 3 peer-to-peer (P2P) chat app, secured by end-to-end encryption.
It is very similar in its conception to Ethereum Whisper.

## Concepts

### Message

A message is a block of utf-8 text.

### Envelope

An envelope contains a compressed and encrypted message.
The encryption is asymetric, meaning only the intended recipient can read its content.

### Node

A node is a client running the application.
It can send and receive messages.

## Requirements

Requirements are listed in the `requirements.txt` file.
Install them with the command

```
pip install -r requirements.txt
```
