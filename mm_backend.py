# all imports
import copy
import json
from datetime import datetime
import webbrowser




# common classes and functions
def json_to_dict():
	with open("resources\\meetings.json") as read_file:
		json_dict = json.load(read_file)
	return (json_dict["additional_info"], json_dict["credits"], json_dict["meetings"])


class Holder:
	additional_info, credits, meetings = json_to_dict()


def dict_to_json():
	with open("resources\\meetings.json", "w") as write_file:
		json.dump({"additional_info": Holder.additional_info, "credits": Holder.credits, "meetings": Holder.meetings}, write_file, indent=4)
	return "Done"

	
def weekday_to_number(weekday):
	if weekday == "Mon":
		return 0
	elif weekday == "Tue":
		return 1
	elif weekday == "Wed":
		return 2
	elif weekday == "Thurs":
		return 3
	elif weekday == "Fri":
		return 4
	elif weekday == "Sat":
		return 5
	else:
		return 6




# Add meetings functions
def add_meeting(category, meeting_id, passcode, meeting_link, meeting_organizer, meeting_subject, timestamp):
	if category == "onetime":
		year, month, day, hour, minute = timestamp
		time = f"{year}-{month}-{day}, {hour}:{minute}"
	elif category == "weekly":
		weekday, hour, minute = timestamp
		time = f"{weekday}, {hour}:{minute}"
	else:
		hour, minute = timestamp
		time = f"{hour}:{minute}"

	new_entry_dict = dict()
	new_entry_dict["category"] = category
	new_entry_dict["time"] = time
	new_entry_dict["meeting_id"] = meeting_id
	new_entry_dict["passcode"] = passcode
	new_entry_dict["meeting_link"] = meeting_link
	new_entry_dict["meeting_organizer"] = meeting_organizer
	new_entry_dict["meeting_subject"] = meeting_subject
	new_entry_dict["active"] = True
	meetings = Holder.meetings
	meetings.append(new_entry_dict)
	Holder.meetings = meetings
	dict_to_json()

	return "Meeting Added"




# Search functions 
def show_all_meetings(queries):
	new_queries = {}
	for key, value in queries.items():
		if value != "all":
			new_queries[key] = value

	temporary_meetings = []
	meetings = Holder.meetings
	if "organizer" in new_queries.keys():
		for meeting in meetings:
			if meeting["meeting_organizer"] == new_queries["organizer"]:
				temporary_meetings.append(meeting)
	if "subject" in new_queries.keys():
		for meeting in meetings:
			if meeting["meeting_subject"] == new_queries["subject"]:
				temporary_meetings.append(meeting)
	if "weekday" in new_queries.keys():
		for meeting in meetings:
			if (meeting["category"] == "weekly") and (new_queries["weekday"] in meeting["time"]):
				temporary_meetings.append(meeting)
			if (meeting["category"] == "daily"):
				temporary_meetings.append(meeting)
			if (meeting["category"] == "onetime") and (new_queries["weekday"] == datetime.strftime(datetime.strptime(meeting["time"], "%Y-%m-%d, %H:%M"), "%a")):
				temporary_meetings.append(meeting)
	if "date" in new_queries.keys():
		for meeting in meetings:
			if new_queries["date"] in meeting["time"]:
				temporary_meetings.append(meeting)
			if meeting["category"] == "daily":
				temporary_meetings.append(meeting)
	if len(new_queries.keys()) == 0:
		temporary_meetings = copy.deepcopy(meetings)

	for meeting in temporary_meetings:
		if meeting["active"] == False:
			temporary_meetings.remove(meeting)

	return temporary_meetings


def show_upcoming_meetings(meeting_range):
	temporary_meetings = []
	meetings = Holder.meetings

	# 30 minutes and 2 hours will be double-sided
	if meeting_range == "30 Minute":
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if (int(time_diff.days) <= 1 or int(time_diff_reverse.days) <= 1) \
				and (int(time_diff.seconds) <= 1800 or int(time_diff_reverse.seconds) <= 1800):
					temporary_meetings.append(meeting)
			elif meeting["category"] == "weekly":
				temp_time = datetime.strptime(meeting["time"], format="%a, %H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if ((str(temp_time)[:3]) == datetime.now().strftime(fmt = "%a")) or abs(weekday_to_number(str(temp_time)[:3]) - datetime.weekday(datetime.now()) <= 1) \
				and (int(time_diff.seconds) <= 1800 or int(time_diff_reverse.seconds) <= 1800):
					temporary_meetings.append(meeting)
			else:
				temp_time = datetime.strptime(meeting["time"], format="%H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if (int(time_diff.seconds) <= 1800 or int(time_diff_reverse.seconds) <= 1800):
					temporary_meetings.append(meeting)

	elif meeting_range == "2 Hour":
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if (int(time_diff.days) <= 1 or int(time_diff_reverse.days) <= 1) \
				and (int(time_diff.seconds) <= 7200 or int(time_diff_reverse.seconds) <= 7200):
					temporary_meetings.append(meeting)
			elif meeting["category"] == "weekly":
				temp_time = datetime.strptime(meeting["time"], format="%a, %H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if ((str(temp_time)[:3] == datetime.now().strftime(fmt = "%a")) or abs(weekday_to_number(str(temp_time)[:3]) - datetime.weekday(datetime.now()) <= 1))\
				and (int(time_diff.seconds) <= 7200 or int(time_diff_reverse.seconds) <= 7200):
					temporary_meetings.append(meeting)
			else:
				temp_time = datetime.strptime(meeting["time"], format="%H:%M")
				time_diff = temp_time - datetime.now()
				time_diff_reverse = datetime.now() - temp_time
				if (int(time_diff.seconds) <= 7200 or int(time_diff_reverse.seconds) <= 7200):
					temporary_meetings.append(meeting)

	elif meeting_range == "Today":
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				if str(temp_time)[:10] == str(datetime.now())[:10]:
					temporary_meetings.append(meeting)
			elif meeting["category"] == "weekly":
				temp_time = datetime.strptime(meeting["time"], format="%a, %H:%M")
				if str(temp_time)[:3] == datetime.now().strftime(fmt = "%a"):
					temporary_meetings.append(meeting)
			else:
				temporary_meetings.append(meeting)

	elif meeting_range == "Tomorrow":
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				if (str(temp_time)[:7] == str(datetime.now())[:7]) and (int(str(temp_time)[8:10]) - 1 == int(str(datetime.now())[8:10])):
					temporary_meetings.append(meeting)
			elif meeting["category"] == "weekly":
				temp_time = datetime.strptime(meeting["time"], format="%a, %H:%M")
				if weekday_to_number(str(temp_time)[:3]) - 1 == datetime.weekday(datetime.now()):
					temporary_meetings.append(meeting)
			else:
				temporary_meetings.append(meeting)

	elif meeting_range == "15 Day":
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				time_diff = temp_time - datetime.now()
				if time_diff.days <= 15:
					temporary_meetings.append(meeting)
			else:
				temporary_meetings.append(meeting)

	else: # 30 Day
		for meeting in meetings:
			if meeting["category"] == "onetime":
				temp_time = datetime.strptime(meeting["time"], format="%Y-%m-%d, %H:%M")
				time_diff = temp_time - datetime.now()
				if time_diff.days <= 30:
					temporary_meetings.append(meeting)
			else:
				temporary_meetings.append(meeting)
		pass


def delete_meeting(time):
	meetings = Holder.meetings
	for meeting in meetings:
		if meeting["time"] == time:
			meeting["active"] = False
	Holder.meetings = meetings
	dict_to_json()
	return "Deleted"


def activate_meeting(time):
	meetings = Holder.meetings
	for meeting in meetings:
		if meeting["time"] == time and meeting["active"] == False:
			meeting["active"] = True
	Holder.meetings = meetings
	dict_to_json()
	return "Activated"


def past_meetings():
	past_meetings_list = []
	meetings = Holder.meetings
	for meeting in meetings:
		if meeting["active"] == False:
			past_meetings_list.append(meeting)
	return past_meetings_list


def clear_history():
	meetings = Holder.meetings
	for meeting in meetings:
		if meeting["active"] == False:
			meetings.remove(meeting)
	Holder.meetings = meetings
	dict_to_json()
	return "History Cleared"


def join_meeting(meeting_link):
	webbrowser.open(meeting_link)
	return "Joining ..."