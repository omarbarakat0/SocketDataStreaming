import socket
import base64
import json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.0.103'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    
    """
    Send messages over socket
    
    Parameters:
            msg: message has to be sent
            
        msg_length: extract message length, and assign number of bytes
        FORMAT: encode message to bits
        
        
    Return:
            send message over socket as json file
            
    """
    
    # encode message to bits
    message = msg.encode(FORMAT)
    
    # Message length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    
    # extract message lenght and add padding space until 64 bytes are filled
    send_length += b' ' * (HEADER - len(send_length))
    
    # Send message length
    client.send(send_length)
    
    # send origonal message
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    
    
image_file = 'truck_test.jpg' 
with open(image_file, "rb") as f:
    im_bytes = f.read() 
    
im_b64 = base64.b64encode(im_bytes).decode("utf8")
payload = json.dumps({"image": im_b64, "Name": image_file})

send("Hello World!")
input()
send(payload)
input()
send("Hello Omar!")

send(DISCONNECT_MESSAGE)