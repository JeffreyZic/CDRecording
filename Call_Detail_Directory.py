#!/usr/bin/python
# -*- coding: utf-8 -*-
# Program: Hourly Call Reports
# Description: Reports on # of inbound
# calls from each hour of the day. Then
# averages the hours for each day
# separately.
# Date: 2/2/15
# Author: Jeffrey Zic

import re
import fileinput
import sys
import datetime
from datetime import date, timedelta
import time
import os.path
import subprocess
import getpass
import Call_Detail_Record

class Call_Detail_Directory:

    """A collection of Call_Detail_Records"""

    def __init__(self):
        """Initializes a Call_Detail_Directory.

        :param cdd: a list of Call_Detail_Records
        :type cdd: Call_Detail_Record
        """

        self.call_detail_directory = []

    def usernamePrompt(inputFunc):
        """Promt the user for a username

        :return: username
        :rtype: str
        """

        username = inputFunc
        return username

    def passwordPrompt():
        """Prompt the user for a password

        :return: password
        :rtype str
        """

        password = getpass.getpass("Password: ")
        return password

    def queryCudaTel(username,password,fname):
        """Query the CudaTel for Call Detail Records

        :param username: name of the user
        :param password: password for the user
        :type username: str
        :type password: str
        :return: response
        :rtype: file
        """

        script = """
        curl -H 'content-type: application/json' '192.168.0.199/gui/cdr/cdr?__auth_user={user}&__auth_pass={password}&sortby=end_timestamp""" +\
        """&sortorder=asc&show_outbound=0&rows=5&between=January+01+2015&between=January+01+2015&page=1' > '{fileName}'
        """
        script = script.format(user=username,password=passwords,fileName=fname)

        subprocess.call(['sh', '-c', script])

    def getLogin(self,un=usernamePrompt(raw_input("Username: ")),pwd=passwordPrompt(),fname='/log/calls'):
        """Get login information for the Cudatel Communications Server

        :return: login
        :rtype: [string,string]
        """
        state = False

        while state == False:

            username = un
            password = pwd

            queryCudaTel(username,password,fname)

            with open(fname, 'r') as f:
                line = f.readline().strip()

                # Fail state if user info is incorrect
                if line == '{"error":"FORBIDDEN"}':
                    print("Incorrect username/password.")
                    state = False
                else:
                    state = True

        return [username,passwords]

    def get_calls(
        self,
        fname,
        login,
        page,
        start_date=date.today() - timedelta(30),
        end_date=date.today() - timedelta(0)
        ):
        """Gets call metadata from file.

        get_calls is used for grabbing call metadata from files generated by the Barracuda Communications Server's
        call reporting system by the REST API in a specified date-range

        When grabbing the metadata as JSON data, the CCS will only return 10000 pieces of call metadata each time.
        For queries that return more than 10000 pieces of metadata, you must increase the page number.

        :param fname: name of call metadata file generated by the Barracuda Communications Server's
        call reporting system
        :param login: array of username and password for the CCS
        :param page: page number of the call metadata to get
        :param start_date: The first date you want to grab calls from.
        :param end_date: The last date you want to grab calls from.
        :type fname: String
        :type login: [String,String]
        :type page: int
        :type start_date: Date
        :type end_date: Date
        :returns: [count,CDR_List]
        :rtype: [int,[Call_Detail_Record]]

        :Example:

        count_calls("Sep0215")
        """

        start_diff = '3'

        fname = (date.today() - timedelta(23)).strftime('%b%d%y')
        newCall = True
        CDR_List = []
        state = False



        username = login[0]
        password = login[1]

        count=0
        script = """
        curl -H 'content-type: application/json' '192.168.0.199/gui/cdr/cdr?__auth_user={user}&__auth_pass={password}&sortby=end_timestamp""" +\
        """&sortorder=asc&show_outbound=0&rows=500000&between={first_date}&between={last_date}&page={page}' > './log/calls'
        """
        script = script.format(diff=start_diff,first_date=start_date,last_date=end_date,user=username,password=password,page=page)

        time.sleep(360) # You shouldn't poll the server more than every 5 minutes. We'll make it 6 to be sure

        subprocess.call(['sh', '-c', script])

        with open('./log/calls', 'r') as f:

            for line in f:

                # In the records, the parameters always appear in the same order so a new call is determined by
                # seeing when it reaches the last parameter in a call, then the next one will be of a new call.
                if newCall == True:
                    newCDR = Call_Detail_Record.Call_Detail_Record()
                    newCall = False

                words = line.rstrip('\n').partition(':')
                type = words[0].lstrip(' ').rstrip(' ')
                data = words[-1].rstrip(',').rstrip(' ').lstrip(' ')

                if type == '"end_timestamp"':
                    newCDR.end_timestamp = data
                    count+=1
                elif type == '"direction"':
                    newCDR.direction = data
                elif type == '"destination_name"':
                    newCDR.destination_name = data
                elif type == '"hangup_cause"':
                    newCDR.hangup_cause = data
                elif type == '"caller_id_name"':
                    newCDR.caller_id_name = data
                elif type == '"destination_type"':
                    newCDR.destination_type = data
                    CDR_List.append(newCDR)
                    newCall = True

        return [count,CDR_List]


    def readCalls(self):
        """Read call metadata from file generated by the Barracuda Communications Server

        :returns: CDR_List[]
        :rtype: Call_Detail_Record
        """

        with open('./log/calls', 'r') as f:

            newCDR = Call_Detail_Record.Call_Detail_Record()
            CDR_List = []
            newCall = False

            for line in f:

                # In the records, the parameters always appear in the same order so a new call is determined by
                # seeing when it reaches the last parameter in a call, then the next one will be of a new call.
                if newCall == True:
                    newCDR = Call_Detail_Record.Call_Detail_Record()
                    newCall = False

                words = line.rstrip('\n').partition(':')
                type = words[0].lstrip(' ').rstrip(' ')
                data = words[-1].rstrip(',').rstrip(' ').lstrip(' ')

                if type == '"end_timestamp"':
                    newCDR.end_timestamp = data
                elif type == '"direction"':
                    newCDR.direction = data
                elif type == '"destination_name"':
                    newCDR.destination_name = data
                elif type == '"hangup_cause"':
                    newCDR.hangup_cause = data
                elif type == '"caller_id_name"':
                    newCDR.caller_id_name = data
                elif type == '"destination_type"':
                    newCDR.destination_type = data
                    CDR_List.append(newCDR)
                    newCall = True

        self.call_detail_directory = CDR_List
        return CDR_List
