from server_script import ServerScript
from client_script import ClientScript


"""
In the main file,
run the server first and then run the client

"""
def main():
    my_server = ServerScript(" ") # creating instance of server
    my_client = ClientScript() # creating instance of client
    [ret_ip, ret_port, ret_file_read] = my_server.read_config()
    [ret_file_data, ret_file_data_list] = my_server.read_file_contents(ret_file_read)
    print("----------Printing contents of file 200k.txt----------")
    print(f"Length of returned file line read: {len(ret_file_data)}")
    print(f"Length of returned data list: {len(ret_file_data_list)}")
    
    #print(ret_file_data)
    #print(ret_file_data_list)
    
    my_server.establish_conn_server()
    my_client.run_client()    
    
    
if __name__ == "__main__":
    main()
    
    
    