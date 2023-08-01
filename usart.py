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

if __name__ == '__main__':
    serial=serial.Serial('COM5',9600,timeout=0.5)
    if serial.isOpen():
        print('open success')
    else:
        print('open failed')

    while True:
        a=input("请输入要发送的数据：")
        send(a)
        sleep(0.5)
        data=recv(serial)
#        print('data=',data,'|')
        if data!='':
            print("receive:",data)
#           print(type(data))
            if data=='71':
                print('exit')
                break
    serial.close()