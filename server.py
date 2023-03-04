import socket 
import threading
import json
import base64

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    
    '''
    get message (image in json_serialize) from each client, decode it and save it
    
    Parameters:
            conn: client conected to the server (sending and receiving messages)
            addr: IP address connected to the server (exp - 192.168.#.###)
            
            
    Return:
            Handle clients that are connected to the server
            receive msg, decode it and accept it
            
    
    
    '''
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    
    # as long as a client is connected, keep listening
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        # check message is not None, if not proceed
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            # verify that messgae is serilazed in Json
            if '{' in msg:
                
                # write and save msg
                with open('json_serial.json', 'w') as f:
                    f.write(msg)
                
                json_file = json.load(open('json_serial.json'))
                
                image_byte = json_file['image']
                image = base64.b64decode((image_byte))
                img_file = open('image.jpeg', 'wb')
                img_file.write(image)
                img_file.close()
                
            # if disconnect message received, diconnect server
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    '''
    Handle multiple client at the same time using threading
    '''
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        
        # client and address of client requesting connection
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()