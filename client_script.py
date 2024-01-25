"""
The client file will do the following:
1. Binds and port and sends off request to the server
2. Connections must be unlimited number of concurrent connections
3. Client must handle errors gracefully using try-except-else-finally
4. Multi-threading will be added to allow multiple simultaneous connections
5. The program is run in a linux environment and developed as such
"""

from configparser import ConfigParser
import socket

class ServerDetailsNotFoundError(Exception):
    pass


class ClientScript:
    def __init__(self):
        pass
    
    
    def read_config(self):
        #Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")

        #Get the loginid and password
        userinfo = config_object["USERINFO"]
        my_admin = userinfo["admin"]
        my_loginid = userinfo["loginid"]
        my_pwd = userinfo["password"]
        print(f"Admin:.......{my_admin}")
        print(f"Login ID:.....{my_loginid}")
        print(f"Password:.....{my_pwd}")
        
        #Get the loginid and password
        serverinfo = config_object["SERVERCONFIG"]
        my_host = serverinfo["host"]
        my_port = serverinfo["port"]
        my_ip = serverinfo["ipaddr"]
        print(f"Hostname:.......{my_host}")
        print(f"Port ID:.....{my_port}")
        print(f"IP Address:.....{my_ip}")
        
        #Get the name of file to read
        fileloc = config_object["FILELOCATION"]
        my_filepath = fileloc["linuxpath"]
        # print("File name:.....{}".format(my_filepath))
        print(f"Path to file: {my_filepath}")
        
        return (my_ip, my_port)


    def run_client(self):
        # create a socket object
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
            [ip_server, port_server] = self.read_config()
            if ip_server == " " or port_server == " ":
                raise ServerDetailsNotFoundError(f"Couldnt load server details {ip_server}:{port_server}")
            server_ip = ip_server  # 127.0.0.1 replace with the server's IP address
            server_port = port_server  # 8000 replace with the server's port number
            # establish connection with server
            server_port = int(server_port) # ensuring the port param is integer
            client.connect((server_ip, server_port))

            while True:
                # input message and send it to the server
                # message is a string of characters like  19;0;23;26;0;19;3;0;
                # msg = input("Enter message: ")
                msg = "24;0;1;11;0;8;3;0;" # in what format is this text e.g. byte, string, 
                client.send(msg.encode("utf-8")[:1024])

                # receive message from the server
                response = client.recv(1024)
                response = response.decode("utf-8")

                # if server sent us "closed" in the payload, we break out of the loop and close our socket
                if response.lower() == "closed":
                    break

                print(f"Received: {response}")
        except ServerDetailsNotFoundError as sdnf_error:
            print(sdnf_error)
        except ConnectionResetError:  
            # adding this helped to prevent error output after text was found
            # I found this error displayed after execution had ended
            print("Connection has been reset by Server")
        else:
            pass
        finally:
            # close client socket (connection to the server)
            client.close()
            print("Connection to server closed")
        
        
    def main_client(self):

        print("----------Inside the client script----------")
        self.run_client()  


if __name__ == "__main__":
    my_client = ClientScript() # creating instance of client
    my_client.main_client()
