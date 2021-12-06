#!/usr/bin/python3
import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
if nickname == "admin":
    password = input("Enter the password for the admin : ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

stop_Thread = False

# Listening to Server and Sending Nickname


def receive():
    while True:
        global stop_Thread
        if stop_Thread:
            break
        try:
            # Receive Message from Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password!")
                        stop_Thread = True
                elif next_message == 'BAN':
                    print("Connection refused becaude of ban !")
                    client.close()
                    stop_Thread = True
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error Occured!")
            client.clode()
            break


def write():
    while True:
        if stop_Thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
                else:
                    print("Commands can only be executed by admin!")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
