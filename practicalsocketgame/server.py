import socket
import threading
from player import Player
import pickle
server='192.168.0.105'
port=5006
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))  
except socket.error as e:
    str(e)
    
s.listen()
print('Waiting for listening')
players=[Player(0,0,50,50,(255,0,0)),Player(100,100,50,50,(0,0,255))]

def handle_client(conn,addr,player):
    conn.send(pickle.dumps(players[player]))
    reply=''
    while True:
        try:
            data=pickle.loads(conn.recv(2048))
            players[player]=data
            
            if not data:
                print('Disconnected')
                break
            else:
                if player==1:
                    reply=players[0]
                else:
                    reply=players[1]
                print('recieved',data)
                print('Sending',reply)
            conn.sendall(pickle.dumps(reply))
        except :
            break
    print('Lost Connection')
    conn.close()
currentplayer=0
while True:
    conn,addr=s.accept()
    print('Connected to:',addr)
    thread=threading.Thread(target=handle_client,args=(conn,addr,currentplayer))
    thread.start()
    currentplayer+=1