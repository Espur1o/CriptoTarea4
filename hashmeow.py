import socket
import sys
import ecdsa
import os
import subprocess
import hashlib
from datetime import datetime, timedelta 
#----CRACKEO-----
def crack(archivo, dicc, salida,modo):
    ini_time= datetime.now() 
    #Archivo 1: -m (0) md5  
    #Archivo 2: -m 0 (10) 20 30 40 50 60 900 3500 3610 3710 3720 3810 3910 4010 4110 4210 4300 4400 
    #Archivo 3: -m 0 (10) 20 23 30 40 50 60 900 1100 3000 3500 3610 3710 3720 3810 3910 4010 4110 4210 4300 4400 8600 11000
    #Archivo 4: -m 0 10 20 23 30 40 50 60 900 (1000) 1100 2100 2600 3000 3500 3610 3710 3720 3810 3910 4010 4110 4210 4300 4400 8300 8600 9900 11000
    #Archivo 5: -m (1800)
    subprocess.run([r"C:/Users/Espur1o/Desktop/Cripto/Tarea 4/hashcat-6.1.1/hashcat-6.1.1/hashcat.exe", "-m",modo,"-a", "0", "--outfile", salida , archivo,dicc])
    end_time= datetime.now()
    final_time=(end_time- ini_time)
    print ("Proceso de crackeo.")
    print ("HORA DE INICIO: " + str(ini_time))
    print ("HORA FINAL: " + str(end_time))
    print ("DELTA: " + str(final_time) )
    return salida
#----CRACKEO-----
#----PASS TEXTO PLANO-----
def to_plain(arch):
    archivo=open(arch)
    plain=[]
    for linea in archivo:
        plano=linea.strip().split(":")[-1] #se necesita el ultimo dato de cada linea
        plain.append(plano)
    return plain
#----PASS TEXTO PLANO-----
#----PASS PBKDF2-----
def pbkdf(plain):
    hashed=[]
    salted=[]
    stored=[]
    for pw in plain: 
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            pw.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            1000, 
            dklen=64 # Llave de 64 bytes
        )
        key=key.hex()
        salt=salt.hex()
        #storage= salt + key
        #stored.append(storage)
        hashed.append(key)
        salted.append(salt)
    return (stored, hashed, salted)    
#-----PASS PBKDF2----
#-----HASH TO TEXT----
def totext(lista1,lista2,salida):
    archivo=open(salida,"w")
    #print (len(lista1))
    #print (lista1)
    for i in range(len(lista1)):
        archivo.write(str(lista1[i]) +":"+str(lista2[i])+"\n")
    archivo.close()
    return None    
#-----HASH TO TEXT----




#-----Variables----
n=1
archivo="C:/Users/Espur1o/Desktop/Cripto/Tarea 4/hashes/archivo_"+str(n)+".hash"
dicc= "C:/Users/Espur1o/Desktop/Cripto/Tarea 4/dict/diccionario_2.dict"
salida="C:/Users/Espur1o/Desktop/Cripto/Tarea 4/cracked/outp" +str(n)+".txt"
salidaPB="C:/Users/Espur1o/Desktop/Cripto/Tarea 4/hashpb/hashpb"+str(n)+".txt"
salidaSalt="C:/Users/Espur1o/Desktop/Cripto/Tarea 4/hashpb/hashsalt"+str(n)+".txt"
# arch1:0 arch2:10 arch3:10 arch4:1000 arch5:1800
modo=str(0)  
#-----Variables----
arch=crack(archivo, dicc, salida, modo)
#se entrega el tiempo de crackeo
plano=to_plain(arch)#genera una lista de los resultados que fueron guardado en el txt
print ("NUMERO DE HASHES"+str(len(plano)))
i_time=datetime.now()#INICIO proceso hash PBKDF2
s,h,salted=pbkdf(plano)
f_time=datetime.now() #FIN proceso hash
d_time=(f_time - i_time)
print ("Proceso de HASH.")
print ("HORA DE INICIO: " + str(i_time))
print ("HORA FINAL: " + str(f_time))
print ("Tiempo que tomó hashear el listado: " + str(d_time))
totext(h,salted,salidaPB)

#-----------------------------------------------
#--------FINAL DE HASH---------------------------
#-----------------------------------------------
#with open("remote_public_key.pem") as e:
#    remote_public_key = e.read()
#ecdh.load_received_public_key_pem(remote_public_key)
#secret = ecdh.generate_sharedsecret_bytes()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

#Se abre el archivo
archivo=open(salidaPB)
    

try:
    for linea in archivo:

        # Send hash
        linea=linea.strip()
        message = linea.encode("utf-8") #encode to bytes
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))
        sock.sendall(b"-LIN")
        data = sock.recv(16)
        print('received {!r}'.format(data))

finally:
    data = sock.recv(16)
    print('closing socket')
    sock.close()