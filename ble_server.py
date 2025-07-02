import asyncio
import socket
import ctypes
from bleak import BleakClient

# BLE Setup
ctypes.windll.ole32.CoInitializeEx(0, 0)
BLE_ADDRESS = "F0:F5:BD:50:E7:E9"   # Update to your Arduino MAC
BLE_CHARACTERISTIC_UUID = "2A56"

async def send_ble_alert(message):
    try:
        async with BleakClient(BLE_ADDRESS) as client:
            if client.is_connected:
                print("Connected to BLE device")
                await client.write_gatt_char(BLE_CHARACTERISTIC_UUID, message)
    except Exception as e:
        print(f"BLE error: {e}")

async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(1)
    print("BLE server listening...")

    while True:
        client_sock, addr = server.accept()
        data = client_sock.recv(1024).decode()
        if data == "ALERT":
            await send_ble_alert(b"ALERT")
        elif data == "RESET":
            await send_ble_alert(b"RESET")
        client_sock.close()

if __name__ == "__main__":
    asyncio.run(main())
# python ble_server.py