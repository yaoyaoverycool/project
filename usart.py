import serial
from time import sleep

def recv(serial):
    while True:
        data=serial.read_all().hex()
        if data==' ':
            continue
        else:
            break
        sleep(0.02)
    return data

def send(serial,send_data):
    if serial.isOpen():
        serial.write(send_data.encode('utf-8'))
        print('发送成功',send_data)
    else:
        print('发送失败')
