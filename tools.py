import json
import base64

def EncodeMessage(status, message, **kwargs):
    dict = {
        "status": status,
        "mensage": message,
        }
    for arg in kwargs:
        dict.update([arg[0], arg[1]])

    encodedMessage = base64.b64encode(bytes(str(dict),'utf-8'))
    return encodedMessage

def DecodeMessage(message):
    decodedMessage = json.loads(base64.b64decode(message).decode('utf-8').replace("'",'"'))
    return decodedMessage

dictVar = EncodeMessage(202, "Hello World!", kwargs=[["user", "Otoma"],])
print(dictVar)
print(DecodeMessage(dictVar))