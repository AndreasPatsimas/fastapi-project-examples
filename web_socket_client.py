from loguru import logger
import ssl

from paho.mqtt.client import Client


def on_connect(mqttc, obj, flags, rc):
    logger.info("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print("ttterersss",  msg)
    print("ttterersss.topic",  msg.topic)
    print("ttterersss.qos",  msg.qos)
    print("ttterersss.payload",  msg.payload)
    logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    logger.info("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print("teers", string)
    logger.info(string)


mqttc = Client('spectrum_mqtt', transport='websockets')
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.tls_set(cert_reqs=ssl.CERT_NONE)
mqttc.tls_insecure_set(True)
token = 'eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE2ODc3NzkyNTIsImlhdCI6MTY4Nzc3NzQ1Miwic3ViIjoiYWRtaW4iLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIn0.Ty6w-CkG8AQ-QZzzGTpXQZzYyr8VJ5bi63GhhpsSo-s0yYWM4PHQ7V-otIpkL1mW2Q4BA14JXGJK0H2vZ5tfmgaUrAEsYOhbXJ-PXwHuIkiPM5PuaZpdB6XvtWiCo1q9K74gHwEcl8xjesR3LnnfAqgYvyspUW0rvIzn7KNI2BuwE2s-bF9bNLed0SxEewv71iclqjMv9_8L83I3kMN98X8OmKcJgHs3YYrFv-5fWd37ZD64_D57E2n2jFKeTslEM25f_gyjHykzv7wbZVs8CvE6rzunonOh_yzd0dpMyleQ0qlBAp0pkUe1i2sMF7P4VY6wojZNKuFfgVMcCY4giFOeJIBqh4i7Z1vqcE-QA4UjWUBGMOLWIWFQnPVv1ov_N12dMo8aWYtita8dob6TckCmtrHO36cIXZsQdBexHLb530dS_hIrDEh9ihCAyhsjSZAZv8enrbqgIFmXhoxGjmDzyyIsUy-Oa08kWkzatllSw-yqXeXVDwV1_ljkMPiO'
mqttc.username_pw_set("jwt-token-username", token)
mqttc.connect("localhost", 8443, 60)
mqttc.enable_logger(logger)
mqttc.subscribe("#", 0)

mqttc.loop_forever()
