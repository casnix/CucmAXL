# CucmAXL
# Copyright Matt Rienzo (C) 2026
# A set of python classes to work with Cisco Unified Communications Manager
# (CUCM)'s SOAP API.
#

import zeep
import base64
import logging
import requests
import itertools
import zeep.transports

# ADD A INI/CFG THAT BLACKLISTS NUMBERS TO PREVENT BREAKING MAIN LINES

class AsyncCucmAXL(zeep.Client):
    def __init__(
            self, 
            wsdlPath: str,
            user: str, 
            password: str, 
            targetServer: str
        ):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level="WARN", 
            format='%(levelname)s %(name)s %(message)s'
        )

        basicPassword = user + ":" + password
        textBytes = basicPassword.encode('utf-8')
        base64Bytes = base64.b64encode(textBytes)
        base64_basicPassword = base64Bytes.decode('utf-8')

        self.transport = zeep.transports.AsyncTransport(verify_ssl=False)
        self.settings = zeep.Settings(
            strict=False, 
            extra_http_headers = {
                'Authorization': (
                    'Basic '+base64_basicPassword
                )
            }
        )

        self.client = zeep.AsyncClient(
            wsdl = wsdlPath, 
            transport = self.transport, 
            settings = self.settings
        )

        self.service = self.client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            targetServer
        )

    def __getattr__(self, key):
        return self.service.service[key]

    def __getitem__(self, key):
        try:
            return self.service.service._operations[key]
        except KeyError:
            raise AttributeError("Service has no operation %r" % key)

    def __iter__(self):
        return iter(self.service.service._operations.items())

    def __dir__(self):
        return list(
            itertools.chain(
                dir(super()), 
                self.service.service._operations
            )
        )


class CucmAXL(zeep.Client):
    def __init__(
            self, 
            wsdlPath: str,
            user: str, 
            password: str, 
            targetServer: str
        ):

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level="WARN", 
            format='%(levelname)s %(name)s %(message)s'
        )
        
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning
        )

        basicPassword = user + ":" + password
        textBytes = basicPassword.encode('utf-8')
        base64Bytes = base64.b64encode(textBytes)
        base64_basicPassword = base64Bytes.decode('utf-8')

        self.transport = zeep.transports.Transport(verify_ssl=False)
        self.settings = zeep.Settings(
            strict=False, 
            extra_http_headers = {
                'Authorization': (
                    'Basic '+base64_basicPassword
                )
            }
        )

        self.client = zeep.Client(
            wsdl = wsdlPath, 
            transport = self.transport, 
            settings = self.settings
        )

        self.service = self.client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            targetServer
        )

    def __getattr__(self, key):
        return self.service.service[key]

    def __getitem__(self, key):
        try:
            return self.service.service._operations[key]
        except KeyError:
            raise AttributeError("Service has no operation %r" % key)

    def __iter__(self):
        return iter(self.service.service._operations.items())

    def __dir__(self):
        return list(
            itertools.chain(
                dir(super()), 
                self.service.service._operations
            )
        )

