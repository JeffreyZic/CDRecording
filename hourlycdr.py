###########################################
## Program: Hourly Call Reports          ##
## Description: Reports on # of inbound  ##
## calls from each hour of the day. Then ##
## averages the hours for each day       ##
## separately.			         ##
## Date: 2/2/15				 ##
## Author: Jeffrey Zic			 ##
###########################################

import re
import fileinput
import sys
from datetime import date, timedelta
import os.path
import datetime
import re
import csv
import subprocess

<<<<<<< HEAD
#TODO: Move this to a separate file that makes use of API, not in API itself
inbound_group = ['"CCR South Front Desk"', '"Cindy Business Office"', '"Tom Back Office"', '"CCR North Front Desk"', '"CCR Workstation"', '"Nan Office Mgr"', '"Library East"', '"Doctor Workstation South"', '"Pharmacy Counter"', '"Team Leader Station"', '"Library South West"', '"Back Office North"', '"Sandi CCR TL"', '"Chris P Back Office South"', '"Tx Room West"']

class Call_Detail_Directory:
	"""A collection of Call_Detail_Records"""
	
	def __init__(self):
		"""Initializes a Call_Detail_Directory.
		
		:param cdd: a list of Call_Detail_Records
		:type cdd: Call_Detail_Record
		"""
		
		self.call_detail_directory = []
	
	def get_calls(self, fname, start_date=date.today() - timedelta(1), end_date=date.today() - timedelta(1)):
		"""Gets call metadata from file.
		
		count_calls is used for grabbing call metadata from files generated by the Barracuda Communications Server's
		call reporting system by the REST API in a specified date-range
		
		:param fname: name of call metadata file generated by the Barracuda Communications Server's
		call reporting system
		:param start_date: The first date you want to grab calls from.
		:param end_date: The last date you want to grab calls from.
		:type fname: String
		:type start_date: Date
		:type end_date: Date
		:returns: CDR_List[]
		:rtype: Call_Detail_Record
		
		:Example:
		
		count_calls("Sep0215")
		"""
		start_diff = "3"
		script = 'NOW=$(date -d "' + start_diff  + 'day ago" +"%B")\r'
		script += 'CurrentMonth=$(date -d "' + start_diff  + 'day ago" +"%B")\r'
		script +=' CurrentDay=$(date -d "' + start_diff  + 'day ago" +"%B")\r'
		script += ' CurrentYear=$(date -d "' + start_diff  + 'day ago" "+%B")\r'
		script += """ cd "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly"
		
		curl -H 'content-type: application/json' "192.168.0.199/gui/cdr/cdr?__auth_user=" + user + "&__auth_pass=" + pass + "&sortby=end_timestamp&sortorder=asc&since=RANGE&rows=500000&between=June+01%2C+2015&between=November+01%2C+2015&show_outbound=0 > "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly_development/CDR/calls"
		"""
		
		fname = (date.today() - timedelta(23)).strftime("%b%d%y")
		newCall = True
		CDR_List = []

		subprocess.call(['sh', '-c', script])
	
		with open("./CDR/calls",'r') as f:
			
			for line in f:
				
				if newCall == True: 
					newCDR = Call_Detail_Record() 
					newCall = False
					# In the records, the parameters always appear in the same order so a new call is determined by
					# seeing when it reaches the last parameter in a call, then the next one will be of a new call.
					
				words = line.rstrip('\n').partition(":")
				type = words[0].lstrip(' ').rstrip(' ')
				data = words[-1].rstrip(',').rstrip(' ').lstrip(' ')
				
				if (type == "\"end_timestamp\""):
					newCDR.end_timestamp = data
				elif (type == '"direction"'):
					newCDR.direction = data
				elif (type == '"destination_name"'):
					newCDR.destination_name = data
				elif (type == '"hangup_cause"'):
					newCDR.hangup_cause = data
				elif (type == '"caller_id_name"'):
					newCDR.caller_id_name = data
				elif (type == '"destination_type"'):
					newCDR.destination_type = data
					CDR_List.append(newCDR)
					newCall = True
				
		self.call_detail_directory = CDR_List		
		return 	CDR_List

class Call_Detail_Record:
	""" Call Detail Records contain metadata for phone calls."""
	
	def __init__(self):
                self.bbx_cdr_id = "",
                self.network_addr = "",
                self.bbx_fax_inbound_id = "" ,
                self.billsec = "",
                self.original_callee_id_name = "",
                self.end_timestamp = "",
                self.direction = "",
                self.destination_name = "",
                self.transfer_source = "",
                self.original_callee_id_number = "",
                self.write_rate = "",
                self.transfer_to = "",
                self.write_codec = "",
                self.context = "",
                self.callee_bbx_phone_id = "",
                self.destination_number = "",
                self.caller_id_number = "",
                self.caller_bbx_phone_registration_id = "",
                self.hangup_cause = "",
                self.original_caller_id_number = "",
                self.gateway_name = "",
                self.record_file_name = "",
                self.callee_bbx_user_id = "",
                self.record_file_checksum = "",
                self.caller_bbx_phone_id = "",
                self.duration = "",
                self.callee_bbx_phone_registration_id = "",
                self.answer_timestamp = "",
                self.hangup_originator = "",
                self.transfer_history = "",
                self.call_type = "",
                self.source_table = "",
                self.bbx_queue_id = "",
                self.hold_events = "",
                self.start_timestamp = "",
                self.uuid = "",
                self.record_keep_days = "",
                self.bbx_fax_outbound_id = "",
                self.bleg_uuid = "",
                self.bbx_callflow_id = "",
                self.destination_list = "",
                self.caller_id_name = "",
                self.click_to_call_uuid = "",
                self.read_rate = "",
                self.original_caller_id_name = "",
                self.recording_retention = "",
                self.caller_bbx_user_id = "",
                self.destination_type = "",
                self.outbound_route = "",
                self.processed= "",
                self.accountcode = "",
                self.read_codec = ""
		
class Call_Counter:
	"""Counts the number of true calls"""
	
	def __init__(self, counts = [0]*24):
		"""Initializes a Call_Counter.
		
		:param counts: A list of counted calls for each hour of a day.
		:param daily_counts: A count of calls by the hour, divided by the day
		:type counts: int[]
		:type daily_counts: dict
		"""
		
		self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	
		self.hourly_counts = {
								"Monday" : [0]*24,
								"Tuesday" : [0]*24,
								"Wednesday" : [0]*24,
								"Thursday" : [0]*24,
								"Friday" : [0]*24,
								"Saturday" : [0]*24,
								"Sunday" : [0]*24}
								
		self.hourly_averages = {
								"Monday" : [0]*24,
								"Tuesday" : [0]*24,
								"Wednesday" : [0]*24,
								"Thursday" : [0]*24,
								"Friday" : [0]*24,
								"Saturday" : [0]*24,
								"Sunday" : [0]*24}
								
		self.daily_averages = {
								"Monday" : 0,
								"Tuesday" : 0,
								"Wednesday" : 0,
								"Thursday" : 0,
								"Friday" : 0,
								"Saturday" : 0,
								"Sunday" : 0}
								
	def count_days_of_week(self,calls,start_date= None,end_date=None):
		"""Counts the number of each day of the week in a date range.
		
		This will count the number of each days of the week in a date range (e.g. number of mondays, tuesdays, etc.).
		You can either provide a Call Detail Directory and it will use the range of dates in that, or specify the date range
		yourself. Specifying a Call Detail Directory will override specified date ranges.
		
		:param call: An optional list of calls to count the days of week in.
		:param start_date: An optional date to use as the beginning of your range.
		:param end_date: An optional  date to use as the end of your range.
		:type calls: Call_Detail_Directory
		:type start_date: date
		:type end_date: date
		:return days_of_week_count
		:rtype dict
		"""
		
		days_of_week_count = {
								"Monday" : 0,
								"Tuesday" : 0,
								"Wednesday" : 0,
								"Thursday" : 0,
								"Friday" : 0,
								"Saturday" : 0,
								"Sunday" : 0}
		
		if (calls):
			start_date = (calls.call_detail_directory[0].end_timestamp.split(" "))[0]
			end_date = (calls.call_detail_directory[-1].end_timestamp.split(" "))[0]
		
		current_date = start_date.split("-")
		current_date = date(int(current_date[0].lstrip('"')),int(current_date[1]),int(current_date[2]))
		
		end_date = date(int(end_date[1:5]),int(end_date[6:8]),int(end_date[9:]))
		
		while current_date <= end_date:
			days_of_week_count[self.weekdays[current_date.weekday()]] += 1
			current_date = current_date + timedelta(1)
			
		return days_of_week_count
	
	def count_calls(self,calls):
		"""Counts the amount of real calls in a directory.
		
		This counts the amount of real calls in a directory. When grabbing calls from Barracuda Communications Server
		there will be erroneous records due to each ringing phone being counted, transfers, call-parking, etc. Inbound calls
		will always have a "direction" equal to "inbound", which sounds obvious however calls that are transferred around 
		an office or intra-office calls tend to show up and won't be listed as "inbound". The hangup cause also won't be
		listed as a transfer or something else and only phones in the inbound_group can be taking inbound calls.
		
		:param calls: List of the calls you are counting
		:type calls: Call_Detail_Directory
		:returns hourly_counts
		:rtype int[]
		"""
		
		for call in calls:
			
			if (call.direction == '"inbound"') and ((call.hangup_cause == '"NORMAL_CLEARING"') or (call.hangup_cause == '"NONE"')) and (call.destination_type != "internal") and (not call.caller_id_name in inbound_group) and (call.destination_name in inbound_group): #Filtering out any calls in the inbound group so we don't count any intra-office calls
				
				call_date = call.end_timestamp.split('-')
				
				day_of_week = date(int(call_date[0].lstrip('"')),int(call_date[1]),int(call_date[2][:2])).weekday()
				self.hourly_counts[self.weekdays[day_of_week]][int(call.end_timestamp.split()[1][:2])] += 1

		return self.hourly_counts
		
	def avg_calls_per_hour(self,calls):
		"""Finds the average amount of calls for each day of the week divided by hour.
		
		Takes a call directory and finds the average number of calls divided by day of the week by the hour.
		
		:param call_directory: list of call detail records to average
		:type call_directory: Call_Detail_Directory
		:returns daily_averages
		:rtype dict
		"""
			
		num_days_of_week = self.count_days_of_week(calls)
		self.count_calls(calls.call_detail_directory)	
		for i in self.weekdays:
			for hour in range(24):
				if num_days_of_week[i] != 0:
					self.hourly_averages[i][hour] = self.hourly_counts[i][hour] / num_days_of_week[i]
				else:
					self.hourly_averages[i][hour] = 0
			
		return self.hourly_averages
		
	def avg_calls_per_day(self,calls):
=======
fname = sys.stdin.readlines() # Receives from stdin, built to work with cdr.sh


#TODO: Move this to a separate file that makes use of API, not in API itself
inbound_group = ['"CCR South Front Desk"', '"Cindy Business Office"', '"Tom Back Office"', '"CCR North Front Desk"', '"CCR Workstation"', '"Nan Office Mgr"', '"Library East"', '"Doctor Workstation South"', '"Pharmacy Counter"', '"Team Leader Station"', '"Library South West"', '"Back Office North"', '"Sandi CCR TL"', '"Chris P Back Office South"', '"Tx Room West"']

class Call_Detail_Directory:
	"""A collection of Call_Detail_Records"""
	
	def __init__(self, cdd = []):
		"""Initializes a Call_Detail_Directory.
		
		:param cdd: a list of Call_Detail_Records
		:type cdd: Call_Detail_Record
		"""
		
		self.call_detail_directory = cdd
	
	def get_calls(start_date=date.today() - timedelta(1), end_date=date.today() - timedelta(1)):
		"""Gets call metadata from file.
		
		count_calls is used for grabbing call metadata from files generated by the Barracuda Communications Server's
		call reporting system by the REST API in a specified date-range
		
		:param start_date: The first date you want to grab calls from.
		:param end_date: The last date you want to grab calls from.
		:type start_date: Date
		:type end_date: Date
		:returns: CDR_List[]
		:rtype: Call_Detail_Record
		
		:Example:
		
		count_calls("Sep0215")
		"""
		
		script = """
		NOW=$(date -d "1 day ago" +"%b%d%y")
		CurrentMonth=$(date -d "1 day ago" +"%B")
		CurrentDay=$(date -d "1 day ago" +"%-d")
		CurrentYear=$(date -d "1 day ago" +"%Y")

		cd "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly"

		curl -H 'content-type: application/json' "192.168.0.199/gui/cdr/cdr?__auth_user=admin&__auth_pass=c^c\$g%o)d&sortby=end_timestamp&sortorder=desc&since=RANGE&rows=2000&between=${CurrentMonth}+${CurrentDay}%2C+${CurrentYear}&between=${CurrentMonth}+${CurrentDay}%2C+${CurrentYear}&show_outbound=0" > "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly/CDR/$NOW"
		"""		
		
		newCall = True
		CDR_List = []

		subprocess.call(['sh', '-c', script])
		
		with open(fname,'r') as f:
		
			for line in f:
				
			if newCall == True: 
				newCDR = Call_Detail_Record() 
				newCall = False
				# In the records, the parameters always appear in the same order so a new call is determined by
				# seeing when it reaches the last parameter in a call, then the next one will be of a new call.
				
			words = line.rstrip('\n').partition(":")
			type = words[0].lstrip(' ').rstrip(' ')
			data = words[-1].rstrip(',').rstrip(' ').lstrip(' ')
			
			if (type == "\"end_timestamp\""):
				newCDR.end_timestamp = data
			elif (type == '"direction"'):
				newCDR.direction = data
			elif (type == '"destination_name"'):
				newCDR.destination_name = data
			elif (type == '"hangup_cause"'):
				newCDR.hangup_cause = data
			elif (type == '"caller_id_name"'):
				newCDR.caller_id_name = data
			elif (type == '"destination_type"'):
				newCDR.destination_type = data
				CDR_LIST.append(newCDR)
				newCall = True
				
		self.call_detail_directory = CDR_LIST		
		return 	CDR_LIST

class Call_Detail_Record:
	""" Call Detail Records contain metadata for phone calls."""
	
	def __init__(self):
		self.bbx_cdr_id = "",
        self.network_addr = "",
        self.bbx_fax_inbound_id = "" ,
        self.billsec = "",
        self.original_callee_id_name = "",
        self.end_timestamp = "",
        self.direction = "",
        self.destination_name = "",
        self.transfer_source = "",
        self.original_callee_id_number = "",
        self.write_rate = "",
        self.transfer_to = "",
        self.write_codec = "",
        self.context = "",
        self.callee_bbx_phone_id = "",
        self.destination_number = "",
        self.caller_id_number = "",
        self.caller_bbx_phone_registration_id = "",
        self.hangup_cause = "",
        self.original_caller_id_number = "",
        self.gateway_name = "",
        self.record_file_name = "",
        self.callee_bbx_user_id = "",
        self.record_file_checksum = "",
        self.caller_bbx_phone_id = "",
        self.duration = "",
        self.callee_bbx_phone_registration_id = "",
        self.answer_timestamp = "",
        self.hangup_originator = "",
        self.transfer_history = "",
        self.call_type = "",
        self.source_table = "",
        self.bbx_queue_id = "",
        self.hold_events = "",
        self.start_timestamp = "",
        self.uuid = "",
        self.record_keep_days = "",
        self.bbx_fax_outbound_id = "",
        self.bleg_uuid = "",
        self.bbx_callflow_id = "",
        self.destination_list = "",
        self.caller_id_name = "",
        self.click_to_call_uuid = "",
        self.read_rate = "",
        self.original_caller_id_name = "",
        self.recording_retention = "",
        self.caller_bbx_user_id = "",
        self.destination_type = "",
        self.outbound_route = "",
        self.processed= "",
        self.accountcode = "",
        self.read_codec = ""
		
class Call_Counter
	"""Counts the number of true calls"""
	
	def __init__(self, counts = [0]*24):
		"""Initializes a Call_Counter.
		
		:param counts: A list of counted calls for each hour of a day.
		:param daily_counts: A count of calls by the hour, divided by the day
		:type counts: int[]
		:type daily_counts: dict
		"""
	
		self.daily_counts = {
								"Monday" : [0]*24,
								"Tuesday" : [0]*24,
								"Wednesday" : [0]*24,
								"Thursday" : [0]*24,
								"Friday" : [0]*24,
								"Saturday" : [0]*24,
								"Sunday" : [0]*24}
								
		self.hourly_averages = {
								"Monday" : [0]*24,
								"Tuesday" : [0]*24,
								"Wednesday" : [0]*24,
								"Thursday" : [0]*24,
								"Friday" : [0]*24,
								"Saturday" : [0]*24,
								"Sunday" : [0]*24}
								
		self.daily_averages = {
								"Monday" : 0,
								"Tuesday" : 0,
								"Wednesday" : 0,
								"Thursday" : 0,
								"Friday" : 0,
								"Saturday" : 0,
								"Sunday" : 0}
								
	def count_days_of_week(calls= None,start_date= None,end_date=None):
		"""Counts the number of each day of the week in a date range.
		
		This will count the number of each days of the week in a date range (e.g. number of mondays, tuesdays, etc.).
		You can either provide a Call Detail Directory and it will use the range of dates in that, or specify the date range
		yourself. Specifying a Call Detail Directory will override specified date ranges.
		
		:param call: An optional list of calls to count the days of week in.
		:param start_date: An optional date to use as the beginning of your range.
		:param end_date: An optional  date to use as the end of your range.
		:type calls: Call_Detail_Directory
		:type start_date: date
		:type end_date: date
		:return days_of_week_count
		:rtype dict
		"""
		
		self.days_of_week_count = {
								"Monday" : 0,
								"Tuesday" : 0,
								"Wednesday" : 0,
								"Thursday" : 0,
								"Friday" : 0,
								"Saturday" : 0,
								"Sunday" : 0}
		
		if calls != None:
			start_date = (calls.call_detail_directory[0].end_timestamp.split(" "))[0]
			end_date = (calls.call_detail_directory[1].end_timestamp.split(" "))[0]
			
		current_date = start_date.split("-")
		current_date = date(current_date[0],current_date[1]current_date[3])
		
		
		while current_date != start_date:
			days_of_week_count[(current_date).weekday()] += 1
			current_date = current_date + timedelta(1)
			
		return days_of_week_count
	
	def count_calls(calls):
		"""Counts the amount of real calls in a directory.
		
		This counts the amount of real calls in a directory. When grabbing calls from Barracuda Communications Server
		there will be erroneous records due to each ringing phone being counted, transfers, call-parking, etc. Inbound calls
		will always have a "direction" equal to "inbound", which sounds obvious however calls that are transferred around 
		an office or intra-office calls tend to show up and won't be listed as "inbound". The hangup cause also won't be
		listed as a transfer or something else and only phones in the inbound_group can be taking inbound calls.
		
		:param calls: List of the calls you are counting
		:type calls: Call_Detail_Directory
		:returns hourly_counts
		:rtype int[]
		"""
		
		weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

		for call in calls:
			
			if (call.direction == '"inbound"') and ((call.hangup_cause == '"NORMAL_CLEARING"') or (call.hangup_cause == '"NONE"')) and (not call.caller_id_name in inbound_group): #Filtering out any calls in the inbound group so we don't count any intra-office calls
				
				call_date = call.end_timestamp.split('-')
				
				day_of_week = date(call_date[0],call_date[1],call_date[2]).weekday()
				daily_count[day_of_week][int(call.end_timestamp.split()[1][:2])] += 1

		return hourly_counts
		
	def avg_calls_per_hour(calls):
		"""Finds the average amount of calls for each day of the week divided by hour.
		
		Takes a call directory and finds the average number of calls divided by day of the week by the hour.
		
		:param call_directory: list of call detail records to average
		:type call_directory: Call_Detail_Directory
		:returns daily_averages
		:rtype dict
		"""
		
		weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
					
		num_days_of_week = count_days_of_week(calls)
			
		for i in weekdays:
			
			self.hourly_averages[i] = self.daily_counts[i] / num_days_of_week[i]
			
		return self.hourly_averages
		
	def avg_calls_per_day(calls):
>>>>>>> origin/master
		"""Finds the average amount of calls for each day of the week
		
		Takes a call directory and finds the average number of calls divided by day of the week.
		
		:param call_directory: list of call detail records to average
		:type call_directory: Call_Detail_Directory
		:returns daily_averages
		:rtype dict
		"""
		
<<<<<<< HEAD
		num_days_of_week = self.count_days_of_week(calls)
			
		for i in self.weekdays:
			daily_counts = sum(self.hourly_counts[i])
			self.daily_averages[i] = daily_counts / num_days_of_week[i]
			
		return self.daily_averages

	def hourly_avg_calls_output(self,averages):
		"""Outputs the average calls divided by hour into a file
=======
		weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
					
		num_days_of_week = count_days_of_week(calls)
			
		for i in weekdays:
			
			self.hourly_averages[i] = self.daily_counts[i] / num_days_of_week[i]
			
		return self.hourly_averages

		#TODO: This needs to be turned into a separate output method, that ideally can output in different formats.
		# if not os.path.isfile("./Reports/Averages"): #if the file to store the data doesn't exist we need to create it with correct formatting
				
			# for day in weekdays:
				
				# with open("./Reports/Averages", 'a') as f:
					# f.write(day + '\n')
					# count = 0
					# while count < 24:
						# f.write(str(count).zfill(2) + " : -\n") #If a lines are marked with a dash that means the program has never been run for that day
						# count += 1
					# f.write("\n")
				
		# for day in range(7):
			# dailyAvgs.append([])
			# with open("./Daily/" + weekdays[int(day)], 'r') as f, open("./Reports/tempavg", 'w') as o:
			
				# pastAvg = [None] * 24
				# foundHour = 0
				# count = 1
				
				# for hour in range(24):
					# for line in f:
					
						# if line != "\n":
							# nums = line.rstrip('\n').split(":")
						
						# if nums[0] == str(hour):
							# indvHrs[day][hour].append(int(nums[1]))
							
						# foundHour = 0
					# f.seek(0)
			
			# for hourlycalls in indvHrs[day]:
					
				# dailyAvgs[day].append(int(sum(hourlycalls) / len(hourlycalls)))
			
		# with open("./Reports/Averages", 'w') as f:
			# for day in range(7):
				# f.write(weekdays[day] + "\n")
				
				# for hour in range(24):
					# f.write(str(hour) + " : " + str(dailyAvgs[day][hour]) + '\n')
				# f.write('\n')
	
	# def daily_calls_output():
		# """Outputs the call counts into a file"""
		
		# weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		# yesterdayDate = date.today() - timedelta(1)
			
		# with open("./Daily/" + weekdays[yesterdayDate.weekday()], 'a') as f:
		
			# f.write(str(yesterdayDate)[:10] + ": \n")
			# for i in range(24):
				# f.write(str(i) + ": " + str(hourlycounts[i]) + "\n")
			# f.write("\n")
			
	def avg_calls_output(averages):
		"""Outputs the average calls into a file
>>>>>>> origin/master
		
		:param averages: list of average call divided by day of the week and hour
		:type averages: int[][]
		"""
	
<<<<<<< HEAD
		with open("houlry_averages.csv", 'wb') as csvfile:
			avgs_writer = csv.writer(csvfile, dialect="excel")
			avgs_writer.writerow([""] + self.weekdays)
			
			for hour in range(24):
				daily_hours = []
				for day in self.weekdays:
					daily_hours.append(self.hourly_averages[day][hour])
				hour_str = str(hour) + ": "
				avgs_writer.writerow([hour_str] + daily_hours)
				
	def daily_avg_calls_output(self,averages):
		"""Outputs the average calls divided by day into a file
		
		:param averages: list of average call divided by day of the week and hour
		:type averages: int[]
		"""
		
		with open("dailiy_averages.csv", 'wb') as csvfile:
			avgs_writer = csv.writer(csvfile, dialect="excel")
			avgs_writer.writerow(self.weekdays)
			
			daily = []
			for day in self.weekdays:
				daily.append(self.daily_averages[day])
			avgs_writer.writerow(daily)
			
	def total_calls_output(self,totals):
		"""Outputs the total calls divided by hour into a file
			
		:param totals: list of total calls divided by hour
		:type totals: int[][]
		"""
		
		with open("totals.csv", 'wb') as csvfile:
			avgs_writer = csv.writer(csvfile, dialect="excel")
			avgs_writer.writerow([""] + self.weekdays)
			
			for day in self.weekdays:
				for hour in range(24):
					avgs_writer.writerow([hour + ": " +  [hourly_averages[day][hour]]])
			
=======
		with open("averages.csv", 'w', newline="") as csvfile:
			avgs_writer = csv.writer(csvfile, dialect="excel")
			
		
def transferF(old, new):
# for replacing a file of the same name
	os.remove(new)
	os.rename(old, new)
	
>>>>>>> origin/master
def main():	
	test = Call_Detail_Directory()
	test.get_calls("test")
	count = Call_Counter()
	count.count_days_of_week(test)
	count.avg_calls_per_hour(test)
	count.avg_calls_per_day(test)
	count.daily_avg_calls_output(count.hourly_averages)
	count.hourly_avg_calls_output(count.hourly_averages)
	
if __name__ == "__main__":
	main()
