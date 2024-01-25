from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["USERINFO"] = {
    "admin": "Eseoghene Ovie",
    "loginid": "oveseovese",
    "password": "barracuda"
}

config_object["SERVERCONFIG"] = {
    "host": "localhost",
    "port": "8000",
    "ipaddr": "127.0.0.1"
}

# I have added a 3rd section called FILELOCATION
config_object["FILELOCATION"] = {
    "linuxpath": "./200k.txt",
    "windowspath": "200k.txt"
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)