import socket
import http.server
from oauth2client.tools import ClientRedirectServer, ClientRedirectHandler

port_number = 0
host_name = 'localhost'
for port_number in range(8080,10000):
    try:
        httpd = ClientRedirectServer((host_name, port_number),
                                   ClientRedirectHandler)
    except ValueError as err:
        print ("socket error: " + str(err))
        pass
    else:
        print ("The server is running on: port " + str(port_number))
        print ("and host_name " + host_name)
        httpd.serve_forever()
        break