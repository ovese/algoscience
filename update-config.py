from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

#Get the USERINFO section
userinfo = config_object["USERINFO"]

#Update the password
userinfo["password"] = "barracuda"

#Update admin
userinfo["admin"] = "Ese Ovie"

#Write changes back to file
with open('config.ini', 'w') as conf:
    config_object.write(conf)