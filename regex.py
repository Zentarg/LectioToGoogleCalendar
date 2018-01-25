# -*- coding: utf-8 -*-

import re
import sys

def getAdditionalContent(lesson_data):
	additional_content_pattern = re.compile(u"(?<=Øvrigt indhold:)([\s\S]*?)(?=$)")
	additional_content_search = re.search(additional_content_pattern, lesson_data)
	if additional_content_search is not None:
		return(additional_content_search.group(0))
	else:
		return("")

def getDate(lesson_data):
	date_pattern = re.compile(u"([1-9]|1[0-9]|2[0-9]|3[0-1])/([1-9]|1[0-2])-[0-9][0-9][0-9][0-9]")
	date_search = re.search(date_pattern, lesson_data)
	if date_search is not None:
		return(date_search.group(0))
	else:
		return("")

def getHomework(lesson_data):
	homework_pattern = re.compile(u"(?<=Lektier:\n)([\s\S]*?)(?=Note:|Øvrigt indhold:|$)")
	homework_search = re.search(homework_pattern, lesson_data)
	if homework_search is not None:
		return(homework_search.group(0))
	else:
		return("")
	
def getNote(lesson_data):
	note_pattern = re.compile(u"(?<=Note:\n)([\s\S]*?)(?=Øvrigt indhold:|$)")
	note_search = re.search(note_pattern, lesson_data)
	if note_search is not None:
		return(note_search.group(0))
	else:
		return("")

def getRoom(lesson_data):
	room_pattern = re.compile(u"(?:(?<=Lokale: )|(?<=Lokaler: ))([\s\S]*?)(?=Lektier:|Note:|Øvrigt indhold:|$)")
	room_search = re.search(room_pattern, lesson_data)
	if room_search is not None:
		return(room_search.group(0))
	else:
		return("")

def getTeacher(lesson_data):
	teacher_pattern = re.compile(u"(?:(?<=Lærer: )|(?<=Lærere: ))([\s\S]*?)\n")
	teacher_search = re.search(teacher_pattern, lesson_data)
	if teacher_search is not None:
		return(teacher_search.group(0))
	else:
		return("")

def getTeam(lesson_data):
	team_pattern = re.compile(u"(?<=Hold: )([\s\S]*?)(?=Lærere:|Lærer:|Lokale:|Lokaler:|Lektier:|Note:|Øvrigt indhold:|$)")
	team_search = re.search(team_pattern, lesson_data)
	if team_search is not None:
		return(team_search.group(0))
	else:
		return("")

def getTime(lesson_data):
	time_pattern = re.compile(u"([0-9][0-9]:[0-9][0-9] til [0-9][0-9]:[0-9][0-9])|(([1-9]|1[0-9]|2[0-9]|3[0-1])/([1-9]|1[0-2])-[0-9][0-9][0-9][0-9] [0-9][0-9]:[0-9][0-9] til ([1-9]|1[0-9]|2[0-9]|3[0-1])/([1-9]|1[0-2])-[0-9][0-9][0-9][0-9] [0-9][0-9]:[0-9][0-9])")
	time_search = re.search(time_pattern, lesson_data)
	if time_search is not None:
		return(time_search.group(0))
	else:
		return("")

def getTitle(lesson_data):
	title_pattern = re.compile(u"(?:(?<=Ændret!)|(?<=Aflyst!)|(?<=^))([\s\S]*?)\n")
	title_search = re.search(title_pattern, lesson_data)
	if title_search is not None:
		return(title_search.group(0))
	else:
		return("")

def getStatus(lesson_data):
	status_pattern = re.compile(u"(?:(Ændret!)|(Aflyst!))")
	status_search = re.search(status_pattern, lesson_data)
	if status_search is not None:
		return(status_search.group(0) + " - ")
	else:
		return("")
#print(getTitle(sys.argv[1]))