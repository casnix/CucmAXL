# CucmAXL
# Copyright Matt Rienzo (C) 2026
# A set of python classes to work with Cisco Unified Communications Manager
# (CUCM)'s SOAP API.
#
# Version 0.1.0-alpha (may not work)
#   - String: can be checked with _MODULE__CucmAXL.Version()
#       Format is "MAJOR.MINOR.PATCH-RELEASE"
#   - Number (as string): can be checked with _MODULE__CucmAXL.VersionNum()
#       Format is "MAJOR.MINOR.PATCH.RELEASE" where release is represented by
#       a number.  Alpha - 0, beta - 1, gamma - 2, etc.
#   - Tuple (for logical comparisions): 
#       Can be checked with _MODULE__CucmAXL.VersionTuple()
#       Format is the same as the number value.
# Reference check for individual class version {
#   AsyncCucmAXL = version 0.1.0-alpha (may not work)
#   CucmAXL = version 0.1.0-alpha (may not work)
#   - String: can be checked with <CLASS_NAME>.Version()
#       Format is "MAJOR.MINOR.PATCH-RELEASE"
#   - Number (as string): can be checked with <CLASS_NAME>.VersionNum()
#       Format is "MAJOR.MINOR.PATCH.RELEASE" where release is represented by
#       a number.  Alpha - 0, beta - 0, gamma - 0, etc.
#   - Tuple (for logical comparisions): 
#       Can be checked with <CLASS_NAME>.VersionTuple()
#       Format is the same as the number value.
# }
#
# Individual classes may not track the module version.  Check the class version
# individually if it matters.

import zeep
import base64
import logging
import requests
import itertools
import zeep.transports

# ADD A INI/CFG THAT BLACKLISTS NUMBERS TO PREVENT BREAKING MAIN LINES

class _MODULE__CucmAXL():
    _Version = "0.1.0-alpha"
    _VersionNum = "0.1.0.0"
    _VersionTuple = (0, 1, 0, 0)

    @classmethod
    def Version(cls) -> str:
        return cls._Version
    
    @classmethod
    def VersionNum(cls) -> str:
        return cls._VersionNum
    
    @classmethod
    def VersionTuple(cls) -> tuple[int, int, int, int]:
        return cls._VersionTuple
    

class AsyncCucmAXL(zeep.Client):
    _Version = "0.1.0-alpha"
    _VersionNum = "0.1.0.0"
    _VersionTuple = (0, 1, 0, 0)
    instances = []

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

        # Make sure to update the instances count
        AsyncCucmAXL.instances.append(self)

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

    @classmethod
    def Version(cls) -> str:
        return cls._Version
    
    @classmethod
    def VersionNum(cls) -> str:
        return cls._VersionNum
    
    @classmethod
    def VersionTuple(cls) -> tuple[int, int, int, int]:
        return cls._VersionTuple


class CucmAXL(zeep.Client):
    _Version = "0.1.0-alpha"
    _VersionNum = "0.1.0.0"
    _VersionTuple = (0, 1, 0, 0)
    instances = []

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

        session = requests.Session()
        session.verify = False
        self.transport = zeep.transports.Transport(session=session)
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

        self.axlService = self.client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            targetServer
        )

        # Make sure to update the instances count
        CucmAXL.instances.append(self)

    def __getattr__(self, key):
        return self.axlService.service[key]

    def __getitem__(self, key):
        try:
            return self.axlService.service._operations[key]
        except KeyError:
            raise AttributeError("Service has no operation %r" % key)

    def __iter__(self):
        return iter(self.axlService.service._operations.items())

    def __dir__(self):
        return list(
            itertools.chain(
                dir(super()), 
                self.axlService.service._operations
            )
        )
    
    @classmethod
    def Version(cls) -> str:
        return cls._Version
    
    @classmethod
    def VersionNum(cls) -> str:
        return cls._VersionNum
    
    @classmethod
    def VersionTuple(cls) -> tuple[int, int, int, int]:
        return cls._VersionTuple
