import socket
import sys
import sqlite3
import ecdsa
n=1
#g = generator_192
#n = g.order()
#secret = randrange( 1, n )
#pubkey = Public_key( g, g * secret )
#privkey = Private_key( pubkey, secret )
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Utiliza la BD
conn = sqlite3.connect('CRIPTO.db')
c = conn.cursor()
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
listado=[]
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        linea=""

        while True:
            data = connection.recv(16)
            if "LIN" in data.decode("utf-8"):
                listado.append(linea)
                #c.execute("INSERT INTO archivo5 VALUES ("+str(linea)+","+str(linea[:32])+","+str(linea[32:])+")")
                linea=""
                print('sending data back to the client')
                connection.sendall(data)
            if data :
                linea+=data.decode("utf-8")
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
        
        for i in listado:
           # i=i.replace('"',"")
            a,b=i.replace("-LIN","").split(":")
            comando='INSERT INTO archivo{} VALUES ("{}", "{}")'.format(n,a,b)
          
            c.execute(comando)
            conn.commit()
conn.close()

