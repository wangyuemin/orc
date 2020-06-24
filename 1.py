import uuid

def get_mac_address():

    node = uuid.getnode()

    mac = uuid.UUID(int = node).hex[-12:]
    print(mac)
get_mac_address()