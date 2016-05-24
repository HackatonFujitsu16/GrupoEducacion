#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 FUJITSU LABORATORIES OF EUROPE

# See __init__.py for error code description
EAPPID = 0
ESYNTX = 1
ETIMEO = 2
ESERVR = 3

import re
import httplib, urllib
import json
from base64 import b64encode
from socket import timeout
SERVER_HOST = "lod4all.net"
SERVER_PATH = "/api/search.cgi"
SERVER_PORT = 80

class Response:
    """This class handles LOD4ALL Python Library's responses and provides all
    necesary information about the data downloaded from LOD4ALL platform. Not
    intended to be instanciated outside py-lod4all, just for internal usage.

    Attributes:
        success:           Boolean depending on the execution result status.
        data:              Plain python object with the response information
                           The structure of this data follows the standard
                           SPARQL query JSON results
                           (http://www.w3.org/TR/sparql11-results-json).
        error_code:        If the attribute success is False this contains
                           the error code.
        error_description: If the attribute success is False this other one
                           contains the error description (for example an error
                           syntax explanation). It maybe an empty string, so
                           use it just for debugging purposes.
    """

    def __init__(self, success, data=None, error_text=None):
        self.success = False
        self.data = None
        self.error_code = None
        self.error_description = None

    def __str__(self):
        return str({'success':self.success,
                    'data':self.data,
                    'error_code':self.error_code,
                    'error_description':self.error_description})


class Connection:
    """Connections are objects used for interacting with LOD4ALL.

    Attributes:
        app_id:     String for your LOD4ALL application id.
        proxy_host: String with proxy host name or IP.
        proxy_port: Number of the port used for connecting with the proxy.
        proxy_user: Proxy user (if needed).
        proxy_pass: Proxy password (if needed).
    """

    def __init__(self,
        app_id='python-lib-access',
        proxy_host=None,
        proxy_port=None,
        proxy_user=None,
        proxy_pass=None):
        """Create a new connection for comunicating with LOD4ALL."""

        if type(app_id) != str:
            raise ValueError('app_id must be a string')
        if type(proxy_host) != str and proxy_host != None:
            raise ValueError('proxy_host must be a string')
        if type(proxy_port) != int and proxy_port != None:
            raise ValueError('proxy_port must be an integer')
        if type(proxy_user) != str and proxy_user != None:
            raise ValueError('proxy_user must be a string')
        if type(proxy_pass) != str and proxy_pass != None:
            raise ValueError('proxy_pass must be a string')

        if proxy_pass != None and proxy_pass <= 0:
            raise ValueError("""currently on the internet ports start from zero.
                Oh God! You should know that!""")
        if proxy_pass != None and proxy_user == None:
            raise ValueError('if you specify proxy_pass you need proxy_user')
        if proxy_user != None and (proxy_port == None or proxy_host == None):
            raise ValueError('''you need proxy_host and proxy_port if you
                want to use a proxy_user''')
        if proxy_host == None and proxy_port != None:
           raise ValueError('you cannot specify just proxy_host or proxy_port')
        if proxy_host != None and proxy_port == None:
           raise ValueError('you cannot specify just proxy_host or proxy_port')

        self.app_id = app_id
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass

    def execute_sparql(self, query):
        """Sends a SPARQL query to the server and returns a Response object
        with the results. The connection to the server is executed
        synchronously."""

        return self.__send_request__('GET', data={'query': query})

    def __send_request__(self, method, data):
        # First we check if we need to use a proxy or not
        if self.proxy_host is None or self.proxy_port is None:
            host = SERVER_HOST
            path = SERVER_PATH
            port = SERVER_PORT
        else:
            host = self.proxy_host
            path = "http://" + SERVER_HOST + SERVER_PATH
            port = self.proxy_port

        # Now we can prepare our request parameters
        response = Response(False)
        body = ""
        data['appID'] = self.app_id
        if data.get('type', None) == None:
            data['type'] = 'sparql'
        headers = {
            'Content-type': '',
            'Accept': 'application/json',
            'User-Agent': 'py-lod4all/0.1.0'
        };
        
        # If the proxy needs auth we add it to headers
        if self.proxy_user != None:
            if self.proxy_pass == None:
                auth = self.proxy_user
            else:
                auth = 'Basic ' + b64encode('%s:%s' % (
                    self.proxy_user, 
                    self.proxy_pass
                ))
            headers['proxy-authorization'] = auth

        if method == "GET":
            path = path + '?' + urllib.urlencode(data)
        elif method == "POST":
            headers['Content-type'] = 'application/x-www-form-urlencoded'
            body = urllib.urlencode(data)

        # Finally send our request
        try:
            http_connection = httplib.HTTPConnection(host, port, timeout=1000)
            http_connection.request(method, path, body, headers)
            http_response = http_connection.getresponse()
            raw_response = http_response.read()

            # And parse our nice response
            data = json.loads(raw_response)

            if data.get('message') != None:
                response.error_code = ESYNTX
                response.error_description = data.get('message')
            else:
                response.success = True
                response.data = data

            return response

        # Error parsing response (it is not a JSON)
        except ValueError:
        
            # Now we try to get the error code
            match = re.match('E([0-9]+)\:(.*)', raw_response)
            if match != None:
                error_code = match.group(1)
                response.error_description = match.group(2)
                if error_code == "0002":
                    response.error_code = ESYNTX
                elif error_code == "0003":
                    response.error_code = ETIMEO
                    response.error_description = "Timeout returned by server"
                else:
                    response.error_code = ESERVR
                    response.error_description = raw_response
            else:
                response.error_code = ESERVR
                response.error_description = raw_response
            return response

        # Error connecting to server
        except httplib.HTTPException:
            response.error_code = ESERVR
            return response

        # Connection timeout
        except timeout:
            response.error_code = ETIMEO
            return response
