import socket
from threading import Thread
import time
class Server:
    def __init__(self):
        self.serverHost = '127.0.0.1'
        self.serverPort = '8888'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.storeName = dict()
        self.keyStore = dict()

    def clientSupport(self, conn, userName):
        while True:
            name = conn.recv(1024).decode()
            userType = conn.recv(1024).decode()
            operationType = conn.recv(1024).decode()

            if userType == 'g' and operationType == 'get':
                attribute = conn.recv(1024).decode()
                time.sleep(0.05)
                if name != userName:
                    conn.send("Sorry! You need manager privilages for doing this!".encode())
                else:
                    userData = self.keyStore.get(name, 'null')
                    # print(self.keyStore.get(name, 'null'))
                    if userData == 'null':
                        # self.keyStore[name] = dict()
                        response = '\n'
                        conn.send(response.encode())
                    else:
                        result = userData.get(attribute, 'null')
                        response = result if result != 'null' else '\n'
                        conn.send(response.encode())

            elif userType == 'g' and operationType == 'put':

                attribute = conn.recv(1024).decode()
                #time.sleep(0.05)
                value = conn.recv(1024).decode()
                time.sleep(0.05)
                if name != userName:
                    conn.send("Sorry! You need manager privileges for doing this!".encode())
                else:
                    userData = self.keyStore.get(name, 'null')
                    if userData == 'null':
                        self.keyStore[name] = dict()

                    self.keyStore[name][attribute] = value
                    conn.send('Data added successfully!'.encode())

            elif userType == 'g' and operationType == 'u':
                print(f"              {name} now has manager privileges!")
                print("-------------------------------------------------------------------------")
                userType = 'm'

            elif userType == 'm' and operationType == 'put':
                attribute = conn.recv(1024).decode()
                value = conn.recv(1024).decode()
                if self.storeName.get(name, 0) == 0:
                    conn.send('invalid username!'.encode())
                else:
                    userData = self.keyStore.get(name, 'null')
                    if userData == 'null':
                        self.keyStore[name] = dict()

                    self.keyStore[name][attribute] = value
                    conn.send('Data added successfully!'.encode())

            elif userType == 'm' and operationType == 'get':
                attribute = conn.recv(1024).decode()
                userData = self.keyStore.get(name, 'null')
                if userData == 'null':
                    response = 'invalid username'
                    conn.send(response.encode())
                else:
                    result = userData.get(attribute, 'null')
                    response = result if result != 'null' else 'no value present'
                    conn.send(response.encode())

            elif operationType == 'end':
                conn.send(f"Good bye {userName}".encode())
                conn.close()
                print(f"              {name} has logged out from the server")
                print("-------------------------------------------------------------------------")
                break

    def runServer(self):

        self.socket.bind(('localhost', 8888))
        self.socket.listen(10)
        print("          The server is running on 127.0.0.1 and port 8888!")
        print("-------------------------------------------------------------------------")
        threadPool = []
        while True:
            conn, addr = self.socket.accept()
            conn.send("[+] Connected.".encode())

            name = conn.recv(1024).decode()

            if self.storeName.get(name, 0) == 0:
                self.storeName[name] = 1
                conn.send("   Registration successful!".encode())
            else:
                conn.send(f"{name} Welcome back!".encode())
            print("      ", name, " has logged into the server with ip & port ", addr, "!")
            print("-------------------------------------------------------------------------")
            thread = Thread(target=self.clientSupport, args=(conn, name))
            threadPool.append(thread)
            thread.start()


if __name__ == "__main__":
    server = Server()
    server.runServer()
