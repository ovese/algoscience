"""
The server file will do the following:
1. Binds and port and responds to connections
2. Connections must be unlimited number of concurrent connections
3. string is sent in the connection in clear text
4. the clear text points to the location where the file to be read is kept or referenced
5. Location of file is given in configuration file
6. Config file can be ini or yaml file type
7. The config file is necesary to avoid hardcoded data that have to be loaded at start of program
8. I have used an ini file which is creatd by the code file create-config.py
9. Another file to update the config file is update-config.py
10. I have used try-except-else-finally block to handle errors
11. Multithreading will be added subsequently
13. The program is run in a linux environment
"""
from configparser import ConfigParser
import socket
import os

class ServerScript:
    def __init__(self, str_text):
        self.str_text = str_text
        # 19;0;23;26;0;19;3;0;
        
        
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
        
        return (my_ip, my_port, my_filepath)
    
    
    def read_file_contents(self, path_to_file):
            try:
                data_list = []
                # remove absolute path if there is
                # filename = os.path.basename(path_to_file)
                with open(path_to_file, "r") as data_file:
                    if not data_file:
                        print("File cant be read")
                    else:
                        print("File opened and wil be read")
                        data_from_file = data_file.read().split("\n")
                        # the line above automatically creates a list from the data_file read
            except FileNotFoundError:
                print("File not found error")
            except FileExistsError:
                print("File does not exist error")
            else:
                for i in range(len(data_from_file)):
                    data_list.append(data_from_file[i])
            finally:
                print("File contents read and will be returned")
                
            return (data_from_file, data_list)
        
    
    def match_text(self, str_to_match,list_to_search):
        """
        This method takes the string to serach for and
        the PROCESSED list of items to search against
        """
        matched = False
        count = 0
        target_str = str_to_match
        for item in range(len(list_to_search)):
            if list_to_search[item] == target_str:
                # print("Text FOUND")
                matched = True
                break
            else:
                # print("Text NOT FOUND")
                matched = False
            count += 1
                
        return (count,matched)     
        
        
    def establish_conn_server(self):
        """
        Steps to take are:
        1. establish the server param details from config file
        2. 
        """
        # load some para,ms from config file
        [server_ip, port_num, file_path] = self.read_config()
        # create or instantiate a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # bind the socket object to an ip address or port
        port_num = int(port_num)
        server.bind((server_ip, port_num)) # this takes an integer as port number
        
        # listen for incoming connections
        server.listen(0)
        print(f"Listening on {server_ip}:{port_num}")
        
        # accept incoming connections ****** coming from CLIENT
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
                
        # receive data from the client
        while True:
            request = client_socket.recv(1024)
            request = request.decode("utf-8") # convert bytes to string
            
            # if we receive "close" from the client, then we break
            # out of the loop and close the conneciton
            if request.lower() == "close":
                # send response to the client which acknowledges that the
                # connection should be closed and break out of the loop
                client_socket.send("closed".encode("utf-8"))
                break
            else:
                print(f"Received: {request}")
            #print(f"Received: {request}")
                # sending response back to client
                response = "accepted".encode("utf-8") # convert string to bytes
                # convert and send accept response to the client
                client_socket.send(response)
                
                # check if it finds the sent text or request
                [ret_ip, ret_port, ret_file_read] = self.read_config()
                [ret_file_data, ret_file_data_list] = self.read_file_contents(ret_file_read)
                
                [counter, verdict] = self.match_text(request, ret_file_data)
                # use returned boolean to print verdict
                if verdict == True:
                    print(f"At line {counter} Text {request} FOUND")
                    break
                else:
                    if counter == len(ret_file_data):
                        print(f"At line {counter} Text {request} NOT FOUND")
                        break 
                    #break
                    # see the location of the break command above
                    # i discovered any one works just as fine       
        
        # freeing resources
        # close connection socket with the client
        client_socket.close()
        print("Connection to client closed")
        # close server socket
        server.close()
        
        
    def main_server(self):
        [ret_ip, ret_port, ret_file_read] = self.read_config()
        [ret_file_data, ret_file_data_list] = self.read_file_contents(ret_file_read)
        print("----------Printing contents of file 200k.txt----------")
        print(f"Length of returned file line read: {len(ret_file_data)}")
        print(f"Length of returned data list: {len(ret_file_data_list)}")
        
        #print(ret_file_data)
        #print(ret_file_data_list)
        
        self.establish_conn_server()
        
if __name__ == "__main__":
    my_server = ServerScript(" ") # creating inst ance of server
    my_server.main_server()

    

                
        


