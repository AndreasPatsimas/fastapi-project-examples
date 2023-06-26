from typing import Optional, Dict
import json
from loguru import logger
import ssl
import requests
from paho.mqtt.client import Client
import time


def get_target(ip: str, port: Optional[int] = None, protocol: str = "http"):
    if port and str(port).endswith("43"):
        protocol = "https"
    target = f"{protocol}://{ip}"
    if port:
        target = f"{target}:{port}"
    return target


# target = get_target("192.168.239.1", 443)
target = get_target("localhost", 8443)
login_endpoint = f"{target}/api/oauth/token-json"
username = "admin"
password = "N@v@r1n0"
session = requests.Session()
payload = {"username": username, "password": password, "grant_type": "password"}

response = session.post(
    login_endpoint,
    json=payload,
    timeout=10,
    verify=False,
)

successful_login = response.json()
token = successful_login["access_token"]


def get_sailor_firmware_data(token: str) -> Dict[str, Dict]:
    start_time = time.time()
    timeout = 5

    system_info_topic = "mqtt/dashboard/system-info"
    antenna_topic = "mqtt/dashboard/antenna"
    modem_topic = "mqtt/dashboard/modem"
    pointing_topic = "mqtt/dashboard/pointing"

    system_info_bytes = None
    antenna_bytes = None
    modem_bytes = None
    pointing_bytes = None

    def on_connect(mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc))

    def on_message(mqttc, obj, msg):
        nonlocal system_info_bytes, antenna_bytes, modem_bytes, pointing_bytes
        if msg.topic == system_info_topic:
            system_info_bytes = msg.payload

        if msg.topic == antenna_topic:
            antenna_bytes = msg.payload

        if msg.topic == modem_topic:
            modem_bytes = msg.payload

        if msg.topic == pointing_topic:
            pointing_bytes = msg.payload

        logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(mqttc, obj, mid):
        logger.info("mid: " + str(mid))

    def on_subscribe(mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(mqttc, obj, level, string):
        logger.info(string)

    mqttc = Client('spectrum_mqtt', transport='websockets')
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.tls_set(cert_reqs=ssl.CERT_NONE)
    mqttc.tls_insecure_set(True)
    mqttc.username_pw_set("jwt-token-username", token)
    mqttc.connect("localhost", 8443, 60)
    mqttc.enable_logger(logger)
    mqttc.subscribe("#", 0)

    mqttc.loop_start()

    try:
        while True:

            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                break

            pass

    except KeyboardInterrupt:
        pass

    # Stop the network loop
    mqttc.loop_stop()
    mqttc.disconnect()

    # Parse the JSON string into a dictionary
    system_info = json.loads(system_info_bytes.decode()) if system_info_bytes else {}
    antenna = json.loads(antenna_bytes.decode()) if antenna_bytes else {}
    modem = json.loads(modem_bytes.decode()) if modem_bytes else {}
    pointing = json.loads(pointing_bytes.decode()) if pointing_bytes else {}

    return {
        "system_info": system_info,
        "antenna": antenna,
        "modem": modem,
        "pointing": pointing,
    }


data = get_sailor_firmware_data(token)
print(data)
