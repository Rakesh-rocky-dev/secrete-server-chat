import socket 
import termcolor 
import time
from threading import Thread
from pyngrok import ngrok
def server():
        port = 6969
        server_addrss = "localhost"
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind((server_addrss,port))
        server_socket.listen()
        cli_soc , conn =  server_socket.accept()
        termcolor.cprint(f"connected to [{conn[0]}]","green")
        termcolor.cprint("[SERVER] Initiating handshake..","green")
        while True:
                length = cli_soc.recv(1024).decode()
                message = cli_soc.recv(int(float(length))).decode()
                if not message:
                        break
                if message.lower()[-7:] == "do-exit":
                        termcolor.cprint("[DISCONNECTED]: CLIENT AND SERVER CONNECTION INTEREPTED.","red")
                        server_socket.close()
                        break
                termcolor.cprint(message,"green")
        
        
        
def client(port,tcp):
        client_server_addrss = str(tcp)+".tcp.in.ngrok.io"
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((client_server_addrss,port))
        while True:
                time.sleep(0.5)
                message = input(termcolor.colored("[YOU]: ","magenta"))
                
                if message.lower()[-7:] == "do-exit":
                        break
                send_msg(message,client_socket)
        send_msg("do-exit",client_socket)
        
        
        
def send_msg(message,client_socket):
        package = f"[{username}]: {message}"
        length = str(len(package.encode("utf-8"))).encode("utf-8")
        length += b" "*(16 - int(length.decode()))
        if int(length.decode()) != 0:
                client_socket.send(length)
                client_socket.send(package.encode())
                
        

def auth(username,password):
        return True        
        
        
def initialize():
        global username
        termcolor.cprint("LOGIN TO KNOW WHO YOU ARE","red")
        username = input(termcolor.colored("username: ","blue"))
        passw = input(termcolor.colored("password: ","blue"))
        ng_port= ngrok.connect(6969, "tcp")
        your_port = ng_port.public_url
        termcolor.cprint(f"YOUR PORT: [{your_port}]","yellow")
        while True:
            port = int(input(termcolor.colored("ENTER THE CLIENT TCP PORT : ","yellow")))
            tcp_code = int(input(termcolor.colored("enter the client tcp code: ","yellow")))
            arg = [port,tcp_code]
            if auth(username,passw):
                    thread_client = Thread(target=client,args=arg)
                    thread_server = Thread(target=server)
                    thread_server.start()
                    thread_client.start()
                    thread_client.join()
                    thread_server.join()
        
                
initialize()                
          
                
                
