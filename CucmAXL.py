# CucmAXL
# Copyright Matt Rienzo (C) 2026
# A set of python classes to work with Cisco Unified Communications Manager
# (CUCM)'s SOAP API.
#

from datetime import datetime

import csv
import io
import itertools
import logging
import re
import zeep
import zeep.transports
import requests
import base64

# ADD A INI/CFG THAT BLACKLISTS NUMBERS TO PREVENT BREAKING MAIN LINES

class AsyncCucmAXL(zeep.Client):

    def __init__(self, wsdlPath, basicPassword):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level="WARN", 
            format='%(levelname)s %(name)s %(message)s'
        )

        textBytes = text.encode('utf-8')
        base64Bytes = base64.b64encode(text_bytes)
        base64_basicPassword = base64Bytes.decode('utf-8')

        self.transport = zeep.transports.AsyncTransport(verify_ssl=False)
        self.settings = zeep.Settings(
            strict=False, 
            extra_http_headers = {
                'Authorization': (
                    'Basic '+basicPassword
                )
            }
        )

        self.client = zeep.AsyncClient(
            wsdl = wsdlPath, 
            transport = self.transport, 
            settings = self.settings
        )

    def __getattr__(self, key):
        return self.client.service[key]

    def __getitem__(self, key):
        try:
            return self.client.service._operations[key]
        except KeyError:
            raise AttributeError("Service has no operation %r" % key)

    def __iter__(self):
        return iter(self.client.service._operations.items())

    def __dir__(self):
        return list(
            itertools.chain(
                dir(super()), 
                self.client.service._operations
            )
        )





class UDSCalendar():

    def __init__(self, calendarCSVPath, basicPassword):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level = "WARN", 
            format = '%(levelname)s %(name)s %(message)s'
        )

        #// wrap in try/catch for each break point
        self.calendarCSVPath = calendarCSVPath
        self._fullCalMemory = self._read_cal_file()
        self._numbersSection = self._scan_numbers_section()
        self.logger.debug("\n\n_numbersSection:\n%s", self._numbersSection)
        self._calendarSection = self._scan_calendar_section()
        self.logger.debug("\n\n_calendarSection:\n%s", self._calendarSection)
        self._variable_map = self.ValidateNumbers()
        self.logger.debug("\n\n_variable_map = %s", repr(self._variable_map))

    def _read_cal_file(self):
        #// wrap in try/catch
        file = open(self.calendarCSVPath, mode='r')
        file_contents = file.read()
        file.close()
        self.logger.debug("\n\nfile_contents:\n%s", file_contents)
        return file_contents

    def _scan_numbers_section(self):
        return re.findall(
            r'(?s)(?<=\.numbers(?:,{31}?)\n)(.*?)(?=\.end.)', 
            self._fullCalMemory
        )

    def _scan_calendar_section(self):
        return re.findall(
            r'(?s)(?<=\.calendar(?:,{31}?)\n)(.*?)(?=\.end.)', 
            self._fullCalMemory
        )

    def ValidateNumbers(self):
        #// make sure variable cells are followed by integers only
        ref_variableMap = {}
        with io.StringIO(self._numbersSection[0]) as numCells:
            reader = csv.DictReader(numCells)
            self.processNumbers(ref_variableMap, reader)
            
        return ref_variableMap

    def processNumbers(self, ref, reader):
        for row in reader:
            self.logger.debug("ValidateNumbers() reader = %s", repr(row))

            if row['Value'].isdigit():
                ref[row['Variable']] = row['Value']
                next
            elif row['Value'] == '':
                self.logger.warn(
                    "ValidateNumbers() found an empty variable."+
                    "  Ignoring it."
                )
                next
            else:
                self.logger.warn(
                    (
                        "ValidateNumbers() variable %s is not an integer:"+
                        " %s.  Ignoring it."
                    ),
                    row['Variable'], 
                    row['Value']
                )
                next

    def TodaysNumber(self):
        with io.StringIO(self._calendarSection[0]) as dayCells:
            reader = csv.DictReader(dayCells)
        
            currentMonth = datetime.now().strftime("%B")
            currentDay = int(datetime.now().day)
            self.logger.debug(
                "TodaysNumber() %s :: %s", 
                currentMonth, 
                str(currentDay)
            )

            return self.getDayVariable(
                currentMonth, 
                currentDay, 
                reader
            )

    def getDayVariable(self, month, day, reader):
        who = ""
        for row in reader:
            if row['Month'] == month:
                who = row[str(day)]
                break

        self.logger.debug(
            "TodaysNumber() day = %s", 
            who
        )

        self.logger.debug(
            "TodaysNumber() is %s", 
            self._variable_map[who]
        )

        return self._variable_map[who]





class CucmAXL(zeep.Client):

    def __init__(self, wsdlPath, basicPassword):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level="WARN", 
            format='%(levelname)s %(name)s %(message)s'
        )
        
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning
        )

        self.setupSession()

        self.client = zeep.Client(
            wsdl = wsdlPath, 
            transport = self.transport, 
            settings = self.settings
        )

        self._basic_password = basicPassword

    def setupSession(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.verify_ssl = False

        textBytes = text.encode('utf-8')
        base64Bytes = base64.b64encode(text_bytes)
        base64_basicPassword = base64Bytes.decode('utf-8')

        self.transport = zeep.transports.Transport(session = self.session)
        self.settings = zeep.Settings(
            strict=False, 
            extra_http_headers = {
                'Authorization': (
                    'Basic '+self._basic_password
                )
            }
        )

    def __getattr__(self, key):
        return self.client.service[key]

    def __getitem__(self, key):
        try:
            return self.client.service._operations[key]
        except KeyError:
            raise AttributeError("Service has no operation %r" % key)

    def __iter__(self):
        return iter(self.client.service._operations.items())

    def __dir__(self):
        return list(
            itertools.chain(
                dir(super()), 
                self.client.service._operations
            )
        )

