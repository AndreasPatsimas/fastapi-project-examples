import binascii
import enum
import os
import re
import time
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Optional
from uuid import UUID

from xml.etree import ElementTree as ET

from pydantic import BaseModel, Field
from bs4 import BeautifulSoup

from collections import defaultdict
import paho.mqtt.client as mqtt
import ssl
from typing import Any, Dict, Optional, Union
import requests
import struct
import asyncio
import websockets


def build_connect_packet(client_id):
    # MQTT CONNECT packet fixed header (byte 1)
    fixed_header = 0x10  # CONNECT packet type
    fixed_header |= 0x00  # Remaining length (0 for now)

    # MQTT CONNECT packet variable header
    protocol_name = "MQTT"  # Protocol name
    protocol_level = 4  # MQTT protocol level (4 for MQTT v3.1.1)
    connect_flags = 0x00  # Connect flags (clean session, no will, no password, no username)

    # MQTT CONNECT packet payload
    payload = struct.pack("!H", len(client_id)) + client_id.encode()  # Client ID

    # Calculate the Remaining Length field
    remaining_length = len(protocol_name) + 2 + 1 + 1 + len(client_id)
    remaining_length_byte = b""
    while remaining_length > 0:
        encoded_byte = remaining_length % 128
        remaining_length //= 128
        if remaining_length > 0:
            encoded_byte |= 0x80
        remaining_length_byte += struct.pack("!B", encoded_byte)

    # Construct the complete CONNECT packet
    connect_packet = bytes([fixed_header]) + remaining_length_byte + \
                     protocol_name.encode() + struct.pack("!B", protocol_level) + \
                     struct.pack("!B", connect_flags) + payload

    return connect_packet


# class PackageBase(BaseModel):
#     id: str = Field(..., title="Package id")
#     version: str = Field(..., title="Software version")
#
#
# last_alert_packages = [PackageBase(id='GTMailPlus', version='2.03.1101')]
# packages = [PackageBase(id='GTMailPlus', version='2.03.1101'), PackageBase(id='TotPlus', version='4.03.1201')]
#
# input_data = [PackageBase(id=package.id, version=package.version) for package in packages if
#               package not in last_alert_packages]
#
# print(input_data)

# Assuming you have the necessary imports and class definitions
