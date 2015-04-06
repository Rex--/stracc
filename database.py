# Simple database, loads and saves data in weeks. Saves files in json format:
#   {
#       'week' : [int corresponding to the week number] (same as filename)
#       'days' : {
#                    '[date - "D/M/Y"]' : {
#                                             'dow' : [string of the day of week(Monday, etc.)],
#                                             'doy' : [int of the day of the year],
#                                             'breakfast' : {
#                                                               'bloodsugar' : [int],
#                                                               'shot': [string]
#                                                           },
#                                             'lunch' : {},
#                                             'dinner' : {},
#                                             'bedtime' : {}
#                                         }
#                }
#   }
#

import os
from datetime import date, datetime, timedelta
import json
import glob
import sys

class Database:

    def __init__(self, ptdb, name=None):
        self._date_format = '%d/%m/%Y'
        self._times_of_day = ['Breakfast', 'Lunch', 'Dinner', 'Bedtime']
        self._path_to_db = ptdb
        self._db_filename = self._path_to_db.split('/')[-1]
        if name != None:
            self._db_name = name
        else:
            self._db_name = self._db_filename
        self._root_db_file = os.path.join(self._path_to_db, self._db_filename + '.json')
        self._Database = self.__loadDB()


    def __loadDB(self):
        if not os.path.exists(self._path_to_db):
            self.__createDB()
        dbFile = open(self._root_db_file, 'rw')
        dbString = dbFile.read()
        dbFile.close()
        return json.loads(dbString)


    def __createDB(self):
        os.mkdir(self._path_to_db)
        today = date.today().strftime(self._date_format)
        dbFile = open(self._root_db_file, 'w')
        dbRootFile = {
            'name': self._db_name,
            'created': today,
            'updated': today
        }
        json.dump(dbRootFile, dbFile, indent=2)
        dbFile.close()

    def __updateDB(self, date):
        self._Database['updated'] = date

    # Checks to see if the datafile for the data exists. If it does, it does nothing,
    #   if it doesnt, it creates an empty file ready to call open() on
    #   Returns the path to the file
    # if weekNum is not None then it will use the current year unless
    #   weekYear is set.
    def __touchDataFile(self, date=None, weekNum=None, weekYear=None):
        if date != None:
            dateObj = datetime.strptime(date, self._date_format)
        elif weekNum != None:
            if weekYear == None:
                weekYear = datetime.today().strftime('%Y')
            dateObj = datetime.strptime('0'+'/'+weekNum+'/'+weekYear, '%w/%U/%Y')
        else:
            dateObj = datetime.today()
        dateYear = dateObj.strftime('%Y')
        dateMonth = dateObj.strftime('%B')
        dateWeek = dateObj.strftime('%U')
        dataFilePath = os.path.join(self._path_to_db, dateYear, dateMonth, dateWeek + '.json')
        # [year]/[month]/[weeknumber].json
        if not os.path.exists(dataFilePath):
            # [year]/[month]
            if not os.path.exists(os.path.join(self._path_to_db, dateYear, dateMonth)):
                # [year]
                if not os.path.exists(os.path.join(self._path_to_db, dateYear)):
                    # make year dir
                    os.mkdir(os.path.join(self._path_to_db, dateYear))
                # make month dir
                os.mkdir(os.path.join(self._path_to_db, dateYear, dateMonth))
            skelly = {
                'week': dateWeek,
                'days': {}
            }
            with open(dataFilePath, 'w') as dataFile:
                json.dump(skelly, dataFile, indent=2)
        return dataFilePath

    # To be called if the data is not the latest or for safety
    #   This function is slower than addNewData, but is safer.
    # date = a string of the date in format: %d/%m/%Y (ex. 05/12/2015)(or 'today')
    # timeOfDay = a string of the time of day (ex. 'Breakfast', 'Lunch', 'Dinner', 'Bedtime')
    # dtype = type of data (test or shot)
    # data = a string of the data to be stored.
    def addData(self, date, timeOfDay, dtype, data):
        if str(date) == 'today':
            date = datetime.today().strftime(self._date_format)
        dateObj = datetime.strptime(date, self._date_format)
        dataFilePath = self.__touchDataFile(date=date)
        dataFile = open(dataFilePath, 'r+')
        dataFileString = dataFile.read()    # Read db file
        dataFile.seek(0)    # Insert cursor at the beginning of the file
        week = json.loads(dataFileString)
        if date not in week['days']:
            week['days'][date] = {
                'dow': dateObj.strftime('%A'),
                'doy': dateObj.strftime('%j'),
                'Breakfast': {},
                'Lunch': {},
                'Dinner': {},
                'Bedtime': {}
            }
        week['days'][date][timeOfDay][dtype] = data
        dataFileString = json.dumps(week, indent=2)
        dataFile.write(dataFileString)
        dataFile.truncate()
        dataFile.close()
        self.__updateDB(datetime.today().strftime(self._date_format))

    # removes the data in [dtype] at [time] on [date]
    def removeData(self, date, timeOfDay, dtype):
        dataFilePath = self.__touchDataFile(date=date)
        dataFile = open(dataFilePath, 'r+')
        dataFileString = dataFile.read()
        week = json.loads(dataFileString)
        if dtype in week['days'][date][timeOfDay]:
            print week['days'][date][timeOfDay][dtype]
            del week['days'][date][timeOfDay][dtype]
        dataFile.seek(0)
        dataFileString = json.dumps(week, indent=2)
        dataFile.write(dataFileString)
        dataFile.truncate()
        self.__updateDB(datetime.today().strftime(self._date_format))


    # Used to get a specific data point at a specific point in time
    def getData(self, date, timeOfDay, dtype):
        dataFilePath = self.__touchDataFile(date=date)
        with open(dataFilePath, 'r') as dataFile:
            dataFileString = dataFile.read()
        week = json.loads(dataFileString)
        return week['days'][date][timeOfDay][dtype]

    # Returns a dictionary corresponding to the day,
    # if no records for the day exist it will return None
    # A call with no arguments returns today
    def getDay(self, date=None):
        if date == None:
            date = datetime.today().strftime(self._date_format)
        dataFilePath = self.__touchDataFile(date=date)
        with open(dataFilePath, 'r') as dataFile:
            dataFileString = dataFile.read()
        week = json.loads(dataFileString)
        return week['days'][date]


    # Returns a dictionary corresponding to the week number,
    # you can also specify a specific date and it will get that week.
    # If no records for the week exists, it will create it and return an empty week.
    # A call with no arguments returns this week.
    def getWeek(self, weekNum=None, weekYear=None, date=None,):
        if date != None:
            dataFilePath = self.__touchDataFile(date=date)
        elif weekNum != None:
            if weekYear == None:
                weekYear = datetime.today().strftime('%Y')
            dataFilePath = self.__touchDataFile(weekNum=weekNum, weekYear=weekYear)
        else:
            dataFilePath = self.__touchDataFile()
        dataFile = open(dataFilePath, 'r')
        dataFileString = dataFile.read()
        return json.loads(dataFileString)

    # Returns a dictionary corresponding to the month and year
    # if no year is given, it assumes this year, if no month is given it assumes this month
    # you can also specify a date and it will get that month.
    # A call with no arguments returns this month
    def getMonth(self, month=None, year=None, date=None):
        if date != None:
            dateObj = datetime.strptime(date, self._date_format)
        elif month == None and year == None:
            dateObj = datetime.today()
        elif month != None and year != None:
            dateObj = datetime.date(year, month, '1')
        elif month != None:
            dateObj = datetime.date(datetime.today().strftime('%Y'), month, '1')
        elif year != None:
            dateObj = datetime.date(year, datetime.today().strftime('%B'), '1')
        monthFolderPath = os.path.join(self._path_to_db, dateObj.strftime('%Y'), dateObj.strftime('%B'))
        weeksInMonth = glob.glob(os.path.join(monthFolderPath, '*.json'))
        monthData = {}
        for week in weeksInMonth:
            weekFile = open(week, 'r')
            weekString = weekFile.read()
            monthData[week.split('/')[-1].strip('.json')] = json.loads(weekString)
        return monthData

    # returns the all time data.. may take a while and might crash...
    #def getAllTime(self):
    #    timeDelta = datetime.strptime(self._Database['updated'], self._date_format) - datetime.strptime(self._Database['created'], self._date_format)
    #    st
    #    for i in range(timeDelta.days):


    # Returns the data [dtype] from [date] to [date]
    # from and to are strings formatted: %d/%m/%Y
    def getDataFromTo(self, fromDate, toDate, dtype='tests'):
        fDObj = datetime.strptime(fromDate, self._date_format)
        tDObj = datetime.strptime(toDate, self._date_format)
        if fDObj < tDObj:
            more = tDObj
            less = fDObj
        elif tDObj < fDObj:
            more = fDObj
            less = tDObj
        else:
            # Equal? Maube?
            return 'Tf? Try using getData()'

        difference = more - less
        timespan = {
            'span': difference,
            'days': {}
        }

        for i in range(difference.days + 1):
            dayCounter = timedelta(i)
            day = less + dayCounter
            dayS = day.strftime(self._date_format)
            timespan['days'][dayS] = self.getData(date=dayS, dtype=dtype)

        return timespan